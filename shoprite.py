import urllib
import requests
from bs4 import BeautifulSoup as soup
import os
from functions import shoprite_splitter, name_splitter

os.makedirs("Shoprite", exist_ok = True)

url = 'https://www.shoprite.co.za/c-2256/All-Departments?q=%3Arelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page='
#url = 'https://www.shoprite.co.za/c-2256/All-Departments'

page = 0 
#total_pages = 529 #As of 12/09/2020, there are 524 pages.
# filename = "Shoprite.csv"
# file = open(filename, "w")
# headers = "Brand Name, Product Name, Price, Size, Units, Quantity\n"
# file.write(headers)
total_pages = 10

while page < total_pages:
	new_url = url + str(page)
	page += 1

	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
	request = urllib.request.Request(new_url, headers = {'User_agent':user_agent})

	response = urllib.request.urlopen(request)
	page_html = response.read()
	response.close()

	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("div", {"class": "item-product"})

	for container in containers:
		name_container = container.findAll("figcaption", {"class": "item-product__caption"})
		product_name = name_container[0].h3.text.strip()

		price_container = container.findAll("div", {"class": "special-price__price"})
		
		try:
			price1 = price_container[0].span.text.strip().replace("R", "")
			position = price1.index('.')
			price = price1[0:position + 3]
		except TypeError:
			pass

		image_container = container.findAll("div", {"class": "item-product__image"})
		image_url = 'https://www.shoprite.co.za' + image_container[0].img['data-original-src']

		units, size, quantity, name = shoprite_splitter(product_name)

		print("Product Name ----->" + name)
		print("Price ------------>" + price)
		print("Size ------------>" + size)
		print("Units ------------>" + units)
		print("Quantity ------------>" + str(quantity))
		print("Downloading Image %s..." % image_url + "\n")

		# res = requests.get(image_url)
		# if res.ok:
		# 	#Open the directory and store the image.
		# 	image_name = product_name + ".jpg"
		# 	f = open(os.path.join("Shoprite", os.path.basename(image_name)), "wb")
		# 	for chunk in res.iter_content(100000):
		# 		f.write(chunk)
		# 	f.close()

		# #Storing the data into tha file.
		# file.write(product_name + "," + price + "," + image_url + "\n") 
	print("page----------> " + str(page) + "\n")
#file.close()
print("\nFinished scraping data.")