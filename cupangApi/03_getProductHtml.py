import requests
from bs4 import BeautifulSoup

def save_html_from_url(url, file_name):
    try:
        # URL로부터 HTML 가져오기
        response = requests.get(url)
        response.raise_for_status()  # 요청에 실패하면 예외 발생

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # HTML을 파일로 저장
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        print(f"HTML 파일이 성공적으로 저장되었습니다: {file_name}")
    
    except requests.exceptions.RequestException as e:
        print(f"URL 요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")

# 사용 예시
save_html_from_url('https://www.naver.com', 'example.html')