import sys
import os
from cupangApi import getProductInfo
from cupangApi import getShortenUrl
import chatgpt
import time

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

def main():
    """
    Main functions.
    """

    # CASE 1 : Category 별 Best 상품, 갯수
    category_id = categories[0]
    item_num = 1
    
    # Product ID 가 겹치는지 확인 후 저장
    bValid, product_url = getProductInfo.get_best_product_url(category_id, item_num)
    time.sleep(1.0)
    
    # Change Url To Shorten URL
    if (bValid == True):
        ShortenURL = getShortenUrl.ChangeShortenUrl(product_url)
    else:
        ShortenURL = ''
    
    time.sleep(1.0)
    ## ChatGPT 이용하여 TEXT, 이미지 생성 코드 call 
    ## ex) chatgpt.main(ShortenURL)


if __name__ == "__main__":
    main()

