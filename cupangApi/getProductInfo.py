import os
import requests
import json
from cupangApi.common import generateHmac 
from dotenv import load_dotenv
import random
from datetime import datetime

# env 
load_dotenv()

# JSON 파일 경로
JSON_FILE_PATH = "coupang_products.json"

def fetch_product(category_id):
    SECRET_KEY = os.getenv('CP_SECRET_KEY')
    ACCESS_KEY = os.getenv('CP_ACCESS_KEY')
    PARTNER_ID = os.getenv('PARTNER_ID')
    REQUEST_METHOD = "GET"
    DOMAIN = "https://api-gateway.coupang.com"
    URL = f"/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/{category_id}?limit=20&subId={PARTNER_ID}"
    
    # HMAC 서명 생성
    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = f"{DOMAIN}{URL}"
    response = requests.request(method=REQUEST_METHOD, url=url,
                                headers={
                                    "Authorization": authorization,
                                    "Content-Type": "application/json"
                                }
                            )

    if response.status_code == 200:
        data = response.json()
        if data['rCode'] == '0' and len(data['data']) > 0:
            return data['data']
    
    return None

def save_to_json(product):
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            products = json.load(file)
    else:
        products = []
    
    # 중복 체크
    if not any(item['productId'] == product['productId'] for item in products):
        products.append({
            "productId": product['productId'],
            "productName": product['productName'],
            "productPrice": product['productPrice'],
            "productImage": product['productImage'],
            "productUrl": product['productUrl'],
            "fetchDate": datetime.now().isoformat()
        })
        
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(products, file, ensure_ascii=False, indent=2)
        
        return True
    return False

def get_product_info(category_id):
    products = fetch_product(category_id)
    
    if products:
        random.shuffle(products)
        for product in products:
            if save_to_json(product):
                return product['productId'], product['productUrl'], product['productImage']
        
        print("모든 상품이 이미 존재합니다. 다른 카테고리를 선택해 주세요.")
    else:
        print("상품을 가져오는데 실패했습니다.")
    
    return None, None

if __name__ == "__main__":
    category_id = input("카테고리 ID를 입력하세요: ")
    id, url, image = get_product_info(category_id)
    if url and image:
        print(f"상품 URL: {url}")
        print(f"상품 이미지: {image}")