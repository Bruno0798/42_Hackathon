import json
import mysql.connector

def upload_data(file):
    # Open and parse the JSON file
    with open(file) as file:
        json_data = json.load(file)

    # Connect to your MySQL database
    connection = mysql.connector.connect(
        host="sql11.freemysqlhosting.net",
        user="sql11655896",
        password="E5IHUDYfiT",
        database="sql11655896"
    )
    cursor = connection.cursor()

    for item in json_data:
        store_name = item["store_name"]
        wine_name = item["wine_name"]
        harvest_year = item["harvest_year"]
        capacity = item["capacity"]
        price_value = item["price"]
        discount = item["discount"]
        currency = item["currency"]
        timestamp = item["date_scraping"]
        location = item["location"]
        # Check if the wine already exists
        select_wine = ("SELECT wine_id FROM wines WHERE wine_name = '"+wine_name+"\'")
        cursor.execute(select_wine)
        row = cursor.fetchone()

        if row:
            wine_id = row[0]
        else:
            # Insert the wine if it doesn't exist
            insert_wine = ("INSERT INTO wines (wine_name, harvest_year, capacity, location) VALUES ('"+wine_name+"', '"+harvest_year+"', '"+capacity+"', '"+location+"')")
            cursor.execute(insert_wine)
            wine_id = cursor.lastrowid

        # Check if the store already exists
        select_store = ("SELECT store_id FROM stores WHERE store_name = '"+store_name+"\'")
        cursor.execute(select_store)
        row = cursor.fetchone()

        if row:
            store_id = row[0]
        else:
            # Insert the store if it doesn't exist
            insert_store = ("INSERT INTO stores (store_name) VALUES ('"+store_name+"')")
            cursor.execute(insert_store)
            store_id = cursor.lastrowid
        wine_id = str(wine_id)
        store_id = str(store_id)
        price_value = price_value.replace(',', '.')
        insert = ("INSERT INTO prices (wine_id, store_id, price_value, discount, currency, timestamp) VALUES ('"+wine_id+"' ,'"+store_id+"' ,"+price_value+" ,'"+discount+"' ,'"+currency+"' ,'"+timestamp+"')")
        cursor.execute(insert)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()
