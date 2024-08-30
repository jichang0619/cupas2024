import os
import json
import time
import requests
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from openai import OpenAI
import cv2

load_dotenv()
API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)
target_url = "https://www.coupang.com/vp/products/6758436671"


class Result:
    def __init__(self):
        self.title = ''
        self.description = ''

result = Result()


def chat_with_gpt(text, max_tokens=300, system_role='You are a helpful assistant.'):
    print('chatGPT api requested..')
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": f"모든 답변은 한국어로 해줘.\n\n {text}"}
        ],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].message.content


def summarize_text(text):
    result_text = chat_with_gpt(f"아래 내용을 요약하는데, 줄바꿈 두 개로 구분된 각 문단이 별개의 내용이고, 내용 파악이나 요약이 어려운 문단의 경우는 요약하지 말고 넘어가. \n\n {text}")
    return result_text


def save_image_from_url(url, path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path)
    return img


def preprocess_image(image_path):
    base_name = os.path.basename(image_path)
    processed_image_path = os.path.join(os.path.dirname(image_path), f"processed_{base_name}")

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(processed_image_path, img_bin)

    return processed_image_path


def extract_text_from_image(image_path):
    processed_image_path = preprocess_image(image_path)
    img = Image.open(processed_image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, lang='kor', config=custom_config)
    return text


def create_output_folder():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(parent_dir, 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    existing_folders = [int(f) for f in os.listdir(output_dir) if f.isdigit()]
    if existing_folders:
        new_folder_name = str(max(existing_folders) + 1)
    else:
        new_folder_name = '0'

    new_folder_path = os.path.join(output_dir, new_folder_name)
    os.makedirs(new_folder_path)

    # 이미지 저장용 폴더 생성
    images_folder_path = os.path.join(new_folder_path, 'images')
    os.makedirs(images_folder_path)

    return new_folder_path, images_folder_path


def save_result_to_json(result, folder_path):
    result_file_path = os.path.join(folder_path, 'data.json')
    with open(result_file_path, 'w', encoding='utf-8') as f:
        json.dump(result.__dict__, f, ensure_ascii=False, indent=4)

    print(f"----- \n저장 위치 : {result_file_path} \n상품명: {result.title}\n-----")


def save_blog_post_to_txt(blog_post, folder_path):
    blog_post_file_path = os.path.join(folder_path, 'blog_post.txt')
    with open(blog_post_file_path, 'w', encoding='utf-8') as f:
        f.write(blog_post)

    print(f"블로그 글 저장 완료: {blog_post_file_path}")


def main(target_url, max_retries=3):
    retries = 0
    while retries < max_retries:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(target_url)

        time.sleep(2)

        try:
            product_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
            )
            product_name = product_name_element.text
            result.title = product_name
            print('-----\n상품명 추출 완료')
        except Exception as e:
            print(f"Error :: finding product name : {e}")
            driver.quit()
            return

        try:
            product_detail = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#productDetail"))
            )
            print('상세 컨텐츠 추출 완료')
        except Exception as e:
            print(f"Error :: 상품 상세 엘리먼트 : {e}")
            driver.quit()
            retries += 1
            print(f"재시도 중... ({retries}/{max_retries})")
            time.sleep(2)
            continue

        # 아웃풋 폴더 생성 (이미지 저장 폴더 포함)
        output_folder_path, images_folder_path = create_output_folder()

        # 이미지 파일 저장 및 텍스트 추출
        all_extracted_texts = []
        if product_detail:
            try:
                images = product_detail.find_elements(By.TAG_NAME, 'img')
                print('-----\n이미지 텍스트 추출 시작')
                if images:
                    for i, img in enumerate(images):
                        img_url = img.get_attribute('src')
                        img_path = os.path.join(images_folder_path, f'image_{i + 1}.png')
                        saved_img = save_image_from_url(img_url, img_path)
                        extracted_text = extract_text_from_image(img_path)
                        if extracted_text:
                            all_extracted_texts.append(extracted_text)
                else:
                    print("'#productDetail'에서 이미지가 발견되지 않음.")
            except Exception as e:
                print(f"Error :: 이미지 텍스트 추출: {e}")

        driver.quit()

        # 한 번의 요청으로 모든 이미지의 텍스트 요약
        if all_extracted_texts:
            print(f'all_extracted_texts : {all_extracted_texts}')
            combined_text = "\n\n".join(all_extracted_texts)
            img_summaries = summarize_text(combined_text)
            result.description += img_summaries + ". "

        # 결과를 JSON 파일로 저장
        save_result_to_json(result, output_folder_path)

        # 블로그 글 작성
        blog_post = chat_with_gpt(
            f"아래 상품명과 내용을 참고해서 상품을 홍보하는 블로그 글을 16줄 이상으로 작성해줘. 제일 처음에는 상품명이 포함된 제목을 작성하고, 각 문단에 문단 내용에 맞는 소제목을 달아줘. \n\n상품명 : {result.title} \n\n내용 :{result.description}", 1000, '너는 제품을 홍보하는 블로거야.')
        save_blog_post_to_txt(blog_post, output_folder_path)  # 블로그 글을 텍스트 파일로 저장
        break

    if retries >= max_retries:
        print("실패")


main(target_url)
