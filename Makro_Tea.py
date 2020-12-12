import urllib
import requests
from bs4 import BeautifulSoup as soup
import os
from functions import makro_splitter

os.makedirs("Makro", exist_ok = True)

url = 'https://www.makro.co.za/beverages-liquor/coffee-teas-hot-drinks/tea/c/JCB?q=%3Arelevance&page='
page = 0 
total_pages = 6 #As of 12/12/2020, there are 8 pages.
filename = "Makro.csv"
file = open(filename, "w")
headers = "Brand Name, Product Name, Price, Size, Units, Quantity\n"
file.write(headers)

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
			#brand_name = name_container_text

			image_container = container.findAll("a", {"class":"product-tile-inner__img js-gtmProductLinkClickEvent"})
			image = image_container[0].img['data-src'] #https is included.

			price_container = container.findAll("p", {"class":"col-xs-12 price"})
			temp_price = price_container[0].text.replace("R", "").strip()
			cents = temp_price[-2:]
			price = temp_price[0:temp_price.index(cents)] + '.' + cents #fix R45.45. Equal rands and cents.

			units, quantity, size = makro_splitter(name_container_text)

			print("Name: " + name_container_text + "\nPrice: R" + price + "\nUnits: " + units +  "\nSize: " + size + "\nQuantity: " + str(quantity))
			print("Downloading Image %s..." % (image)) 
			res = requests.get(image)
			if res.ok:
				#Open the directory and store the image.
				image_name = name_container_text + ".jpg"
				f = open(os.path.join("Makro", os.path.basename(image_name)), "wb")
				for chunk in res.iter_content(100000):
					f.write(chunk)
				f.close()

			#Storing the data into tha file.
			file.write(name_container_text + ", " + name_container_text + "," + price + "," + size + "," + units + "," + str(quantity) + "\n")
			print("\n")
		except IndexError:
			pass
	print("\nPage " + str(page)+ "\n")

file.close()		
print(str(count) + " Items were found.")