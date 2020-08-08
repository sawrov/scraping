from selenium import webdriver
from selenium.common import exceptions as DriverExceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
import time
import numpy as np
import urllib.request as request
import urllib3.exceptions as UException
from multiprocessing.pool import ThreadPool
import requests.exceptions as RException
from datetime import datetime
from builtins import any as Any
import schedule
import csv
import tkinter as tk
from tkinter.filedialog import askopenfilename


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
            # chrome_options = Options()
            # chrome_options.add_argument("--headless")
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
            quit()

    def start_scraping(self, url):
        try:
            if self.set_url(url):
                if self.load_url():
                    self.show_info()
                    self.start_file_download()
                    self.get_reviews()
                    self.successful_url.write(url + "\n")
                else:
                    print("CAN'T LOAD URL")
            else:
                print("CAN'T SET URL")
        except:
            print("THERE WAS AN ISSUE SCRAPING THE LINK:\n")
            self.unsuccessful_url.write(url + "\n")
            print("THE URL HAS BEEN LOGGED")
            print("THE URL WITH THE PROBLEM IS: \n\n")
            print("---------------------------------------")
            print(url)
            print("---------------------------------------")
            # raise

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
        lists = self.driver.find_elements_by_xpath(
            "//*[@id='nav-global']/div[4]/div/div/div/div[3]/div/ul//li")
        for list in lists:
            if self.currency in list.text:
                list.click()
                print("CURRENCY SET TO: " + str(list.text))
                self.driver.find_element_by_xpath("//*[@id='nav-global']/div[4]/div/div/div/div[4]/button").click()
                return True
        return False

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
                    # self.reset_buttons(self.information["size_elements"])
                    # self.reset_buttons(self.information["color_elements"])
                    self.information["shipping_elements"][self.index].click()
                except IndexError:
                    break
            for i, color in enumerate(self.information["color_elements"]):
                self.reset_buttons(self.information["color_elements"])
                if "selected" in self.information["track_color_selection"][i].get_attribute("class"):
                    pass
                else:
                    try:
                        color.click()
                    except:
                        continue
                for j, size in enumerate(self.information["size_elements"]):
                    try:
                        if "disabled" in size.get_attribute("class"): continue
                        size.click()
                        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                        time.sleep(0.2)
                        temp = self.driver.find_element_by_class_name(
                            'product-price-value').text + "||" + re.sub('\spieces available\s', '',
                                                                        self.driver.find_element_by_class_name(
                                                                            "product-quantity-tip").text)
                        self.size_color_matrix[i][j] = temp
                        size.click()
                        webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

                    except DriverExceptions.NoSuchElementException:
                        print("Size for " + color.get_attribute("title") + "\tUNAVAILABLE")
                        continue
                color.click()

            self.information["variation_in_size_and_color"][self.index] = (self.size_color_matrix.tolist())
            self.index += 1
            if not self.shipping_flag:
                break

    def get_reviews(self):
        # product_detail = self.driver.find_element_by_id("product-detail")
        # self.driver.execute_script("arguments[0].scrollIntoView();", product_detail)
        wait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="product-detail"]/div[1]/div/div[1]/ul/li[2]')))
        rev_tab = self.driver.find_element_by_xpath('//*[@id="product-detail"]/div[1]/div/div[1]/ul/li[2]')
        rev_tab.click()
        link = self.driver.find_element_by_xpath('//*[@id="product-evaluation"]').get_attribute('src')
        self.driver.get(link)
        try:
            wait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'feedback-list-wrap')))
            feedbacks = self.driver.find_elements_by_class_name('feedback-item')
            if (len(feedbacks) > 0):
                Csv = open("Output/" + 'Reviews.csv', 'a+', encoding='utf-8')
                csv_writer = csv.writer(Csv)
                for feedback in feedbacks[:10]:
                    head, _, _ = feedback.text.partition('Helpful?')
                    csv_writer.writerow([str(self.current_url), head])
        except DriverExceptions.TimeoutException:
            print(" NO REVIEWS FOUND")

        # print(reviews)
        # print(len(reviews))
        # for rev in reviews:
        #     print("HERE")
        #     print(rev.text)

    def show_info(self):

        self.get_variations()
        self.get_description()

        try:
            f = open("Output/TEXT/" + str(re.sub(r'[\\/*?:"<>|]', "", str(self.information["title"])))[:50] + ".txt",
                     "w+", encoding='utf-8')
        except:
            f = open("Output/TEXT/" + self.information["title"] + ".txt",
                     "w+", encoding='utf-8')

        f.write(str(("NAME:\t" + self.information["title"] + "\n").encode("utf-8")))
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
                if self.shipping_flag:
                    f.write("\t FROM:" + self.information["shipping_details"][i].split(":->")[0] + "\n")
                    shipping_country = self.information["shipping_details"][i].split(":->")[0]
                    shipping_details = self.information["shipping_details"][i].split(":->")[1]
                else:
                    shipping_country = "N/A"
                    shipping_details = self.information["shipping_info_element"].text
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
                                 csv_size, l.split("||")[0], l.split("||")[1], shipping_country, shipping_details])
                        except AttributeError:
                            f.write("\t\t\t" + self.information["size_details"][k] + ":" + "NA\n")
                            self.writer.writerow(
                                [str(self.current_url), self.information["title"], self.information["store"], csv_color,
                                 csv_size, "NA", "NA", shipping_country, shipping_details])
        else:
            if self.color_flag:
                shipping_country = "N/A"
                shipping_details = self.information["shipping_info_element"].text
                for i, color in enumerate(self.information["color_elements"]):
                    self.reset_buttons(self.information["color_elements"])
                    if "selected" in self.information["track_color_selection"][i].get_attribute("class"):
                        pass
                    else:
                        try:
                            color.click()
                            price = self.driver.find_element_by_class_name(
                                'product-price-value').text
                            qty = re.sub('\spieces available\s', '', self.driver.find_element_by_class_name(
                                "product-quantity-tip").text)
                            self.writer.writerow(
                                [str(self.current_url), self.information["title"], self.information["store"],
                                 color.text,
                                 "NA", price, qty, shipping_country, shipping_details])
                        except:
                            continue

            else:
                self.writer.writerow(
                    [str(self.current_url), self.information["title"], self.information["store"],
                     self.information["price"], self.information["qty"].text])
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
        if self.color_flag:
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
        try:
            self.driver.quit()
        except:
            pass


class AliScraper_GUI:

        def __init__(self):
            self.root = tk.Tk()
            self.root.title("ALI EXPRESS SCRAPER")
            self.root.geometry("550x200")

            self.verification()
            self.currency()
            self.cronjob()
            self.select_file()
            self.scrape_button()

            self.root.mainloop()
            self.verified=False

        def verification(self):
            self.label1 = tk.Label(self.root, text="ENTER THE KEY").grid(row=1, column =0)
            self.key = tk.Entry(self.root)
            self.key.grid(row=1, column=1)
            self.verify_key = tk.Button(self.root, text="VERIFY KEY", command=lambda: self.checkfunc())
            self.verify_key.grid(row=1, column=2)

        def currency(self):
            self.label2 = tk.Label(self.root, text=" SELECT A CURRENCY").grid(row=3,column=0)
            self.currency_file = open("currency_list.txt", "r")
            self.currency_list = self.currency_file.readlines()
            self.currency_list = [i.strip() for i in self.currency_list]
            self.dropdown_var = tk.StringVar(self.root)
            self.dropdown_var.set(self.currency_list[0])
            self.dropdown_currency = tk.OptionMenu(self.root, self.dropdown_var, *self.currency_list).grid(row=3,column=1)

        def cronjob(self):
            self.label3 = tk.Label(self.root, text="SCHEDULE A REFRESH").grid(row=4,column=0)
            days = [str(day) + " day" for day in list(range(0,30))]
            time = [str(hr) + " hrs" for hr in list(range(0,24))]
            self.dropdown_day = tk.StringVar(self.root)
            self.dropdown_day.set(days[0])
            self.dropdown_time = tk.StringVar(self.root)
            self.dropdown_time.set(time[0])

            self.dropdown_day_item = tk.OptionMenu(self.root, self.dropdown_day, *days).grid(row=4,column=3,columnspan=1)
            self.dropdown_time_item = tk.OptionMenu(self.root, self.dropdown_time, *time).grid(row=4,column=2,columnspan=1)

            self.cron_check = tk.IntVar()
            C1 = tk.Checkbutton(self.root, text="YES", variable=self.cron_check, onvalue=1, offvalue=0).grid(row=4, column=1)

        def select_file(self):
            self.label4 = tk.Label(self.root, text="The program looks in aliexpressurl.txt by default")
            self.label4.grid(row=5, column=1)
            self.select_file = tk.Button(self.root, text="LOAD URL FROM FILE", command=lambda: self.selectfile()).grid(row=6, column=1)


        def scrape_button(self):
            start_scraping = tk.Button(self.root, text="START SCRAPING", command=lambda: self.main())
            start_scraping.config(state=tk.DISABLED)
            start_scraping.grid(row=7, column=1)

        def checkfunc(self):
            if self.verify(self.key.get()):
                self.verified=True
                print("VERIFIED")
                self.verify_key.configure(state=tk.DISABLED)
                self.key.configure(state=tk.DISABLED)
                self.start_scraping.config(state=tk.ENABLED)

            else:
                self.verified=False
                print("NOT VERIFIED")

        def selectfile(self):
            self.label4.config(text=askopenfilename())

        def verify(self,key):
            try:
                key = key.lower()
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
            except IndexError:
                return False

        def main(self):
            try:
                f = open("debug.txt", "a+")
            except FileNotFoundError:
                print("file not present")
            folder_name = str(datetime.now().strftime("%b %d %Y %H-%M"))
            # csv file open
            Csv = open("Output/" + 'Mother.csv', 'a+', encoding='utf-8')
            csv_writer = csv.writer(Csv)
            load_url=self.label4["text"]
            if not os.path.exists(load_url):
                load_url="aliexpressurl.txt"
                print("DEFAULT PATH USED")

            with open(load_url) as links:
                urls = links.readlines()
                for url in urls:
                    try:
                        print("TESTING URL: " + url)
                        currency = self.dropdown_var.get()
                        currency=currency.split(":")[0]
                        print(currency)
                        scrape = AliExpressScraper(folder_name, csv_writer, currency)
                        scrape.start_scraping(url)
                        scrape.close_session()

                    except KeyboardInterrupt:
                        try:
                            scrape.driver.close()
                        except UException.MaxRetryError:
                            pass
                        print("YOU QUIT THE PROGRAM")
                        quit()
                    # except DriverExceptions.
            print("PLEASE CHECK \"Output\" DIRECTORY FOR TEXT FILES ")

# cron job in here on main function
if __name__ == "__main__":
    _=AliScraper_GUI()

    # if validate_user():
    # main(curr)
    # schedule.every(10).minutes.do(main)
    # while True:
    #     schedule.run_pending()
