import os
import cv2
import requests
from PIL import Image
from io import BytesIO
import pytesseract
import json


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
    return pytesseract.image_to_string(img, lang='kor', config=custom_config)


def create_output_folder():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(parent_dir, 'output')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    existing_folders = [int(f) for f in os.listdir(output_dir) if f.isdigit()]
    new_folder_name = str(max(existing_folders) + 1) if existing_folders else '0'

    new_folder_path = os.path.join(output_dir, new_folder_name)
    os.makedirs(new_folder_path)

    images_folder_path = os.path.join(new_folder_path, 'images')
    os.makedirs(images_folder_path)

    return new_folder_path, images_folder_path


def save_result_to_json(result, folder_path):
    result_file_path = os.path.join(folder_path, 'data.json')
    with open(result_file_path, 'w', encoding='utf-8') as f:
        json.dump(result.__dict__, f, ensure_ascii=False, indent=4)

    print(f"----- \n저장 위치 : {result_file_path} \n상품명: {result.title}\n카테고리: {result.category}")


def save_txt(contents, folder_path, file_name='file_name'):
    file_path = os.path.join(folder_path, f'{file_name}.txt')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(contents)

    print(f"텍스트 파일 {file_name} 저장 위치: {file_path}")


def save_image(image_data, save_path, file_name):
    if not save_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        save_path += f'/{file_name}.jpg'

    image_url = image_data[0].url
    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))
    img.save(save_path)

    print(f"이미지 저장 위치: {save_path}")

def download_hero_image(img_url, save_path):
    response = requests.get(img_url)
    if response.status_code == 200:
        with open(f'{save_path}/hero.jpg', 'wb') as file:
            file.write(response.content)
        print(f"쿠팡 대표 이미지 저장 완료: {save_path}")
    else:
        print(f"쿠팡 대표 이미지 다운로드 실패: {img_url}")