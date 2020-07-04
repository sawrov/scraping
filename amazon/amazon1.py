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

    
#******WORK IN PROGRESS****************************************************************************************
# exif data image clean code
# exif code here
# exif = image clean


#******WORK IN PROGRESS****************************************************************************************
#PROUCT_PRICE_set RULE

    #       product_price = driver.find_element_by_xpath('//SPAN[@id="priceblock_ourprice"]')
    #       print("PRODUCTPRICE: " + product_price.text)
    #       PRODUCT_PRICE_SET_RULE = product_price + "$ &/or %"  (SET UP TXT. INPUT $Or% Or both $+%)*******************************
    #       print(PRODUCT_PRICE _SET _RULE:   "+PRODUCT_PRICE _SET _RULE.text
    

    
#******WORK IN PROGRESS****************************************************************************************
#SHIP_PRICE_set RULE

    #       ship_to = driver.find_element_by_xpath('//*[@id="contextualIngressPtLabel_deliveryShortLine"]/span[2]')
    #       print("SHIP_TO:"+ship_to.text)  (must get ship price not ship country this only example.....)***************************
    #       SHIP_PRICE_SET_RULE = ship_price + "$ &/or %"  (SET UP TXT. INPUT $Or% Or both $+%)*************************************
    #       print"SHIP_PRICE_SET_RULE:   "+SHIP_PRICE _SET _RULE.text
    


#cron job to update every min/hour/day/week #******WORK IN PROGRESS****************************************************************************************
    #set up a txt.file to update as you select min/hour/day/week/   
    #create cron job to run

#images from product page*****************************************************************
    
    title = driver.find_element_by_id('productTitle')
    print("TITLE: " + title.text)

    currency = driver.find_element_by_xpath('//*[@id="cerberus-data-metrics"]')
    print("CURRENCY:  " + currency.get_attribute("data-asin-currency-code"))

    product_price = driver.find_element_by_xpath('//SPAN[@id="priceblock_ourprice"]')
    print("PRODUCTPRICE: " + product_price.text)
    
#******WORK IN PROGRESS****************************************************************************************
    #ship_price =    this is used for ship price set rule

    #short_description = driver.find_element_by_id("productDescription")
    #print ("DESCRIPTION: "+ description.text)

#******WORK IN PROGRESS****************************************************************************************
    #full_decripton = driver
    print (info attribute full description)

    Item_specifics = driver.find_element_by_id("detailBullets")
    print ("ITEM_SPECIFICS:  " +Item_specifics.text)

    ship = driver.find_element_by_id("fast-track-message")
    print ("SHIP: "+ship.text)

#******WORK IN PROGRESS****** (need to find for all countries not just one) this grabs a note availibility dont loose it use it.**************************************************
    ship_to = driver.find_element_by_xpath('//*[@id="contextualIngressPtLabel_deliveryShortLine"]/span[2]')
    print("SHIP_TO:"+ship_to.text)

#******WORK IN PROGRESS******
    availability = driver.find_element_by_ID("availability")*********************************************************************8
    print("Availability:   "+availability.text)

#******WORK IN PROGRESS******      ****************************************************************************************************************************
    size_button = driver.find_element_by_xpath('//*[@id="dropdown_selected_size_name"]/span').click()

    sizes = driver.find_elements_by_xpath("//ul[@class='a-nostyle a-list-link']/li/a[@class='a-dropdown-link']")

    colors = driver.find_elements_by_xpath("//ul[@role='radiogroup']//img")


    # GET ALL VARIATIONS IN SIZE AND COLORS------------------------i had it working i fucked it up and cant retrieve my work*********************************need start over***

    #if size_flag == 1 and color_flag == 1:
    for color in colors:
        color.click()
    for size in sizes:
                size.click()
                time.sleep(0.5)
                print(color.get_attribute("alt") + "--" + size.text + ":" + driver.find_element_by_xpath(
                "//ul[@class='a-nostyle a-list-link']/li/a[@class='a-dropdown-link']").text+"--->"+driver.find_element_by_id("availability"))

    # find attribute for ship all countries path works to attribute but cant find attribute/work in progress/********************************************attribute issue why?**

    AllSHIPCountries = driver.find_element_by_id("contextualIngressPtLabel_deliveryShortLine").click()
    # SHIPCountries = driver.find_elements_by_id("GLUXCountryList")
    SHIPCountries = driver.find_elements_by_class_name('a-dropdown-link')

    for AllSHIPCountries in SHIPCountries:
        print(AllSHIPCountries.get_attribute("   "))  ####Find Attribute####





    driver.quit()







                #******WORK IN PROGRESS******






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




#**********BELLOW IS CODE AND NOTES (WORKING ON IT)


#AllSHIPCountries = driver.find_element_by_id("contextualIngressPtLabel_deliveryShortLine").click()
#SHIPCountries = driver.find_elements_by_id("GLUXCountryList")
#SHIPCountries = driver.find_elements_by_class_name('a-dropdown-link')
#SHIPCountries = driver.find_element_by_xpath()
#SHIPCountries = driver.find_elements_by_class_name('a-dropdown-item')
#SHIPCountries = driver.find_element_by_xpath('//a[@class="a-dropdown-link"]')

#print ("SHIPCOUNTRIES:   "+SHIPCountries + '\t')

#for ALLSHIPCountries in SHIPCountries:
#print (ALLSHIPCountries.get_attribute('/a'))


#/a    /id/class/a/li/span
#//a[@class="a-dropdown-link"]      xpath all countries
#SHIPCountries = driver.find_elements_by_class_name('a-dropdown-item')
#SHIPCountries = driver.find_elements_by_class_name('a-dropdown-link')






# ----------Read-from-text-file------------
    # with open("aliexpressurl.txt") as links:
    #     urls = links.readlines()
    #     for url in urls:
    #         scrape(url)


#*******************************************************it opens browser and goes to first link but not next one in txt url file. ? why?
try:
    with open("amazonurl.txt") as links:
        urls = links.readlines()
        for url in urls:
            scrape(url)
except:
    print("\n\n\n\n")
    print("MAKE SURE THE FILE NAME IS aliexpressurl.txt")
    print("MAKE SURE IT IS IN THE SAME DIRECTORY")
    print("CHECK THE URL ENTERED")

quit()

    # ----------Read-from-text-file------------
