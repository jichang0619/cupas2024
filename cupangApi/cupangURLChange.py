import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
import os
from dotenv import load_dotenv

load_dotenv()

# 모든 request header의 Authorization에 생성한 HMAC signature를 함께 보내줘야 함.
def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
    message = datetimeGMT + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)

# 일반 쿠팡 상품 URL 을 쿠팡파트너스 내 계정 연계된 URL 로 변경하기 위한 코드
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
    







