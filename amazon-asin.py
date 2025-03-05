import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Define ASIN codes
ASIN_CODES = ["B009BA7S8M", "B01MS8KUBZ", "B01LZVGHB1", "B00OO7C9MW", "B019Z82RVC"]

# Setup the Selenium WebDriver (Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

amazon_url = "https://www.amazon.in/dp/"

# List to store product details
product_details = []

for ASIN in ASIN_CODES:
    search_string = amazon_url + ASIN
    print(f"Processing ASIN: {search_string}")
    driver.get(search_string)

    # Scroll to the bottom of the page to ensure all elements are loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract product title and price details
    productTitle = soup.find("span", {"id": "productTitle"})
    price_whole = soup.find("span", {"class": "a-price-whole"})
    price_fraction = soup.find("span", {"class": "a-price-fraction"})
    price = 0

    # Check if price elements are available and format the price
    if price_whole and price_fraction:
        price = price_whole.text + price_fraction.text.strip()

    # Extract details from the product detail table
    prod_det_table = soup.find_all("table", {"class": "a-keyvalue prodDetTable"})

    product_info = {}

    if prod_det_table:
        for table in prod_det_table:
            rows = table.find_all("tr")
            for row in rows:
                th = row.find("th")
                td = row.find("td")

                if th and td:
                    key = th.get_text(strip=True)
                    value = td.get_text(strip=True)
                    product_info[key] = value.strip("\u200e")

    # Store the extracted information in the product_details list
    if productTitle:
        product_details.append(
            {
                "ASIN": ASIN,
                "Product Name": productTitle.get_text(strip=True),
                "Product Price": price,
                "Search Time": str(datetime.now()),
                **product_info,
            }
        )

# Quit the driver after finishing all ASINs
driver.quit()

# Convert the list of product details to a DataFrame
df = pd.DataFrame(product_details)

# Save the DataFrame to a CSV file
df.to_csv("amazon_product_details.csv", index=False)

print("CSV file 'amazon_product_details.csv' has been saved.")
