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

    def get_views(self):
        metas = self.driver.find_elements(By.TAG_NAME, 'meta')
        for meta in metas:
            if meta.get_attribute('itemprop') == 'interactionCount':
                return int(meta.get_attribute('content'))
        return 0

    def parse(self, urls):
        try:
            result = pd.DataFrame({'Ссылка': [], "Просмотры": []})
            for i, url in enumerate(urls):
                print(f'Парсинг {i + 1}/{len(urls)}')
                self.driver.get(url)

                result.loc[len(result)] = [url, self.get_views()]
            return result
        except Exception as ex:
            log.error({'error': ex, 'traceback': traceback.format_exc()})
            print('Произошла неизвестная ошибка, отправьте файл log_client.log разработчику')

    def quit(self):
        self.driver.quit()
