from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import re



class Order:
	def __init__(self , *args):
		self.driver = None

	def check_status(self):
		# If Driver is running , Skip rerun.
		if self.driver == None:
			return False
		else:
			return True

# Start browser
	def start_browser(self, data):
		PATH = "chromedriver.exe"

		self.driver = webdriver.Chrome(PATH)

		self.driver.get(r"https://grofers.com/")
		
		self.set_location()
		time.sleep(5)

		added , alternates = self.func(data)
		return added , alternates


# Setting location at the grofers landing page
	def set_location(self):
		try:
			self.driver.find_element_by_css_selector(".btn.location-box.mask-button").click()

		except:
			search = self.driver.find_element_by_css_selector("input[role='combobox']")
			search.send_keys("delhi")
			search.send_keys(Keys.RETURN)

		return True


# Type items one by one in the searchbar
	def search_items(self,item):
		search = self.driver.find_element_by_class_name("react-autosuggest__input")
		self.driver.execute_script("arguments[0].click();", search)
		search.send_keys(Keys.CONTROL + "a")
		search.send_keys(Keys.DELETE)
		search.send_keys(item)
		search.send_keys(Keys.RETURN)
		return True


# Searching items
	# Extracting all products
	# Comparing product name with searched item
	# if matched , Adding it to cart
	def func(self , data):
		
		added = []
		alternates = dict()

		for item in data:
			self.search_items(item)
			time.sleep(4)
			try:
				temp = []
				all_products = self.driver.find_elements_by_css_selector(".plp-product")
			except:
				print("error")

			for product in all_products:
				flag = 0
				product_name = product.find_elements_by_css_selector(".plp-product__name--box")
				new = re.sub('[(!@#$/)]', ' ', product_name[0].text.lower())
				for k in item.lower().split():
					if k in new.split():
						flag += 1
				if flag == len(item.split()):
					product.find_element_by_css_selector('.add-to-cart__add-btn').click()
					added.append(item)
					break

				else:
					temp.append(product_name[0].text)


			alternates[item] = temp


		return added , alternates

# Reordering the selected alternatives
	def func_reorder(self , data):
		for item in data:
			self.search_items(item)
			time.sleep(4)
			all_products = self.driver.find_elements_by_css_selector(".plp-product")
			for product in all_products:
				product_name = product.find_elements_by_css_selector(".plp-product__name--box")
				if product_name[0].text == item:
					product.find_element_by_css_selector('.add-to-cart__add-btn').click()
					break

		return True



