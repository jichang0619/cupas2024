from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException

tistory_url = "https://www.tistory.com/"

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)
# 브라우저 사이즈
driver.set_window_size(1900, 1000)
# 웹페이지 로드될 때까지 2초 대기
driver.implicitly_wait(time_to_wait=2)

driver.get(tistory_url)

# 카카오 계정 로그인 추가 인증 같은게 필요함.. 기존 브라우저에서 할 수 있는 방법 없나..
