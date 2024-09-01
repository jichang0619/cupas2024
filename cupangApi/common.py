import hmac
from time import gmtime, strftime
import hashlib

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