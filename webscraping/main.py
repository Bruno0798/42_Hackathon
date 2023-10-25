import json
import re
import sys
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from termcolor import colored
import os
from insert_db import upload_data



def clear_terminal():
    os.system('clear')

# Call this function to clear the terminal
clear_terminal()

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 10)
driver.set_window_size(1700, 1080)
driver.delete_cookie('my_cookie')


def detect_currency(product_price):
    # Define a list of common currency symbols and codes
    currency_patterns = {
        "USD": [r"\$", "usd", "dollar"],
        "EUR": [r"€", "eur", "euro"],
        "GBP": [r"£", "gbp", "pound"],
    }

    product_price = product_price.lower()

    for currency_code, patterns in currency_patterns.items():
        for pattern in patterns:
            if re.search(pattern, product_price):
                return currency_code

    # If no currency symbol or code is detected, return a default value (or None)
    return None

def decode_unicode_escape(s):
    return s.encode("utf-8").decode("unicode-escape")

# Read the existing JSON data from the file
with open("sites.json", "r", encoding="utf-8") as json_file:
    sites_data = json.load(json_file)
if isinstance(sites_data, str):
    sites_data = json.loads(sites_data)

# Read the existing JSON data from the file
with open("data.json", "r", encoding="utf-8") as json_file:
    existing_data = json.load(json_file)
if isinstance(existing_data, str):
    existing_data = json.loads(sites_data)

for i in range(3):
	website_name = sites_data[0][i]['website_name']
	print(colored("\t\t\t\t\t\t\t" + website_name, "red"))
	table = PrettyTable()
	table.field_names = ["Wine Name", "Year", "Capacity", "Price", "Discount", "EAN", "Currency", "Scraping Date", "Location"]
	for j in range(4):
		website_name = sites_data[0][i]['website_name']
		product_ean = sites_data[0][i]['data'][j]['product_ean']
		website_url = sites_data[0][i]['url']
		product_name = sites_data[0][i]['data'][j]['product_name']
		product_price = sites_data[0][i]['product_price']
		harvest_year = sites_data[0][i]['data'][j]['harvest_year']
		discount = sites_data[0][i]['data'][j]['discount']
		currency = sites_data[0][i]['data'][j]['currency']
		location = sites_data[0][i]['data'][j]['location']
		product_description = sites_data[0][i]['product_description']

		website_url = driver.current_url
		if website_name == "Continente":
			driver.get("https://www.continente.pt/pesquisa/?q=" + product_ean + "&start=0&srule=Continente&pmin=0.01")
		elif website_name == "El Corte Inglês":
			driver.quit()
			driver = webdriver.Firefox(options=options)
			wait = WebDriverWait(driver, 10)
			driver.get("https://www.elcorteingles.pt/supermercado/pesquisar/?term=" + product_ean)
			driver.set_window_size(1700, 1080)
			driver.delete_cookie('my_cookie')
		elif website_name == "Garrafeira Soares":
			driver.quit()
			driver = webdriver.Firefox(options=options)
			wait = WebDriverWait(driver, 10)
			driver.get("https://www.garrafeirasoares.pt/pt/resultado-da-pesquisa_36.html?term=" + product_ean)
			driver.set_window_size(1700, 1080)
			driver.delete_cookie('my_cookie')
		else:
			clear_terminal()
			print(colored("Fail", 'red', attrs=['bold', 'blink']))
			print(colored("Not Ready For "+ website_name + " website!", attrs=['blink']))
			sys.exit()

		current_url = driver.current_url

		# Access the page source directly
		page_source = driver.page_source

		# Parse the page source with BeautifulSoup
		soup = BeautifulSoup(page_source, "html.parser")

		product_tile = soup.find(class_=sites_data[0][i]['product_tile'])
		description_element = product_tile.find(class_=product_description)
		price_element = product_tile.find(class_=product_price)

		if description_element and price_element:
			product_price_sy = price_element.text
			product_price = product_price_sy.replace("\n", "").replace("€", "").strip()
			currency = detect_currency(product_price_sy)


			scraping_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			table.add_row([product_name, "None", "750ml", product_price, "None", product_ean, currency, scraping_date, "Portugal"])

			new_info = {
				"store_name": website_name,
				"wine_name": product_name,
				"harvest_year": "",
				"capacity": "750ml",
				"price": product_price,
				"discount": "",
				"ean": product_ean,
				"currency": currency,
				"date_scraping": scraping_date,
				"location": location
			}
			existing_data.append(new_info)

			if j == 3:
				print(table)
				print("\n")
	# Write the combined data back to the JSON file
		with open("data.json", "w", encoding="utf-8") as json_file:
			json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
upload_data("data.json")
driver.quit()
