# -*- coding: utf-8 -*-
# ================================================================================
#          /\_/\  
#         ( o.o ) 
#          > ^ <
# ================================================================================
#                   Project: CUPANG PARTNER PROJ
#                   Created by: Y.S. Oh, J.C. Kim
#                   Date: 2024-09-01
#                   Description: This is a project for automating Coupang Partners
# ================================================================================


from cupangApi.getProductInfo import get_product_info
from chatgpt.gptmain import main as chatgpt_main
from cupangApi.getShortenUrl import ChangeShortenUrl

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
    1026: '해외여행', # 안되는듯
    1029: '반려동물용품',
    1030: '유아동패션'
}

def main():
    category_id = input("카테고리 ID를 입력하세요: ")
    id, url, image = get_product_info(category_id)
    
    if id and url and image:
        print(f"상품 ID: {id}")
        print(f"상품 URL: {url}")
        print(f"상품 이미지: {image}")
        time.sleep(1.0)
        ## Change Shorten URL
        ## Shorten URL 할 때 위 url 을 그대로 쓰면 변환이 안됨
        ## 그래서 상품 id 이용
        modiURL = f"https://www.coupang.com/vp/products/{id}"
        ShortenURL = ChangeShortenUrl(modiURL)
        print(ShortenURL)
        
        print("크롤링 및 블로그 포스트 생성을 시작합니다...")
        chatgpt_main(ShortenURL)
    else:
        print("상품 정보를 가져오는데 실패했습니다.")
    
    time.sleep(1.0)
    

if __name__ == "__main__":
    main()
    
