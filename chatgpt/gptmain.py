from chatgpt.openai_client import chat_with_gpt, create_image
from chatgpt.crawler import fetch_product_data
from chatgpt.utils import save_image, save_image_from_url, extract_text_from_image, create_output_folder, save_result_to_json, save_blog_post_to_txt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def main(url, max_retries=3):
    retries = 0
    driver = None

    while retries < max_retries:
        try:
            driver = setup_driver()
            result, images = fetch_product_data(driver, url)

            if not result or not images:
                retries += 1
                print(f"상품 정보를 가져오는 데 실패했습니다. 재시도 중... ({retries}/{max_retries})")
                time.sleep(2)
                continue

            # 출력 폴더 생성
            output_folder, images_folder = create_output_folder()

            # 대표 이미지 생성 및 저장
            image_prompt = f"상품명: {result.title}, 카테고리: {result.category}에 맞는 블로그용 썸네일 이미지를 생성해줘."
            image_data = create_image(image_prompt)
            save_image(image_data, images_folder)

            # 이미지 텍스트 추출
            all_extracted_texts = []
            for i, img in enumerate(images):
                img_url = img.get_attribute('src')
                img_path = f"{images_folder}/image_{i + 1}.png"
                save_image_from_url(img_url, img_path)
                extracted_text = extract_text_from_image(img_path)
                if extracted_text:
                    all_extracted_texts.append(extracted_text)

            # 텍스트 요약
            if all_extracted_texts:
                combined_text = "\n\n".join(all_extracted_texts)
                result.description = chat_with_gpt(f"아래 내용을 요약해줘.\n\n{combined_text}")

            # 결과 텍스트 파일 저장
            save_result_to_json(result, output_folder)

            # 블로그 글 작성 및 저장
            blog_post = chat_with_gpt(
                f"아래 상품명과 내용을 참고해서 상품을 홍보하는 블로그 글을 16줄 이상으로 작성해줘. 제일 처음에는 상품명이 포함된 제목을 작성하고, 내용의 맨 처음에 {url} 을 표시해줘 , 각 문단에 문단 내용에 맞는 소제목을 달아줘. 소제목 : 이라고 쓰지말고 Bold 처리 해줘, 그리고 맨 마지막엔 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다. 라고 한 문장 써줘 \n\n상품명 : {result.title} \n\n내용 :{result.description}\n\n카테고리: {result.category}",
                1000, '너는 제품을 홍보하는 블로거야.')
            save_blog_post_to_txt(blog_post, output_folder)

            break

        except Exception as e:
            retries += 1
            print(f"오류 발생: {e}. 재시도 중... ({retries}/{max_retries})")
            time.sleep(5)

        finally:
            if driver:
                driver.quit()

    if retries >= max_retries:
        print("최대 재시도 횟수를 초과하여 실패했습니다.")

if __name__ == "__main__":
    main()
