import urllib
import requests
from bs4 import BeautifulSoup as soup
import os
from functions import shoprite_splitter, mark_splitter

os.makedirs("Makro", exist_ok = True)

url = 'https://www.makro.co.za/search?q=%3Arelevance&page='

page = 0 
total_pages = 8 #As of 09/01/2021, there are 3968 pages..
filename = "Makro.csv"
file = open(filename, "w")
headers = "Brand Name, Product Name, Price, Size, Units, Quantity\n"
file.write(headers)

count = 0
while page < total_pages:
	new_url = url + str(page)
	page += 1

	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	#user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
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
			name = name_container[0].text.strip()

			image_container = container.findAll("a", {"class":"product-tile-inner__img js-gtmProductLinkClickEvent"})
			image = image_container[0].img['data-src'] #https is included.
			#print(name + "\t" + image)

			#Fix the price part.
			# price_container = container.findAll("p", {"class":"col-xs-12 price"})
			# temp_price = price_container[0].text.replace("R", "").strip()
			# cents = temp_price[-2:]
			# price = temp_price[0:temp_price.index(cents)] + '.' + cents #fix R45.45. Equal rands and cents.
			# print(price)

			units, quantity, size, prod_name = mark_splitter(name)
			#print("Name: " + name + "\nImage: " + image + "\nPrice: R" + price)

			print("Name: " + name + "\nUnits: " + units +  "\nSize: " + str(size) + "\nQuantity: " + str(quantity))
			print("Downloading Image %s..." % (image)) 
			res = requests.get(image)
			if res.ok:
				#Open the directory and store the image.
				image_name = name + ".jpg"
				f = open(os.path.join("Makro", os.path.basename(image_name)), "wb")
				for chunk in res.iter_content(100000):
					f.write(chunk)
				f.close()

			#Storing the data into tha file.
			file.write(name + ", " + name + "," +  "," + str(size) + "," + units + "," + str(quantity) + "\n")
			print("\n")
		except IndexError:
			pass
	print("\nPage " + str(page)+ "\n")

file.close()		
print(str(count) + " Items were found.")