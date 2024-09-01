import os
import requests
import json
from common import generateHmac
from dotenv import load_dotenv

# env 
load_dotenv()

def is_id_unique(new_id, json_file_path):
    """
    Check if the generated ID is unique within the given JSON file.

    :param new_id: The ID to check for uniqueness.
    :param json_file_path: Path to the JSON file.
    :return: True if the ID is unique, False otherwise.
    """
    if not os.path.exists(json_file_path):
        print("JSON file does not exist.")
        return False

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Assume that the JSON data is a list of dictionaries with an 'id' key.
    for entry in data:
        if entry.get('id') == new_id:
            return False

    return True

# 전체 상품 정보 저장
def save_productinfo_as_json(string_data, folder_path):
    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 파일 경로 설정
    file_path = os.path.join(folder_path, f"productInfo.json")
    
    # 파일이 존재하면 기존 데이터를 읽어오고, 존재하지 않으면 빈 리스트로 시작
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            try:
                existing_data = json.load(json_file)  # 기존 데이터 읽기
            except json.JSONDecodeError:
                existing_data = []  # 파일이 비었거나 JSON이 잘못된 경우 빈 리스트로 설정
    else:
        existing_data = []  # 파일이 없으면 빈 리스트

    # 문자열을 JSON 형식으로 변환
    new_data = json.loads(string_data)
    
    # 기존 데이터가 리스트 형태인 경우 새 데이터를 추가
    if isinstance(existing_data, list):
        existing_data.append(new_data)
    else:
        # 기존 데이터가 리스트가 아니면, 리스트로 변환해서 새 데이터를 추가
        existing_data = [existing_data, new_data]

    # 수정된 데이터를 다시 파일에 저장 (덮어쓰기)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    print(f"새로운 데이터가 추가되었습니다: {file_path}")
    
    
def get_best_product_url (coupang_category_id, item_num):
    
    # 현재 파일의 디렉토리 위치를 가져옴
    file_name = "productInfo.json"
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    output_directory = os.path.join(parent_directory, 'output')
    json_file_path = os.path.join(output_directory, file_name)
    
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    PARTNER_ID = "YOUR_PARTNER_ID"
    REQUEST_METHOD = "GET"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/products/bestcategories/" + str(coupang_category_id) + '?limit=' + str(item_num) + '&subId=' + PARTNER_ID
    
    # HMAC 서명 생성
    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = "{}{}".format(DOMAIN, URL)
    response = requests.request(method=REQUEST_METHOD, url=url,
                                headers={
                                    "Authorization": authorization,
                                    "Content-Type": "application/json"
                                }
                            )

    # API 응답 데이터 파싱
    data = response.json()

    # 상품 정보 출력
    for item in data['data']:
        productId = item['productId']
        productName = item['productName']
        productPrice = item['productPrice']
        productImage = item['productImage']
        productUrl = item['productUrl']
        
    # JSON 파일의 ID 항목 중 중복되는 것이 없으면 TRUE
    bValid = is_id_unique (productId, json_file_path)
    
    if bValid == True :
        string_data = "Id: {}, Product Name: {}, Product Price : {}, ProductImage URL: {}, Product URL : {}".format(productId, productName, productPrice, productImage, productUrl)
        
        save_productinfo_as_json(string_data, output_directory, file_name)
    
    return bValid, productUrl



    




    


