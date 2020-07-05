from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
import time
import numpy as np
import urllib.request
from multiprocessing.pool import ThreadPool


def download_files(Path):
    # regular expression to get the name of the file.
    imagePath = Path[1]
    reg = r'^(.*[\\\/])'
    location = "DOWNLOADED_IMAGES\\" + str(Path[0]) + re.sub(reg, "", imagePath)
    urllib.request.urlretrieve(imagePath, location)
    return location


def scrape(url):
    # -------------HouseKeeping-----------

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1024)

    # -------------HouseKeeping-----------

    driver.get(url)

    price = driver.find_element_by_class_name('product-price-value')
    title = driver.find_element_by_class_name('product-title-text')
    store = driver.find_element_by_class_name('store-name')
    images = driver.find_elements_by_xpath('//div[@class="images-view-item"]/img')
    qty = driver.find_element_by_class_name("product-quantity-tip")
    list_of_sku = driver.find_elements_by_class_name('sku-property')
    list_of_pictures = []
    # --------------To close the POP-UPBOX---------------
    try:
        wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-dialog-body")))
        driver.find_element_by_class_name("next-dialog-close").click()
    except:
        print("No POPUP Detected")
    # --------------To close the POP-UPBOX---------------

    # ----------Defining Flags-------------
    color_flag = 0
    shipping_flag = 0
    size_flag = 0
    description_flag = 0
    # -----------Defining Flags------------

    print("-------------------INFORMATION-------------------")
    print("Price: " + price.text + "\n")
    print("TITLE: " + title.text + "\n")
    print("SELLER: " + store.text + "\n")
    print("QUANTITY: " + qty.text + "\n")

    print("-------IMAGES-----------")
    for items in images:
        links = (items.get_attribute('src'))
        links = links.replace(".jpg_50x50", "")
        list_of_pictures.append(links)

    # Clear Exif Data HERE
    print("-------END-IMAGES-----------")

    print("------------VARIATIONS-------------")

    # -------------CODE BLOCK TO GET VARIATIONS-----------------------

    sku_properties = driver.find_elements_by_xpath("//div[@class='sku-wrap']/div[@class='sku-property']")
    property_values = dict()
    colors = []
    sizes = []
    for key, _ in enumerate(sku_properties):
        xpath2 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/div"
        element = driver.find_element_by_xpath(xpath2)
        # use try in here later
        xpath3 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/ul/li"
        if element.text == "Color:":
            color_flag = 1
            colors = driver.find_elements_by_xpath(xpath3 + "/div/img")
            for index, color in enumerate(colors):
                title = color.get_attribute("title")
                src = color.get_attribute("title") + ":" + color.get_attribute("src")
                property_values.setdefault(element.text, []).append(title)

        elif element.text == "Ships From:":
            shipping_flag = 1
            shipping = driver.find_elements_by_xpath(xpath3)
            for ship in shipping:
                driver.execute_script("arguments[0].scrollIntoView(true);", ship)
                ship.click()
                elm = wait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@class='product-shipping-info black-link']")))
                time.sleep(1)
                shipping_info = driver.find_element_by_class_name("product-shipping").text
                property_values.setdefault(element.text, [ship.text]).append(shipping_info)
        elif element.text == "Size:":
            sizes = driver.find_elements_by_xpath(xpath3)
            size_flag = 1
            for size in sizes:
                property_values.setdefault(element.text, []).append(size.text)

    # -------------------------DOWNLOAD FILES AND CLEAR EXIF-------------------------------

    try:
        os.makedirs("DOWNLOADED_IMAGES")
    except FileExistsError:
        pass
    results = ThreadPool(5).imap_unordered(download_files, enumerate(list_of_pictures))
    # test=map(download_files, list_of_pictures)
    for result in results:
        print(result)
    quit()
    # -------------------------DOWNLOAD FILES AND CLEAR EXIF-------------------------------

    # GET ALL VARIATIONS IN SIZE AND COLORS------------------------
    size_color_matrix = np.zeros(shape=(len(colors), len(sizes)), dtype=object)
    if size_flag == 1 and color_flag == 1:
        for i, color in enumerate(colors):
            color.click()
            for j, size in enumerate(sizes):
                try:
                    size.click()
                    time.sleep(0.1)
                    # print(driver.find_element_by_class_name('product-price-value').text)
                    size_color_matrix[i][j] = driver.find_element_by_class_name(
                        'product-price-value').text + "(" + re.sub('\spieces available\s', '',
                                                                   driver.find_element_by_class_name(
                                                                       "product-quantity-tip").text) + ")"
                # print(color.get_attribute("title") + "--" + size.text + ":" + driver.find_element_by_class_name(
                #     'product-price-value').text + "--->" + driver.find_element_by_class_name(
                #     "product-quantity-tip").text)
                except:
                    continue
        print(size_color_matrix)

    #  GET ALL VARIATION IN SIZE AND COLORS------------------
    # Displaying all the information
    for check in property_values:
        print(check)
        print('-----------')
        for values in property_values[check]:
            print(values)
        print("\n")
        print("---------------")
    if shipping_flag == 0:
        print("\nSHIPPING INFO")
        print(driver.find_element_by_class_name("product-shipping").text)

    print("---------------DESCRIPTION------------------")
    i = 200
    description = ""
    check = ""
    while i < 5000:
        try:
            description = driver.find_element_by_id("product-description")
            check = description.text
        except:
            pass
        driver.execute_script("window.scrollBy(0, arguments[0]);", i)
        i = i + 10
        if check != "":
            description_flag = 1
            break

    if description_flag == 1:
        print(re.sub(' +', ' ', description.text))
    else:
        print("UNABLE TO EXTRACT DESCRIPTION:: WORKING ON IT. PLEASE REPORT THIS LINK TO YOUR PROVIDER")

    print("---------------END OF DESCRIPTION------------------")
    print("---------------IMAGES IN DESCRIPTION------------------")

    try:
        desc_img = driver.find_elements_by_class_name("desimg")
        for img in desc_img:
            print(img.get_attribute("src"))
    except:
        print("NO IMAGES FOUND IN DESCRIPTION")
    print("---------------END IMAGES IN DESCRIPTION------------------")

    driver.quit()


# ----------Read-from-text-file------------
with open("aliexpressurl.txt") as links:
    urls = links.readlines()
    for url in urls:
        scrape(url)

#
# try:
#     with open("aliexpressurl.txt") as links:
#         urls = links.readlines()
#         for url in urls:
#             scrape(url)
# except:
#     print("\n\n\n\n")
#     print("MAKE SURE THE FILE NAME IS aliexpressurl.txt")
#     print("MAKE SURE IT IS IN THE SAME DIRECTORY")
#     print("CHECK THE URL ENTERED")
quit()

# ----------Read-from-text-file------------
