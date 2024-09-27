import time as sleep_time
from datetime import datetime, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from config import *
from db import *
class ContractScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.page = 1

    def setup_driver(self):
        """Thiết lập trình duyệt và vào trang web."""
        try:
            self.driver = webdriver.Firefox()
            self.driver.get(self.url)
            self.driver.implicitly_wait(10)
            sleep_time.sleep(5)  
        except Exception as e:
            print(f"Error setup driver: {e}")

    def select_items_per_page(self, value="50"):
        """Chọn số lượng mục hiển thị trên mỗi trang."""
        try:
            select_element = self.driver.find_element(By.CSS_SELECTOR, 'select[style="border-radius: 5px;"]')
            select = Select(select_element)
            select.select_by_value(value)  
            sleep_time.sleep(2)  
        except Exception as e:
            print(f"Error select items per page: {e}")

    def scrape_page(self):
        """Thu thập dữ liệu từ trang hiện tại."""
        try:
            sleep_time.sleep(15)  
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find_all('div', class_='content__body__left__item__infor')
            print(f"Number of items found: {len(items)} - page: {self.page}")

            for item in items:
                code_elem = item.find('p', class_='content__body__left__item__infor__code')
                code = code_elem.text.strip() if code_elem else None

                notice_element = item.find('span', class_='content__body__left__item__infor__notice')
                if notice_element is None:
                    notice_element = item.find('span', class_='content__body__left__item__infor__notice--be')

                notice = notice_element.text.strip() if notice_element else "N/A"

                contract_name_elem = item.find('h5', class_='content__body__left__item__infor__contract__name format__text__title')
                contract_name = contract_name_elem.text.strip() if contract_name_elem else None

                details = item.find_all('h6', class_='format__text')
                inviter = details[0].find('span').text.strip() if len(details) > 0 and details[0].find('span') else None
                investor = details[1].find('span').text.strip() if len(details) > 1 and details[1].find('span') else None

                date_posted = None
                for h6 in item.find_all('h6'):
                    if 'Ngày đăng tải thông báo' in h6.get_text():
                        date_posted_span = h6.find('span')
                        date_posted = date_posted_span.text.strip() if date_posted_span else None

                field = None
                location = None
                for h6 in item.find_all('h6'):
                    if 'Lĩnh vực' in h6.get_text():
                        field_span = h6.find('span')
                        field = field_span.text.strip() if field_span else None
                    elif 'Địa điểm' in h6.get_text():
                        location_span = h6.find('span')
                        location = location_span.text.strip() if location_span else None

                closing_time_elem = item.find('h5').find_next('h5') if item.find('h5') else None
                closing_time = closing_time_elem.text.strip() if closing_time_elem else None

                closing_date_elem = item.find('h5').find_next('h5').find_next('h5') if item.find('h5') else None
                closing_date = closing_date_elem.text.strip() if closing_date_elem else None

                bidding_method = None
                bidding_form_p = item.find('p', string=lambda text: 'Hình thức dự thầu' in text if text else False)
                if bidding_form_p:
                    bidding_method_elem = bidding_form_p.find_next('h5')
                    bidding_method = bidding_method_elem.text.strip() if bidding_method_elem else None

                # Chuyển đổi thành datetime, time và date
                if date_posted:
                    date_posted = datetime.strptime(date_posted, "%d/%m/%Y - %H:%M")
                if closing_time:
                    closing_time = datetime.strptime(closing_time, "%H:%M").time()
                if closing_date:
                    closing_date = datetime.strptime(closing_date, "%d/%m/%Y").date()

                self.save_data(code, notice, contract_name, inviter, investor, date_posted, field, location, closing_time, closing_date, bidding_method)

                
        except Exception as e:
            print(f"Error scape_page: {e}")

    def next_page(self):
        """Chuyển sang trang tiếp theo."""
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, 'button.btn-next')
            if next_button.is_enabled():
                next_button.click()
                self.page += 1
                return True
            else:
                return False
        except Exception as e:
            print(f"Error next_page: {e}")
            return False

    def save_data(self, code, notice, contract_name, inviter, investor, date_posted, field, location, closing_time, closing_date, bidding_method):
        """Lưu dữ liệu vào tệp JSON."""
        try:
            new_contract = Contract(
            code=code,
            notice=notice,
            contract_name=contract_name,
            inviter=inviter,
            investor=investor,
            date_posted=date_posted,
            field=field,
            location=location,
            closing_time=closing_time,
            closing_date=closing_date,
            bidding_method=bidding_method
        )
            session = Session()
            session.add(new_contract)
            session.commit()
        except Exception as e:
            print(f"Error save_data: {e}")

    def close_driver(self):
        """Đóng trình duyệt."""
        if self.driver:
            self.driver.quit()

    def run(self):
        """Chạy quá trình thu thập dữ liệu."""
        self.setup_driver()
        self.select_items_per_page("50")

        has_next_page = True
        while has_next_page == True:
            self.scrape_page()
            
            has_next_page = self.next_page()
        
        self.close_driver()

if __name__ == "__main__":
    url = URL_PAGE
    scraper = ContractScraper(url)
    scraper.run()
