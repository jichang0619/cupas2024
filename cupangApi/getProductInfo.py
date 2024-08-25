import hmac
import hashlib
import requests
import json
from time import gmtime, strftime
import os
from dotenv import load_dotenv

load_dotenv()

# deeplink 파라미터 사용

SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_KEY = os.getenv('ACCESS_KEY')

REQUEST_METHOD = "GET"
DOMAIN = "https://api-gateway.coupang.com"
URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/product"

# "productUrl" 정보에 링크 있음

# 카테고리별 Best 아이템 추출하기
