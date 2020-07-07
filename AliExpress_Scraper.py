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
    url = ""
    list_of_url = ""

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
        try:
            response = request.urlopen(url).getcode()
            if response == 200:
                self.url = url
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

    def terminate(self):
        self.driver.quit()



scrape = AliExpressScraper()
scrape.read_url_from_file("aliexpress34url.txt")
scrape.update_url("https://stackoverflow.com/questions/1949318/checking-if-a-website-is-up-via-python")
scrape.terminate()
