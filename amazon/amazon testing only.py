from selenium import webdriver

chrome_path = r"C:\Users\bezz\OneDrive\Desktop\chromedriver.exe"
driver = webdriver.Chrome()
driver.get("https://www.amazon.com/Kikiz-Little-Girls-Princess-Dress/dp/B07NW8KZDP/ref=sr_1_2_sspa?dchild=1&keywords=shoes&qid=1593419826&sr=8-2-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzUk8wMlBJTjBFMUlDJmVuY3J5cHRlZElkPUEwMTkxMDUwWDQxT1lDWjdLSDY3JmVuY3J5cHRlZEFkSWQ9QTAyNTAxOTAyQU9YSkdNNk0wTTE3JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1&psc=1")

size = driver.find_element_by_id("variation_size_name")
print("size: " + size.text)




size = driver.find_element_by_xpath('//*[@id="dropdown_selected_size_name"]/span').click()
sizes = driver.find_elements_by_xpath("//ul[@class='a-nostyle a-list-link']/li/a[@class='a-dropdown-link']")
colors = driver.find_elements_by_xpath("//ul[@role='radiogroup']//img")
price = driver.find_element_by_xpath('//SPAN[@id="priceblock_ourprice"]')
print("PRICE: " + price.text)
availability = driver.find_element_by_id('availabilityInsideBuyBox_feature_div')
print ("AVAILABILITY   "+availability.text)
for size in sizes:
    size.text + ("\t")
for color in colors:
    color.get_attribute('alt')
    print(color.get_attribute("alt") + "--" + size.text + ("\t") + ":" + driver.find_element_by_xpath(
                    '//SPAN[@id="priceblock_ourprice"]').text + "--->" + driver.find_element_by_id(
                    'availability').text)
driver.quit()

#size = driver.find_element_by_id("variation_size_name")
#print("size: " + size.text)

#size_button = driver.find_element_by_xpath('//*[@id="dropdown_selected_size_name"]/span').click()

#sizes = driver.find_elements_by_xpath("//ul[@class='a-nostyle a-list-link']/li/a[@class='a-dropdown-link']")

#colors = driver.find_elements_by_xpath("//ul[@role='radiogroup']//img")

#for size in sizes:
#    print(size.text + "\t")

#for color in colors:
#    print(color.get_attribute('alt'))



#title = driver.find_element_by_id('productTitle')
#print("TITLE: " + title.text)

#https://www.amazon.com/Brooks-Mens-Ghost-Biking-Black/dp/B07L6KNJZV/ref=sr_1_8?dchild=1&keywords=shoes&qid=1592311675&sr=8-8

#price = driver.find_element_by_id('unifiedPrice_feature_div')
#print("PRICE: " + price.text)
#price = driver.find_element_by_id('desktop_unifiedPrice')
#print("PRICE: " + price.text)
#price = driver.find_element_by_id('price')
#print("PRICE: " + price.text)
#price = driver.find_element_by_id("priceblock_ourprice")
#print("PRICE: " + price.text)
#price = driver.find_element_by_xpath('//SPAN[@id="priceblock_ourprice"]')
#print("PRICE: " + price.text)

#select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
#select.select_by_visible_text("7")


#select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
#select.select_by_visible_text("8")


#select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
#select.select_by_visible_text("8.5")


#select = Select(driver.find_element_by_id("native_dropdown_selected_size_name"))
#select.select_by_visible_text("9")

#color = driver.find_element_by_id("variation_color_name")
#print("color: " + color.text)

#color = driver.find_element_by_id("variation_color_name")
#print("color: " + color.text)

#InStock = driver.find_elements_by_id("availability")
#print(id("availability"))

#driver.find_elements_by_id('color_name')
#print(id("color_name"))

#quantity = driver.find_element_by_id('quantity')
#print ("QUANTITY   "+quantity.text)

#availability = driver.find_element_by_id('availabilityInsideBuyBox_feature_div')
#print ("AVAILABILITY   "+availability.text)



