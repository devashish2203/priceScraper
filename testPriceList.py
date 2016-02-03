#Script to get list of iPhone prices from amazon and flip kart
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchAttributeException
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

class TestProductList:
	def setUp(self):
		self.driver = webdriver.Chrome()
		#Set implicit wait for 10 secs
		self.driver.implicitly_wait(10)

	def test_main(self):
		amazonList = self.getListFromAmazon("iPhone", 35000.00, 60000.00)
		flipkartList = self.getListFromFlipkart("iPhone", 35000.00, 60000.00)
		resultList = amazonList + flipkartList
		resultList.sort(key= lambda x: x[2])

		print("=========")
		for item in resultList:
			print("----------------")
			print "Name: ", item[0]
			print "Link: ", item[1]
			print "Price: ", item[2]
			print("----------------")


		print("========")



	def getListFromAmazon(self, searchTerm, minPrice, maxPrice):
		#print(searchTerm, maxPrice, minPrice)

		assert type(minPrice) == float
		assert type(maxPrice) == float
		browser = self.driver
		browser.get("https://www.amazon.in")

		#Search for iPhone
		searchBox = browser.find_element_by_id("twotabsearchtextbox")
		searchBox.send_keys(searchTerm)
		searchBox.submit()


		#Filter for Apple
		filterList = browser.find_elements_by_class_name("refinementLink")
		for filters in filterList:
			if filters.text == "Apple":
				filters.click()
				break
		time.sleep(2)


		#Filter for Smartphones (Added extra to ensure only smartPhones are shown)
		filterList = browser.find_elements_by_class_name("childRefinementLink")
		for filters in filterList:
			#print(filters.text)
			if filters.text == "Smartphones":
				filters.click()
				break


		time.sleep(5)
		#Set price filters
		browser.find_element_by_id("low-price").send_keys(str(minPrice))
		highPrice = browser.find_element_by_id("high-price")
		highPrice.send_keys(str(maxPrice))
		highPrice.submit()


		# #Sort by Price "Not useful as it lists phone accessories instead of Phones"
		# sortBy = Select(browser.find_element_by_id("sort"))
		# sortBy.select_by_value("price-asc-rank")
		#Parse Results to get name - link - Price
		result = []
		items = browser.find_elements_by_class_name("s-result-item")
		#Reduce wait as page is already loaded
		self.driver.implicitly_wait(1)
		for item in items:
			try:
				nameElement = item.find_element_by_class_name("s-access-detail-page")
			except NoSuchElementException:
				#print("Placeholder result. Skip")
				break
			details = []
			details.append(nameElement.get_attribute("title"))
			details.append(nameElement.get_attribute("href"))

			priceElement = None
			price = None
			try:
				priceElement = item.find_element_by_class_name("s-price")
				price = float(priceElement.text.strip().replace(",", ""))
			except NoSuchElementException:
				#print("Getting price from offers")
				priceElement = item.find_elements_by_class_name("a-color-price")[1]
				price = float(priceElement.text.strip().replace("from ", "").replace(",", "").strip())
			details.append(price)
			if price >= minPrice and price <= maxPrice:
				#print(details)
				result.append(details)

		#Increase wait again
		self.driver.implicitly_wait(10)
		result.sort(key=lambda x: x[2])
		#print("Amazon List", result)
		return result

	def getListFromFlipkart(self, searchTerm, minPrice, maxPrice):
		assert type(minPrice) == float
		assert type(maxPrice) == float
		browser = self.driver
		browser.get("https://www.flipkart.com")

		#Search for iPhone
		searchBox = browser.find_element_by_id("fk-top-search-box")
		searchBox.send_keys(searchTerm)
		searchBox.submit()


		#Filter for mobiles
		filterLinks = browser.find_elements_by_partial_link_text("Mobiles")
		for filters in filterLinks:
			path = None
			try:
				path = filters.get_attribute("path")
			except NoSuchAttributeException:
				#print("Path not found")
				continue
			if path == "mobiles":
				filters.click()
				break

		#Price Filter
		browser.find_element_by_partial_link_text("35001 and Above").click()

		result = []
		products = browser.find_element_by_id("products")
		items = products.find_elements_by_class_name("gd-col")

		for item in items:
			details = []
			nameElement = item.find_element_by_class_name("pu-title")
			#Get first anchor tag
			nameLink = nameElement.find_elements_by_tag_name("a")[0]
			details.append(nameLink.get_attribute("title").strip())
			details.append(nameLink.get_attribute("href"))

			#Get Price
			priceElement = item.find_element_by_class_name("pu-final")
			price = float(priceElement.text.strip().replace("Rs.", "").replace(",", "").strip())
			details.append(price)

			if price >= minPrice and price <= maxPrice:
				result.append(details)
		#Increase wait again
		self.driver.implicitly_wait(10)
		result.sort(key=lambda x: x[2])
		#print("Flipkart Results: ", result)
		return result
				
		pass

	def tearDown(self):
		self.driver.quit()