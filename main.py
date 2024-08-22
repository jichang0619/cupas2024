## 
# 1. Cupang 에서 상품 정보 가져오기 
# 2. 상품 동영상 만들기 (youtube 업로드)

import hmac
import hashlib
import requests
import json
from time import gmtime, strftime

REQUEST_METHOD = "POST"
DOMAIN = "https://api-gateway.coupang.com"
URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"

# Replace with your own ACCESS_KEY and SECRET_KEY
ACCESS_KEY = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

REQUEST = { "coupangUrls": [
    "https://www.coupang.com/np/search?component=&q=good&channel=user", 
    "https://www.coupang.com/np/coupangglobal"
]}


def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
    message = datetimeGMT + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)


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