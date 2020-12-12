import urllib
from urllib.error import HTTPError
from urllib.error import URLError
import requests
from bs4 import BeautifulSoup as soup
import os #Automatically make a file and store images in that file.
import re
from functions import name_splitter, shoprite_splitter

#os.makedirs("Game", exist_ok = True) #Creates a folder if it does not exist.

URL = 'https://www.game.co.za/game-za/en/All-Game-Categories/c/G000?q=%3Arelevance&page='

page = 0 
total_pages = 647 #As of 17/10/2020, there are 647 pages.
filename = "Game.csv"
file = open(filename, "w")
headers = "Brand Name, Product Name, Price, Size, Units, Quantity\n"
file.write(headers)

while page < 10:
	new_url = URL + str(page)
	page += 1

	#user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
	headers={'User-Agent':user_agent,}
	request = urllib.request.Request(new_url, None, headers)

	response = urllib.request.urlopen(request)

	#Opening a connection and grabbing the page/request access to the url.
	#response = urllib.request.urlopen(request)
	page_html = response.read() #Offloads the contents of the web page into a variable.
	response.close() #Closes a connection.

	#Parses the html.
	page_soup = soup(page_html, "html.parser")

	#Grabs each product container.
	containers = page_soup.findAll("div", {"class": "product-item productListerGridDiv"})

	#Loop through each container and grab neccessary data.
	for container in containers:
		brand_container = container.findAll("div", {"class":"product-brand"}) 
		brand_name = brand_container[0].text.strip() 

		image_container = container.findAll("div", {"class":"productPrimaryImage"})
		image = image_container[0].img['src']
		product_image = "https://www.game.co.za" + image #URL image.

		product_name_container = container.findAll("div",{"class":"product-name"})
		product_name = product_name_container[0].text.strip()

		price_container = container.findAll("span", {"class":"finalPrice"})
		price = price_container[0].text.replace("R","")

		#Not needed.
		old_price_container = ""
		old_price = "" 

		#Not needed.
		try:
			old_price_container = container.findAll("span", {"class":"strikethrough"})
			old_price = old_price_container[0].text.strip()
		except:
			pass

		units, size, quantity, name = shoprite_splitter(product_name)
		print("Name ---> " + name)
		print("Price ---> R" + price)
		print("Size ---> " + size + units)
		print("Quantity ---> " + str(quantity)) 
		print(" ")

		print("Downloading Image %s..." % (product_image)) 
		res = requests.get(product_image)
		if res.ok:
			#Open the directory and store the image.
			image_name = product_name + ".jpg"
			f = open(os.path.join("Game", os.path.basename(image_name)), "wb")
			for chunk in res.iter_content(100000):
				f.write(chunk)
			f.close()

		#Storing the data into tha file.
		file.write(name + ", " + name + "," + price + "," + size + "," + units + "," + str(quantity) + "\n")

	print("----------> Page " + str(page) + "\n")

file.close()
print("\nFinished scraping data.")