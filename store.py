import urllib
import requests
from bs4 import BeautifulSoup as soup
import os #Automatically make a file and store images in that file.
import re
from functions import attached_last, attached_first, unattached_first, unattached_last, appear_middle, name_splitter

os.makedirs("Images", exist_ok = True) #Creates a folder if it does not exist.

#URL = 'https://www.game.co.za/game-za/en/All-Game-Categories/Groceries-%26-Household/Groceries/c/G0067?q=%3Arelevance&page='
URL = 'https://www.game.co.za/game-za/en/All-Game-Categories/c/G000?q=%3Arelevance&page='

page = 0
#As of 7/11/2020, there are 760 pages.
while page < 3:
	new_url = URL + str(page)
	page += 1

	user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
	request = urllib.request.Request(new_url, headers={'User-Agent': user_agent})

	#Opening a connection and grabbing the page/request access to the url.
	response = urllib.request.urlopen(request)
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
		old_price_container = container.findAll("span", {"class":"strikethrough"})
		old_price = old_price_container[0].text.strip()

		#units, size, actual_product_name = name_splitter(product_name)
		# print("Name ---> " + actual_product_name)
		# print("Price ---> R" + price)
		# print("Size ---> " + size + units)
		pos = name_splitter(product_name)
		print("Position -----> " + pos)
		print(" ")

		#print("Downloading Image %s..." % (product_image)) 
		#res = requests.get(product_image)
		#if res.ok:
			#Open the directory and store the image.
			#image_name = product_name + ".jpg"
			#f = open(os.path.join("Images", os.path.basename(image_name)), "wb")
			#for chunk in res.iter_content(100000):
				#f.write(chunk)
			#f.close()
	print("----------> Page " + str(page))
	print("\n")

print("\n")
print("Finished scraping data.")
