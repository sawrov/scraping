from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.aliexpress.com/item/4000970644013.html?spm=a2g0o.productlist.0.0.73b9753eiOZcbh&algo_pvid=d0bdb248-24cd-434f-af4d-fb4d49b6f651&algo_expid=d0bdb248-24cd-434f-af4d-fb4d49b6f651-10&btsid=0ab6d69f15919610188667793e70a0&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
# url="https://www.aliexpress.com/item/4000970644013.html?spm=a2g0o.productlist.0.0.73b9753eiOZcbh&algo_pvid=d0bdb248-24cd-434f-af4d-fb4d49b6f651&algo_expid=d0bdb248-24cd-434f-af4d-fb4d49b6f651-10&btsid=0ab6d69f15919610188667793e70a0&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_"
# url="https://www.aliexpress.com/item/4000103365480.html?spm=a2g01.12617084.fdpcl001.1.2d54jCb7jCb7mn&gps-id=5547572&scm=1007.19201.130907.0&scm_id=1007.19201.130907.0&scm-url=1007.19201.130907.0&pvid=a934229c-22a1-4e1e-8b3f-901c2b5ae23f";

# -------------HouseKeeping-----------
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1024)
driver.get(url)
# -------------HouseKeeping-----------

price = driver.find_element_by_class_name('product-price-value')
title = driver.find_element_by_class_name('product-title-text')
store = driver.find_element_by_class_name('store-name')
images = driver.find_elements_by_xpath('//div[@class="images-view-item"]/img')
list_of_sku = driver.find_elements_by_class_name('sku-property')
list_of_pictures = []
# --------------To close the POP-UPBOX---------------
try:
    wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-dialog-body")))
except:
    print("No POPUP Detected")
driver.find_element_by_class_name("next-dialog-close").click()
# --------------To close the POP-UPBOX---------------


# folder Creation to download pictures.
# dir_for_images = 'Downloaded_Images/' + store.text + "/"
# os.makedirs(os.path.dirname(dir_for_images), exist_ok=True)


print("-------------------OUTPUT-------------------")
print("Price: " + price.text)
print("TITLE: " + title.text)
print("SELLER: " + store.text)
no_of_item = 0

for items in images:
    links = (items.get_attribute('src'))
    links = links.replace(".jpg_50x50", "")
    # urllib.request.urlretrieve(links, dir_for_images + str(no_of_item))
    # saving this is an array.
    list_of_pictures.append(links)
    no_of_item += 1

# Clear Exif Data HERE
# or filename in os.listdir(dir_for_images):
# print(filename)
# will clear exif data
# print(list_of_pictures)
# while sku:

# -------------CODE BLOCK TO GET VARIATIONS-----------------------
print(
    driver.find_element_by_xpath("//div[@class='sku-wrap']/div[@class='sku-property'][1]/ul/li/div/img").get_attribute(
        "src"))
sku_properties = driver.find_elements_by_xpath("//div[@class='sku-wrap']/div[@class='sku-property']")
property_values = dict()
for key, _ in enumerate(sku_properties):
    xpath2 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/div"
    element = driver.find_element_by_xpath(xpath2)
    print(element.text)
    # use try in here later
    xpath3 = "//div[@class='sku-wrap']/div[@class='sku-property'][" + str(key + 1) + "]/ul/li"
    if element.text == "Color:":
        colors = driver.find_elements_by_xpath(xpath3 + "/div/img")
        for index, color in enumerate(colors):
            src = str(index) + ":" + color.get_attribute("src")
            property_values.setdefault(element.text, []).append(src)

    elif element.text == "Ships From:":
        shipping = driver.find_elements_by_xpath(xpath3)
        for ship in shipping:
            driver.execute_script("arguments[0].scrollIntoView(true);", ship)
            print(ship.text)
            ship.click()
            elm = wait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='product-shipping-info black-link']")))
            shipping_info = driver.find_element_by_class_name("product-shipping").text
            print(shipping_info)
            property_values.setdefault(element.text, [ship.text]).append(shipping_info)

for check in property_values:

    print(check)
    print('-----------')

    for values in property_values[check]:
        print(values)
print("\n\n\n\n")
# print(driver.find_element_by_id("product-description").text)
# print(items.get_attribute("src"))
# Code for except block
# print(sys.exc_info()[0])
driver.quit()
