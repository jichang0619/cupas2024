import os
import requests
import json
from common import generateHmac
from dotenv import load_dotenv


# env 
load_dotenv()

# Shorten URL 변경 함수
def ChangeShortenUrl (inputURL):
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