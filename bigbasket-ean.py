import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Define EAN codes
EAN_CODES = [
    "284420",
    "1232573",
    "280474",
    "40237234",
    "1208821",
]

# Setup the Selenium WebDriver (Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument("--incognito")
options.add_argument("--headless")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=options)

bigbasket_url = "https://www.bigbasket.com/pd/"

product_data = []

for ean in EAN_CODES:
    url = f"{bigbasket_url}{ean}"
    print(f"Processing EAN: {ean} - {url}")
    driver.get(url)
    time.sleep(3)

    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        product_name_element = soup.find("h1", {"class": "bofYPK"})
        product_name = product_name_element.text

        price_element = soup.find("td", {"class": "fLZywG"})
        price_text = price_element.text
        match = re.search(r"₹(\d+)", price_text)
        price = 0
        if match:
            price = match.group(1)

        # Create a dictionary to store the product details
        product_details = {"PID": ean, "Product Name": product_name, "Price": price}

        # prod_det_table = soup.find_all("table", {"class": "_0ZhAN9"})

        # for table in prod_det_table:
        #     rows = table.find_all("tr")

        #     for row in rows:
        #         tds = row.find_all("td")
        #         if len(tds) == 2:
        #             key = tds[0].text.strip()
        #             value_element = tds[1].find("ul")
        #             if value_element:
        #                 value = value_element.get_text(
        #                     separator=", "
        #                 ).strip()  # Join li text if multiple items
        #             else:
        #                 value = "N/A"

        #             product_details[key] = value

        product_data.append(product_details)
    except Exception as e:
        print(f"Error extracting product name for PID {ean}: {e}")

# Create a DataFrame from the product_data list
df = pd.DataFrame(product_data)

# Save the DataFrame to a CSV file
df.to_csv("product_details.csv", index=False)

# Print the DataFrame to verify the content
print("Product Details saved to product_details.csv")
print(df.head())

# Close the browser
driver.quit()
