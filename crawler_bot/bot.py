import csv
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver


class Bot(ABC):
    def __init__(self, driver_path, output_path, base_url, config_parser, implicitly_wait=25):
        self.output_path = output_path
        self.config_parser = config_parser
        self.base_url = base_url
        self.implicitly_wait = implicitly_wait
        if not bool(driver_path):
            driver_path = '/chromedriver.exe'
        self.driver = webdriver.Chrome(driver_path)
        myclient = MongoClient("mongodb://localhost:27017/")
        mydb = myclient["crawler"]
        self.mycol = mydb["badongsan"]

    def crawling(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(self.implicitly_wait)
        soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        return self.parse_data(soup)

    @abstractmethod
    def auto_craw(self, config):
        raise NotImplementedError()

    @abstractmethod
    def parse_data(self, soup_of_page):
        raise NotImplementedError()

    def to_csv(self, data):
        keys = data[0].keys()
        with open(self.output_path, 'w', newline='', encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def to_mongo(self, data):
        print("=> Save to db\n")
        for el in data:
            self.mycol.insert_one(el)
