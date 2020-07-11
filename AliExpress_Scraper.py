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
        self.description_element = None
        print("-----------------INITIALIZING SCRAPER--------------\n")
        # print(self.ascii_art)
        # ----------Flags--------------
        self.color_flag = False
        self.shipping_flag = False
        self.size_flag = False
        self.description_flag = False
        self.size_color_matrix_flag = False
        self.output_text = "\t---------------------------------------------------------\n"
        # ----------Flags--------------

        # ---------MAKING DIRECTORY---------

        try:
            os.makedirs("Output/TEXT")
        except FileExistsError:
            pass
        try:
            os.makedirs("Output/IMAGES")
        except FileExistsError:
            pass
        # ---------MAKING DIRECTORY---------

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
            finally:
                self.update_basic_information()
            return True
        except DriverExceptions.NoSuchElementException:
            print("THE URL ENTERED IS NOT COMPATIBLE WITH THE PROGRAM\n")
            print("PLEASE ENTER A VALID URL")
            print("ANY ALI-EXPRESS PAGE TO BUY A PRODUCT IS VALID \n")
            return False

    def update_basic_information(self):
        self.information["price"] = self.driver.find_element_by_class_name('product-price-value').text
        self.information["title"] = self.driver.find_element_by_class_name('product-title-text').text
        self.information["store"] = self.driver.find_element_by_class_name('store-name').text
        self.information["images"] = self.driver.find_elements_by_xpath('//div[@class="images-view-item"]/img')
        self.information["qty"] = self.driver.find_element_by_class_name("product-quantity-tip")
        self.information["shipping_info_element"] = self.driver.find_element_by_class_name("product-shipping")

    def get_description(self):
        i = 0
        check = ""
        while i < 5000:
            try:
                self.description_element = self.driver.find_element_by_id("product-description")
                check = self.description_element.text
            except:
                pass
            self.driver.execute_script("window.scrollBy(0, arguments[0]);", i)
            i = i + 10
            if check != "":
                self.description_flag = True
                break

        if self.description_flag:
            self.information["description"] = (re.sub(' +', ' ', self.description_element.text))
        else:
            self.information["description"] = "UNABLE TO EXTRACT DESCRIPTION: NO DESCRIPTION PRESENT"

    def get_variations(self):
        sku_properties = self.driver.find_elements_by_xpath("//div[@class='sku-wrap']/div[@class='sku-property']")
        for key, _ in enumerate(sku_properties):
            xpath2 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/div"
            element = self.driver.find_element_by_xpath(xpath2)
            xpath3 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/ul/li"
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
                    self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                               self.driver.find_element_by_id("root"))
                    ship.click()
                    _ = wait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//span[@class='product-shipping-info black-link']")))
                    time.sleep(1)
                    self.information["shipping_details"].append(
                        ship.text + ":->" + self.information["shipping_info_element"].text)
            elif "Size:" in element.text:
                self.information["size_elements"] = self.driver.find_elements_by_xpath(
                    xpath3 + "[@class='sku-property-item']")
                self.size_flag = True
                self.information["size_details"] = []
                for size in self.information["size_elements"]:
                    self.information["size_details"].append(size.text)
            else:
                print("SAURAV HAS NOT ACCOUNTED FOR FOLLOWING VARIATION")
                print(element.text)
                print("INFORM HIM AND COPY THIS LINK")
        if self.color_flag and self.size_flag:
            self.price_for_size_and_colors()

    def reset_buttons(self,elements):
        for element in elements:
            if "selected" in element.get_attribute("class"):
                element.click()


    def price_for_size_and_colors(self):

        self.size_color_matrix_flag = True
        self.size_color_matrix = np.zeros(
            shape=(len(self.information["color_elements"]), len(self.information["size_elements"])), dtype=object)
        if self.shipping_flag:
            self.information["variation_in_size_and_color"] = np.empty(len(self.information["shipping_elements"]),
                                                                       dtype=object)
        else:
            self.information["variation_in_size_and_color"] = np.empty(1, dtype=object)
        while True:
            if self.shipping_flag:
                try:
                    self.information["shipping_elements"][self.index].click()
                except IndexError:
                    break
            for i, color in enumerate(self.information["color_elements"]):
                self.reset_buttons(self.information["color_elements"])
                if "selected" in self.information["track_color_selection"][i].get_attribute("class"):
                    pass
                else:
                    color.click()
                for j, size in enumerate(self.information["size_elements"]):
                    try:
                        if "disabled" in size.get_attribute("class"): continue
                        size.click()
                        time.sleep(0.2)
                        temp = self.driver.find_element_by_class_name(
                            'product-price-value').text + "||" + re.sub('\spieces available\s', '',
                                                                        self.driver.find_element_by_class_name(
                                                                            "product-quantity-tip").text)
                        self.size_color_matrix[i][j] = temp
                        size.click()


                    except DriverExceptions.NoSuchElementException:
                        print("Size for " + color.get_attribute("title") + "\tUNAVAILABLE")
                        continue
                self.reset_buttons(self.information["size_elements"])
            self.information["variation_in_size_and_color"][self.index] = (self.size_color_matrix.tolist())
            self.index += 1
            if not self.shipping_flag:
                break

    def show_info(self):
        self.get_variations()
        self.get_description()
        f = open("Output/TEXT/" + str(self.information["title"]) + ".txt", "w+")
        f.write("NAME:\t" + self.information["title"] + "\n")
        f.write("STORE:\t" + self.information["store"] + "\n")
        f.write("BASE-PRICE:\t" + self.information["price"] + "\n")
        f.write("\nSHIPPING INFORMATION: \n")
        # if self.size_color_matrix_flag: print(self.information["variation_in_size_and_color"])
        if self.shipping_flag:
            for info in self.information["shipping_details"]:
                f.write("\t" + info.replace('\r', '').replace('\n', '') + "\n")

        else:
            f.write(self.information["shipping_info_element"].text)

        if self.color_flag:
            f.write("\nCOLOR INFORMATION: \n")
            f.write("\tNumber of Different Colors:" + str(len(self.information["color_details"])))
            f.write("\n\tColor Names:\n")
            for color in self.information["color_details"]:
                f.write("\t\t" + color[0])

        if self.size_flag:
            f.write("\n\nSIZE INFORMATION: \n")
            f.write("\tAVAILABLE SIZES: ")
            for info in self.information["size_details"]: f.write(info + " ")

        if self.size_color_matrix_flag:
            f.write("\n\nVARIATION IN PRICES:\n")
            for i, info_list in enumerate(self.information["variation_in_size_and_color"]):
                if self.shipping_flag: f.write(
                    "\t FROM:" + self.information["shipping_details"][i].split(":->")[0] + "\n")
                for j, price in enumerate(info_list):
                    f.write("\t\t FOR COLOR: " + self.information["color_details"][j][0] + "\n")
                    for k, l in enumerate(price):
                        f.write("\t\t\t" + self.information["size_details"][k] + ":" + l.split("||")[0] + " QTY:" +
                                l.split("||")[1] + "\n")
        f.write("\n\n---------DESCRIPTION-----------\n\n")
        f.write(self.information["description"])

    def terminate(self):
        self.driver.quit()


# test = input("Enter URL to scrape : ")
test = "https://www.aliexpress.com/item/4000588993297.html?spm=a2g0o.productlist.0.0.6321e7b8lZ1xNh&algo_pvid=6e318c9b-c868-44d6-b321-78c194ae8f2f&algo_expid=6e318c9b-c868-44d6-b321-78c194ae8f2f-4&btsid=0ab6d69515944368163817904e975f&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
# test = "https://www.aliexpress.com/item/4000411592783.html?spm=a2g0o.productlist.0.0.27eae7b8SJ75f6&s=p&ad_pvid=202007092234373867627591379420003663993_1&algo_pvid=e9dfc962-ad76-406a-82c7-eba6f3c67aa5&algo_expid=e9dfc962-ad76-406a-82c7-eba6f3c67aa5-0&btsid=0ab6fab215943592771575542e867d&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_ "
# test = "https://www.aliexpress.com/item/4000911368854.html?spm=a2g0o.productlist.0.0.6321e7b8lZ1xNh&algo_pvid=6e318c9b-c868-44d6-b321-78c194ae8f2f&algo_expid=6e318c9b-c868-44d6-b321-78c194ae8f2f-0&btsid=0ab6d69515944368163817904e975f&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
scrape = AliExpressScraper()
# scrape.read_url_from_file(test)
if scrape.update_url(test):
    if scrape.load_url():
        scrape.show_info()
        print("-----------THE SCRAPING COMPLETED SUCCESSFULLY----------\n\n")

scrape.terminate()
print("PLEASE CHECK \"Output\" DIRECTORY FOR TEXT FILES ")
