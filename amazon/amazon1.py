from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def scrape(url):
# url = "https://www.aliexpress.com/item/4000904854907.html?spm=2114.best.6.2.4da90o1v0o1vjP&scm=1007.17258.148196.0&pvid=eafaf190-7bab-48ca-bfc4-847e043f026a"
# -------------HouseKeeping-----------
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1024)

# -------------HouseKeeping-----------

    driver.get(url)


# exif data image clean code
# exif code here
# exif = image clean



#PROUCT_PRICE_set RULE

#       price = driver.find_element_by_xpath('//SPAN[@id="priceblock_ourprice"]')
#       print("PRICE: " + price.text)
#       PRODUCT_PRICE _SET _RULE = "$ &/or %"  (SET UP TXT. INPUT $Or% Or both $+%)
#       price = product_price
#       print = price + product_price_set_rule = "product_price"



#SHIP_PRICE_set RULE

#       ship = driver.find_element_by_id("fast-track-message")
#       print ("SHIP: "+ship.text)
#       SHIP_PRICE _SET _RULE = "$ &/or %"  (SET UP TXT. INPUT $Or% Or both $+%)
#       price = product_price
#       price + ship_price_set_rule = "ship_price"
#set up a txt.file  for  (SET UP TXT. INPUT $Or% Or both $+%)

#cron job to update every min/hour/day/week
#set up a txt.file to update as you select min/hour/day/week/


    title = driver.find_element_by_id('productTitle')
    print("TITLE: " + title.text)

    currency = driver.find_element_by_xpath('//*[@id="cerberus-data-metrics"]')
    print("CURRENCY:  " + currency.get_attribute("data-asin-currency-code"))

    price = driver.find_element_by_xpath('//SPAN[@id="priceblock_ourprice"]')
    print("PRICE: " + price.text)

    description = driver.find_element_by_id("productDescription")
    print ("DESCRIPTION: "+ description.text)

    Item_specifics = driver.find_element_by_id("detailBullets")
    print ("ITEM_SPECIFICS:  " +Item_specifics.text)

    ship = driver.find_element_by_id("fast-track-message")
    print ("SHIP: "+ship.text)

#******WORK IN PROGRESS****** (need to find for all countries not just one) this grabs a note availibility dont loose it use it.
    ship_to = driver.find_element_by_xpath('//*[@id="contextualIngressPtLabel_deliveryShortLine"]/span[2]')
    print("SHIP_TO:"+ship_to.text)

    availability = driver.find_element_by_id("availability")
    print("AVAILABILITY:   "+availability.text)

#******WORK IN PROGRESS******

#-----------------------------GET ALL COLOR SIZE PRICE IMAGES ------------------------

    size_button = driver.find_element_by_xpath('//*[@id="dropdown_selected_size_name"]/span').click()

    sizes = driver.find_elements_by_xpath("//ul[@class='a-nostyle a-list-link']/li/a[@class='a-dropdown-link']")

    colors = driver.find_elements_by_xpath("//ul[@role='radiogroup']//img")


#if size_flag == 1 and color_flag == 1:
    for color in colors:
        color.click()
    for size in sizes:
                size.click()
                time.sleep(0.5)
                print(color.get_attribute("alt") + "--" + size.text + "\t" + ":" + driver.find_element_by_xpath(
                "//ul[@class='a-nostyle a-list-link']/li/a[@class='a-dropdown-link']").text+"--->"+driver.find_element_by_id("availability"))




#-----------------------------GET ALL shipping VARIATIONS ------------------------


#    AllSHIPCountries = driver.find_element_by_id("contextualIngressPtLabel_deliveryShortLine").click()
#    SHIPCountries = driver.find_elements_by_id("GLUXCountryList")
#    SHIPCountries = driver.find_elements_by_class_name('a-dropdown-link')

#    for AllSHIPCountries in SHIPCountries:
#    print(AllSHIPCountries.get_attribute("  a-popover-wrapper "))
# find attribute for ship all countries path works to attribute but cant find attribute/work in progress/


#******FINISHED SCRIPT********

    driver.quit()




#SIZE COLOR WORKING

#size_button = driver.find_element_by_xpath('//*[@id="dropdown_selected_size_name"]/span').click()

#sizes = driver.find_elements_by_xpath("//ul[@class='a-nostyle a-list-link']/li/a[@class='a-dropdown-link']")

#colors = driver.find_elements_by_xpath("//ul[@role='radiogroup']//img")

#    for size in sizes:
#        print(size.text + "\t")

#    for color in colors:
#        print(color.get_attribute('alt'))

# GET ALL VARIATIONS IN SIZE AND COLORS------------------------

#SIZE COLOR WORKING



# ----------Read-from-text-file------------

try:
    with open("amazonurl.txt") as links:
        urls = links.readlines()
        for url in urls:
            scrape(url)
except:
    print("\n\n\n\n")
    print("MAKE SURE THE FILE NAME IS amazonurl.txt")
    print("MAKE SURE IT IS IN THE SAME DIRECTORY")
    print("CHECK THE URL ENTERED")

quit()

# ----------Read-from-text-file------------
