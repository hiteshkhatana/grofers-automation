from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import pandas as pd
import numpy as np
import os






#PATH = "chromedriver.exe"


def func(data):
    ordered_list = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(executable_path =os.environ.get("CHROMEDRIVER_PATH") , chrome_options=chrome_options)


    driver.get(r"https://grofers.com/")
    
    #location = driver.find_element_by_class_name("Select-control")
    #location.click()
    #search = driver.find_element_by_css_selector("input[role='combobox']")
    #search.send_keys("New delhi")
    #search.send_keys(Keys.RETURN)
    
    time.sleep(3)
    
    for item in data["product"]:
        search = driver.find_element_by_class_name("react-autosuggest__input")
        driver.execute_script("arguments[0].click();", search)
        search.send_keys(Keys.CONTROL + "a")
        search.send_keys(Keys.DELETE)
        search.send_keys(item)
        search.send_keys(Keys.RETURN)


        time.sleep(3)


        all_products = driver.find_elements_by_xpath("//div[@class='plp-product']")
        for product in all_products:
            product_name = product.find_element_by_class_name('plp-product__name--box').text
            if product_name == item:
                add = product.find_element_by_class_name('add-to-cart__add-btn')
                add.click()
                ordered_list.append(item + " is ordered")
                break

    



    time.sleep(5)
    #driver.quit()
    return(ordered_list)



def create():
	rows = ["MDH Deggi Red Chilli Powder",
	"MDH Garam Masala",
	"MDH Coriander Powder/Dhania",
	"MDH Cumin Powder/Jeera",
	"MDH Turmeric Powder/Haldi",
	"Brooke Bond Red Label Tea (Zip Lock)",
	"Mawana Premium Crystal Sulphurless Sugar",
	"Ariel Complete Detergent Powder",
	"Rajdhani Besan",
	"India Gate Broken Mogra Basmati Rice",
	"Grofers Mother's Choice Unpolished Black Urad Dal (Chilka)",
	"Grofers Mother's Choice Unpolished Green Moong Dal (Chilka)",
	"Grofers Mother's Choice Unpolished Chana Dal",
	"Grofers Mother's Choice Unpolished Red Masoor Dal",
	"Grofers Mother's Choice American Almonds",
	"Grofers Mother's Choice Kishmish/Raisins",
	"Grofers Mother's Choice Walnut Kernels"]

	column = ["product"]

	data = pd.DataFrame(rows , columns = column)

	return data

#ata = create()

#all_p = func(data)
#for i in all_p:
#	print(i)
