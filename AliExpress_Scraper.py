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
import requests.exceptions as RException


class AliExpressScraper:
    current_url = ""
    list_of_url = ""
    information = {}
    links_for_color = []

    # ----------Flags--------------
    # ----------Flags--------------

    def __init__(self):
        self.index = 0;
        print("-----------------INITIALIZING SCRAPER--------------\n")
        # print(self.ascii_art)
        # ----------Flags--------------
        self.color_flag = False
        self.shipping_flag = False
        self.size_flag = False
        self.description_flag = False
        self.size_color_matrix_flag = False
        # ----------Flags--------------
        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(1920, 1024)
        except RException.ConnectionError:
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
            except RException.ConnectionError:
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

    def get_variations(self):
        sku_properties = self.driver.find_elements_by_xpath("//div[@class='sku-wrap']/div[@class='sku-property']")
        for key, _ in enumerate(sku_properties):
            xpath2 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/div"
            element = self.driver.find_element_by_xpath(xpath2)
            xpath3 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/ul/li"
            print(element.text)
            if "Color:" in element.text:
                self.color_flag = True
                self.information["track_color_selection"] = self.driver.find_elements_by_xpath(xpath3)
                self.information["color_elements"] = self.driver.find_elements_by_xpath(xpath3 + "/div/img")
                self.information["color_details"] = []
                for index, color in enumerate(self.information["color_elements"]):
                    self.information["color_details"].append(
                        [color.get_attribute("title"), color.get_attribute("src")])

            elif element.text == "Ships From:":
                self.shipping_flag = True
                self.information["shipping_elements"] = self.driver.find_elements_by_xpath(xpath3)
                self.information["shipping_details"] = []
                for ship in self.information["shipping_elements"]:
                    # self.driver.execute_script("arguments[0].scrollIntoView(true);", ship)
                    ship.click()
                    _ = wait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[@class='product-shipping-info black-link']")))
                    time.sleep(1)
                    self.information["shipping_details"].append(
                        self.driver.find_element_by_class_name("product-shipping").text)
            elif element.text == "Size:":
                self.information["size_elements"] = self.driver.find_elements_by_xpath(xpath3)
                self.size_flag = True
                self.information["size_details"] = []
                for size in self.information["size_elements"]:
                    self.information["size_details"].append(size.text)
        if (self.color_flag and self.size_flag):
            self.price_for_size_and_colors()

    def price_for_size_and_colors(self):
        self.size_color_matrix_flag = True
        self.size_color_matrix = np.zeros(
            shape=(len(self.information["color_elements"]), len(self.information["size_elements"])), dtype=object)
        if self.shipping_flag:
            self.information["variation_in_size_and_color"] = np.empty(len(self.information["shipping_elements"]),
                                                                       dtype=object)
        while True:
            if self.shipping_flag:
                try:
                    self.information["shipping_elements"][self.index].click()
                except IndexError:
                    break
            for i, color in enumerate(self.information["color_elements"]):
                if "selected" in self.information["track_color_selection"][i].get_attribute("class"):
                    print("SELECTED HURRAH")
                else:
                    color.click()
                for j, size in enumerate(self.information["size_elements"]):
                    try:
                        size.click()
                        time.sleep(0.2)
                        temp = self.driver.find_element_by_class_name(
                            'product-price-value').text + "||" + re.sub('\spieces available\s', '',
                                                                        self.driver.find_element_by_class_name(
                                                                            "product-quantity-tip").text)
                        self.size_color_matrix[i][j] = temp
                    except DriverExceptions.NoSuchElementException:
                        print("Size for " + color.get_attribute("title") + "\tUNAVAILABLE")
                        continue
            print("VALUE APPENDED TO THE ARRAY IS: \n")
            print(self.size_color_matrix)
            self.information["variation_in_size_and_color"][self.index]=(self.size_color_matrix)
            print("VALUE RIGHT AFTER ASSIGNMENT: \n")
            print(self.information["variation_in_size_and_color"][self.index])
            self.index += 1
        print(self.information["variation_in_size_and_color"])

    def show_info(self):
        print("VALUE AFTER STORING\n")
        if self.size_color_matrix_flag: print(self.information["variation_in_size_and_color"])

        print("\n")

        if self.shipping_flag:
            print(self.information["shipping_details"])
        else:
            print(self.driver.find_element_by_class_name("product-shipping").text)

        print("\n STORE INFO---\n")
        print(self.information["store"].text)
        print(self.information["title"].text)
        if self.size_color_matrix_flag: print(self.size_color_matrix)

    def terminate(self):
        self.driver.quit()


# test=input("Enter URL to scrape : ")
test = "https://www.aliexpress.com/item/4001139880092.html?spm=2114.12010612.8148356.3.7d814f04zET2wu"
scrape = AliExpressScraper()
# scrape.read_url_from_file(test)
if scrape.update_url(test):
    if scrape.load_url():
        scrape.update_basic_information()
        scrape.get_variations()
        scrape.show_info()
        print("-----------THE SCRAPING COMPLETED SUCCESSFULLY----------\n\n")

scrape.terminate()
