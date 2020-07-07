from selenium import webdriver
from selenium.common import exceptions as DriverExceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
import time
import numpy as np
import urllib.request as request
from multiprocessing.pool import ThreadPool
import requests.exceptions as reqexception


class AliExpressScraper:
    current_url = ""
    list_of_url = ""
    information = {}

    def __init__(self):
        print("-----------------INITIALIZING SCRAPER--------------\n")
        # print(self.ascii_art)
        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(1920, 1024)
        except reqexception.ConnectionError:
            print("\n--PLEASE CHECK YOUR INTERNET CONNECTION--")
            exit()
        except DriverExceptions.InvalidSessionIdException:
            print("\nBROWSER CLOSED UNEXPECTEDLY:.....")
            exit()

        except DriverExceptions.SessionNotCreatedException:
            print("\nBROWSER CLOSED BEFORE SESSION WAS CREATED")
            exit()

    def update_url(self, url):
        if url:
            try:
                response = request.urlopen(url).getcode()
                if response == 200:
                    self.current_url = url
                    return True
                else:
                    print("\nPlease Check The Url")
                    return False
            except reqexception.ConnectionError:
                print("\nCHECK INTERNET CONNECTION")
                return False


    def read_url_from_file(self, file):
        try:
            f = open(file, "r")
            self.list_of_url = f.read()
            return True
        except OSError:
            print("\n\n" + file + "-----NOT FOUND")
            return False

    def load_url(self):
        try:
            self.driver.get(self.current_url)
            _ = self.driver.find_element_by_xpath('//*[@id="root"]')
            try:
                wait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-dialog-body")))
                self.driver.find_element_by_class_name("next-dialog-close").click()
            except DriverExceptions.NoSuchElementException:
                print("No POP-UP Detected")
                pass
            return True
        except DriverExceptions.NoSuchElementException:
            print("THE URL ENTERED IS NOT COMPATIBLE WITH THE PROGRAM\n")
            print("PLEASE ENTER A VALID URL")
            print("ANY ALI-EXPRESS PAGE TO BUY A PRODUCT IS VALID \n")
            return False

    def update_basic_information(self):
        self.information["price"] = self.driver.find_element_by_class_name('product-price-value')
        self.information["title"] = self.driver.find_element_by_class_name('product-title-text')
        self.information["store"] = self.driver.find_element_by_class_name('store-name')
        self.information["images"] = self.driver.find_elements_by_xpath('//div[@class="images-view-item"]/img')
        self.information["qty"] = self.driver.find_element_by_class_name("product-quantity-tip")

    def show_info(self):
        print(self.information["qty"].text)
        print(self.information["price"].text)
        print(self.information["store"].text)
        print(self.information["title"].text)

    def terminate(self):
        self.driver.quit()

test=input("Enter URL to scrape : ")
scrape = AliExpressScraper()
scrape.read_url_from_file(test)
if scrape.update_url(test):
    if scrape.load_url():
        scrape.update_basic_information()
        scrape.show_info()
        print("-----------THE SCRAPING COMPLETED SUCCESSFULLY----------\n\n")

scrape.terminate()
