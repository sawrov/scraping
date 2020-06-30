from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

url = input("Enter Valid Aliexpress url\n")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1024)
driver.get(url)

try:
    wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-dialog-body")))
except:
    print("No POPUP Detected")
driver.find_element_by_class_name("next-dialog-close").click()
element = ""
i = 200
while (i < 10000):
    try:
        element = driver.find_element_by_id("product-description")
        print(element.text)
    except:
        pass
    driver.execute_script("window.scrollBy(0, arguments[0]);", i)
    i = i + 100
    if element != "":

        break
print(element.text)
