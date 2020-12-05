import urllib
import requests
from bs4 import BeautifulSoup as soup
import os
from functions import makro_splitter

os.makedirs("Makro", exist_ok = True)

url = 'https://www.makro.co.za/beverages-liquor/coffee-teas-hot-drinks/coffee/c/JCA?q=%3Arelevance&page='

page = 0 
#total_pages = 577 #As of 17/10/2020, there are 577 pages.
# filename = "Makro.csv"
# file = open(filename, "w")
# headers = "Brand Name, Product Name, Price, Size, Units, Quantity\n"
# file.write(headers)
total_pages = 8
count = 0
while page < total_pages:
	new_url = url + str(page)
	page += 1

	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
	request = urllib.request.Request(new_url, headers = {'User_agent':user_agent})

	response = urllib.request.urlopen(request)
	page_html = response.read()
	response.close()

	page_soup = soup(page_html, "html.parser")

	containers = page_soup.findAll("div", {"class": "product-tile-inner"})
	for container in containers:
		count += 1
		try:
			name_container = container.findAll("a", {"class": "product-tile-inner__productTitle js-gtmProductLinkClickEvent"})
			name_container_text = name_container[0].text.strip()
			# position = name_container_text.find("(")
			# size_container = name_container_text[position:]

			image_container = container.findAll("a", {"class":"product-tile-inner__img js-gtmProductLinkClickEvent"})
			image = image_container[0].img['data-src'] #https is included.

			price_container = container.findAll("p", {"class":"col-xs-12 price"})
			temp_price = price_container[0].text.replace("R", "").strip()
			cents = temp_price[-2:]
			price = temp_price[0:temp_price.index(cents)] + '.' + cents

			units, quantity = makro_splitter(name_container_text)

			print("Name --->" + name_container_text + "\nImage --->" + image + "\nPrice --->R" + price + "\nUnits --->" + units + "\nQuantity --->" + str(quantity))
		except IndexError:
			pass
	print("\nPage " + str(page)+ "\n")
		
print(str(count) + " Items were found.")