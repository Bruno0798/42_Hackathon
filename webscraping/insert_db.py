import json
import mysql.connector

# Open and parse the JSON file
with open('data.json') as file:
    json_data = json.load(file)

# Connect to your MySQL database
connection = mysql.connector.connect(
    host="sql11.freemysqlhosting.net",
    user="sql11655896",
    password="E5IHUDYfiT",
    database="sql11655896"
)
cursor = connection.cursor()

for item in json_data
    store_name = item["store_name"]
    wine_name = item["wine_name"]
    harvest_year = item["harvest_year"]
    capacity = item["capacity"]
    price_value = item["price"]
    discount = item["discount"]
    currency = item["currency"]
    timestamp = item["date_scraping"]
    location = item["location"]

# Extract the variables from the JSON object
""" store_name = json_data[0]["store_name"]
wine_name = json_data[0]["wine_name"]
harvest_year = json_data[0]["harvest_year"]
capacity = json_data[0]["capacity"]
price_value = json_data[0]["price"]
discount = json_data[0]["discount"]
currency = json_data[0]["currency"]
timestamp = json_data[0]["date_scraping"]
location = json_data[0]["location"] """

# Check if the wine already exists
select_wine = ("SELECT wine_id FROM wines WHERE wine_name = '"+wine_name+"\'")
cursor.execute(select_wine)
row = cursor.fetchone()

if row:
    wine_id = row[0]
else:
    # Insert the wine if it doesn't exist
    insert_wine = ("INSERT INTO wines (wine_name, harvest_year, capacity, location) VALUES ('"+wine_name+"', '"+(harvest_year)+"', '"+capacity+"', '"+location+"')")
    print(insert_wine)
    cursor.execute(insert_wine)
    wine_id = cursor.lastrowid

# Execute the INSERT statement

#insert_prices = "INSERT INTO prices (price_value, discount, store_id, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)"
#values = (price_value, discount, wine_id, store_id, timestamp)
#cursor.execute(insert_prices, values)

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()
