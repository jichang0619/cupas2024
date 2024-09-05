from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Result:
    def __init__(self):
        self.title = ''
        self.description = ''
        self.category = ''

def fetch_product_data(driver, url):
    result = Result()

    try:
        driver.get(url)

        product_name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        result.title = product_name_element.text
        print('-----\n상품명 추출 완료')

        category_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#breadcrumb"))
        )
        result.category = category_element.text.replace('\n', ' > ')
        print(f'카테고리 추출 완료: {result.category}')

        product_detail = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#productDetail"))
        )
        images = product_detail.find_elements(By.TAG_NAME, 'img')
        print('상세 컨텐츠 추출 완료')

        return result, images

    except Exception as e:
        print(f"Error 발생: {e}")
        return None, None
