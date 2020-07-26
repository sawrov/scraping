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
from datetime import datetime
from builtins import any as Any
import schedule
import csv


class AliExpressScraper:
    current_url = ""
    information = {}
    links_for_color = []

    # ----------Flags--------------
    # ----------Flags--------------

    def __init__(self, folder_name, csv_writer, currency):
        print("-----------------INITIALIZING SCRAPER--------------\n")

        # -------initializing variables-----------------
        self.index = 0;
        self.description_element = None
        self.download_location = ""
        self.currency = currency

        # ----------Declaring Flags--------------
        self.color_flag = False
        self.shipping_flag = False
        self.size_flag = False
        self.description_flag = False
        self.size_color_matrix_flag = False
        self.description_img_flag = False
        # self.files_to_download_present = False
        # ----------Flags--------------
        self.writer = csv_writer
        # ---------MAKING DIRECTORY---------
        self.log_dir = "Output/LOGS/" + folder_name

        try:
            os.makedirs("Output/TEXT")
        except FileExistsError:
            pass
        try:
            os.makedirs("Output/IMAGES")
        except FileExistsError:
            pass
        try:
            os.makedirs(self.log_dir)
        except FileExistsError:
            pass
        # ---------MAKING DIRECTORY---------

        # ---------OPENING FILES -----------

        self.successful_url = open(self.log_dir + "/Successful_url.txt", "a+")
        self.unsuccessful_url = open(self.log_dir + "/Unsuccessful.txt", "a+")
        self.variation_url = open(self.log_dir + "/New_variation_url.txt", "a+")

        # ---------OPENING FILES -----------

        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(1920, 1024)
        except RException.ConnectionError:
            print("\n--PLEASE CHECK YOUR INTERNET CONNECTION--")
            quit()
        except DriverExceptions.InvalidSessionIdException:
            print("\nBROWSER CLOSED UNEXPECTEDLY:.....")
            quit()

        except DriverExceptions.SessionNotCreatedException:
            print("\nBROWSER CLOSED BEFORE SESSION WAS CREATED")
            exit()

    def start_scraping(self, url):
        try:
            if self.set_url(url):
                if self.load_url():
                    self.show_info()
                    self.start_file_download()
                    self.successful_url.write(url + "\n")
                else:
                    print("CAN'T LOAD URL")
            else:
                print("CAN'T SET URL")
        except:
            print("THERE WAS AN ISSUE SCRAPING THE LINK:\n")
            self.unsuccessful_url.write(url + "\n")
            print("THE URL HAS BEEN LOGGED")
            raise

    def setcurrency(self):

        q1_a = wait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-role='region-pannel']")))
        q2_b = wait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-role='region-pannel']")))
        time.sleep(3)
        region = self.driver.find_element_by_xpath("//div[@data-role='region-pannel']")
        # print (region)
        # print(region.text)
        region.click()
        q1_a = wait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='nav-global']/div[4]/div/div/div/div[3]/div/span")))
        currency_list = self.driver.find_element_by_xpath("//*[@id='nav-global']/div[4]/div/div/div/div[3]/div/span")
        currency_list.click()
        # selected_curr=self.driver.find_element_by_xpath("//*[@id='nav-global']/div[4]/div/div/div/div[3]/div/div/input").send_keys("USD")
        lists=self.driver.find_elements_by_xpath(
            "//*[@id='nav-global']/div[4]/div/div/div/div[3]/div/ul//li")
        print(len(lists))
        for list in lists:
            if self.currency in list.text:
                list.click()
                self.driver.find_element_by_xpath("//*[@id='nav-global']/div[4]/div/div/div/div[4]/button").click()
                return True
        return False
        # key = self.driver.find_element_by_xpath(
        #     "//*[@id='nav-global']/div[4]/div/div/div/div[3]/div/ul//li/a[text()='USD']")
        # print(key.text)
        # key.click()
        # print(len(currency_list))
        # print(currency)
        # currency.click()

    def close_session(self):
        self.terminate()
        self.successful_url.close()
        self.unsuccessful_url.close()
        self.variation_url.close()

    def set_url(self, url):
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

    def download_files(self, Path):
        # regular expression to get the name of the file.
        download_url = Path[1]
        reg = r'^(.*[\\\/])'
        filename = re.sub(reg, "", download_url)
        full_path = self.download_location + "/" + str(Path[0]) + filename
        try:
            if os.path.isfile(full_path):
                pass
            else:
                request.urlretrieve(download_url, full_path)
            return True
        except:
            return False

    def load_url(self):
        try:
            self.driver.get(self.current_url)
            _ = self.driver.find_element_by_xpath('//*[@id="root"]')
            try:
                wait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "next-dialog-close")))
                self.driver.find_element_by_class_name("next-dialog-close").click()
                if self.setcurrency():
                    wait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "next-dialog-close")))
                    self.driver.find_element_by_class_name("next-dialog-close").click()
            except DriverExceptions.NoSuchElementException:
                print("No POP-UP Detected")
                pass
            except DriverExceptions.TimeoutException:
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
        while i < 2000:
            try:
                self.description_element = self.driver.find_element_by_id("product-description")
                check = self.description_element.text
            except DriverExceptions.NoSuchElementException:
                pass
            self.driver.execute_script("window.scrollBy(0, arguments[0]);", i)
            i = i + 100
            time.sleep(2)
            if check != "":
                self.description_flag = True
                break

        try:
            self.information["description_img"] = self.driver.find_elements_by_xpath(
                "//div[@id='product-description']//img")
            self.description_img_flag = True
        except DriverExceptions.NoSuchElementException:
            pass

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
                print("\nNEW VARIATION DETECTED: URL NOTED")
                self.variation_url.write(element.text + ":" + self.current_url + "\n")
        if self.color_flag and self.size_flag:
            self.price_for_size_and_colors()

    @staticmethod
    def reset_buttons(elements):
        for element in elements:
            if "selected" in element.get_attribute("class"):
                element.click()

    def price_for_size_and_colors(self):
        split_thin_line = self.driver.find_element_by_class_name("split-line-thin")
        self.driver.execute_script("arguments[0].scrollIntoView();", split_thin_line)

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
                    csv_color = self.information["color_details"][j][0]
                    for k, l in enumerate(price):
                        try:
                            csv_size = self.information["size_details"][k]
                            f.write("\t\t\t" + self.information["size_details"][k] + ":" + l.split("||")[0] + " QTY:" +
                                    l.split("||")[1] + "\n")
                            self.writer.writerow(
                                [str(self.current_url), self.information["title"], self.information["store"], csv_color,
                                 csv_size, l.split("||")[0], l.split("||")[1]])
                        except AttributeError:
                            f.write("\t\t\t" + self.information["size_details"][k] + ":" + "NA\n")
                            self.writer.writerow(
                                [str(self.current_url), self.information["title"], self.information["store"], csv_color,
                                 csv_size, "NA", "NA"])
        f.write("\n\n---------DESCRIPTION-----------\n\n")
        f.write(self.information["description"])

    def start_file_download(self):
        print("DOWNLOADING IMAGES")
        # ("---------------images------------------")
        loc = "Output/IMAGES/" + self.information["store"] + "/images"
        try:
            os.makedirs(loc)
        except FileExistsError:
            pass
        self.download_location = loc
        list_of_images = []
        for img_elm in self.information["images"]:
            list_of_images.append(img_elm.get_attribute("src").replace(".jpg_50x50", ""))
        results = ThreadPool(5).imap_unordered(self.download_files, enumerate(list_of_images))
        for result in results:
            if result:
                pass
            else:
                print("IMAGE NOT DOWNLOADED")
        # ("---------------images------------------")

        # ("---------------colors------------------")
        loc = "Output/IMAGES/" + self.information["store"] + "/color"
        try:
            os.makedirs(loc)
        except FileExistsError:
            pass
        self.download_location = loc
        list_of_images = []
        for img_elm in self.information["color_details"]:
            list_of_images.append(img_elm[1].replace(".jpg_50x50", ""))
        results = ThreadPool(5).imap_unordered(self.download_files, enumerate(list_of_images))
        for result in results:
            if result:
                pass
        # ("---------------colors------------------")

        # ("---------------images in desc--------------------")
        list_of_images = []
        if self.description_img_flag:
            loc = "Output/IMAGES/" + self.information["store"] + "/description"
            try:
                os.makedirs(loc)
            except FileExistsError:
                pass
            self.download_location = loc
            for img in self.information["description_img"]:
                list_of_images.append(img.get_attribute("src").replace(".jpg_120x120", ""))
            results = ThreadPool(5).imap_unordered(self.download_files, enumerate(list_of_images))
            for result in results:
                if result:
                    pass
            print("SCRAPING SUCCESSFULLY COMPLETED: " + self.current_url)

    def terminate(self):
        self.driver.quit()


# test = "https://www.aliexpress.com/item/4000607551628.html?spm=2114.12010610.8148356.43.564e4db0e12tqe"
# test = "https://www.aliexpress.com/item/32949506271.html?spm=a2g0o.productlist.0.0.3888e7b879Rcun&s=p&ad_pvid=202007052216005954785301924050015873321_1&algo_pvid=f893b3df-c6b9-4ebe-9a0a-8b6e8fadcd06&algo_expid=f893b3df-c6b9-4ebe-9"
# test = "https://www.aliexpress.com/item/4001051026485.html?spm=a2g0o.productlist.0.0.7df5ccb2zZiTEB&s=p&ad_pvid=202007052248174590920487854410017043611_3&algo_pvid=2cb4a5ce-b886-4f04-95cd-9123a0bf902f&algo_expid=2cb4a5ce-b886-4f04-95cd-9123a0bf902f-2&btsid=0be3743615940144978691860e8c10&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
# test = "https://www.aliexpress.com/item/4000411592783.html?spm=a2g0o.productlist.0.0.27eae7b8SJ75f6&s=p&ad_pvid=202007092234373867627591379420003663993_1&algo_pvid=e9dfc962-ad76-406a-82c7-eba6f3c67aa5&algo_expid=e9dfc962-ad76-406a-82c7-eba6f3c67aa5-0&btsid=0ab6fab215943592771575542e867d&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_ "
# test = "https://www.aliexpress.com/item/4000911368854.html?spm=a2g0o.productlist.0.0.6321e7b8lZ1xNh&algo_pvid=6e318c9b-c868-44d6-b321-78c194ae8f2f&algo_expid=6e318c9b-c868-44d6-b321-78c194ae8f2f-0&btsid=0ab6d69515944368163817904e975f&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
# scrape.start_scraping(test)

def main(currency):
    # print("COOL")
    try:
        f = open("debug.txt", "a+")
    except FileNotFoundError:
        print("file not present")
    folder_name = str(datetime.now().strftime("%b %d %Y %H-%M"))
    # csv file open
    Csv = open("Output/" + str(folder_name) + 'output.csv', 'w')
    csv_writer = csv.writer(Csv)
    with open("aliexpressurl.txt") as links:
        urls = links.readlines()
        for url in urls:
            try:
                print("TESTING URL: " + url)
                scrape = AliExpressScraper(folder_name, csv_writer, currency)
                scrape.start_scraping(url)
                scrape.close_session()

            except KeyboardInterrupt:
                print("YOU QUIT THE PROGRAM")
                quit()
            # except DriverExceptions.
    print("PLEASE CHECK \"Output\" DIRECTORY FOR TEXT FILES ")


def verify(key):
    print(key)
    score = 0
    check_digit = key[2]
    check_digit_count = 0
    chunks = key.split('-')
    for chunk in chunks:
        if len(chunk) != 4:
            return False
        for char in chunk:
            if char == check_digit:
                check_digit_count += 1
            score += ord(char)
    if score == 1672 and check_digit_count == 5:
        return True
    return False


def validate_user():
    while True:
        key = input("PLEASE ENTER A VALID KEY TO RUN THE PROGRAM:  ")
        try:
            if verify(key.lower()):
                print("KEY VALID:")
                return True
            else:
                print("INVALID KEY, PLEASE ENTER A VALID KEY TO RUN THE PROGRAM\n")
        except IndexError:
            print("PLEASE ENTER A VALID KEY\n")


# cron job in here on main function
if __name__ == "__main__":
    currency_file = open("currency_list.txt", "r")
    currency_list=currency_file.readlines()
    print ("\n".join(currency_list))
    curr = input("CHOOSE THE CURRENCY FROM THE LIST ABOVE \n FOR EG: ENTER AUD FOR AUSTRALIAN DOLLAR: ")
    if Any(curr.upper() in x for x in currency_list):
        print("VALID KEYWORD")
    else:
        print(" INVALID CURRENCY DEFAULT CURRENCY (USD) IS USED")
        curr="USD"
    # if validate_user():
    main(curr)
    # schedule.every(10).minutes.do(main)
    # while True:
    #     schedule.run_pending()
