import os
import logging
import traceback

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

file_log = logging.FileHandler('log_client.log', encoding='utf-8')
logging.basicConfig(handlers=(file_log,),
                    format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s',
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

log = logging.getLogger("parser")


class Client:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.page_load_strategy = 'eager'
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationController")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument(f"user-data-dir={os.getcwd()}/cookie")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1920, 1080)

    @staticmethod
    def format_views(views):
        if 'тыс.' in views:
            return int(views.split('тыс.')[0].strip()) * 1000
        elif 'млн' in views:
            return float(views.split('млн')[0].strip().replace(',', '.')) * 1000000
        else:
            return int(views.split('просмотр')[0].replace(' ', ''))

    def parse(self, urls):
        try:
            result = pd.DataFrame({'Ссылка': [], "Просмотры": []})
            for url in urls:
                self.driver.get(url)
                views = self.driver.find_element(By.CLASS_NAME, 'bold.style-scope.yt-formatted-string')
                result.loc[len(result)] = [url, self.format_views(views.text)]
            return result
        except Exception as ex:
            log.error({'error': ex, 'traceback': traceback.format_exc()})
            print('Произошла неизвестная ошибка, отправьте файл log_client.log разработчику')

    def quit(self):
        self.driver.quit()
