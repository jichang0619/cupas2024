import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta

# env 
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_KEY = os.getenv('ACCESS_KEY')
PARTNER_ID = "YOUR_PARTNER_ID"

REQUEST_METHOD = "GET"
DOMAIN = "https://api-gateway.coupang.com"
coupang_item_limit = 1 # 한번에 가져올 개수(카테고리별)

# 문자열 정제 함수
def clearStr(str):
    return str.replace(" ", "").replace(",", "").replace("원", "").replace("\n", "").replace("%", "")

# HMAC 서명 생성 함수
def generateHmac(method, url, secretKey, accessKey):
    path = url.split("?")[0]
    query = url.split("?")[1:]
    datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
    message = datetimeGMT + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)

# Shorten URL 변경 함수
def cupangURLChanger (inputURL):
    # deeplink 파라미터 사용
    SECRET_KEY = os.getenv('SECRET_KEY')
    ACCESS_KEY = os.getenv('ACCESS_KEY')

    REQUEST_METHOD = "POST"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

    product_URL = inputURL

    REQUEST = { "coupangUrls": [
        product_URL
    ]}
    
    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = "{}{}".format(DOMAIN, URL)
    
    response = requests.request(method=REQUEST_METHOD, url=url,
                            headers={
                                "Authorization": authorization,
                                "Content-Type": "application/json"
                            },
                            data=json.dumps(REQUEST)
                            )
    
    print(response.json())
    shortenURL = response.json()['data'][0]['shortenUrl']
    
    return shortenURL

# 전체 상품 정보 저장
def save_ProductInfo(string_data, folder_path):
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
    
# 카테고리 ID와 이름 매핑
categories = {
    1001: '여성패션',
    1002: '남성패션',
    1010: '뷰티',
    1011: '출산/유아동',
    1012: '식품',
    1013: '주방용품',
    1014: '생활용품',
    1015: '홈인테리어',
    1016: '가전디지털',
    1017: '스포츠/레저',
    1018: '자동차용품',
    1019: '도서/음반/DVD',
    1020: '완구/취미',
    1021: '문구/오피스',
    1024: '헬스/건강식품',
    1025: '국내여행',
    1026: '해외여행',
    1029: '반려동물용품',
    1030: '유아동패션'
}

# 모든 카테고리에 대해 반복
for key, value in categories.items():
    coupang_category_id = key

    REQUEST_METHOD = "GET"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/products/bestcategories/" + str(coupang_category_id) + '?limit=' + str(coupang_item_limit) + '&subId=' + PARTNER_ID

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
        
    
    shortenURL = cupangURLChanger(productUrl)    
    string_data = "Id: {}, Product Name: {}, Product Price : {}, ProductImage URL: {}, Product URL : {}, Shorten URL : {}".format(productId, productName, productPrice, productImage, productUrl, shortenURL)
    folder_path = "cupas2024\Output"
    file_name = "All Product Info"
    save_ProductInfo(string_data, folder_path, file_name)
    
    # 폴더 생성은 ID 로 


