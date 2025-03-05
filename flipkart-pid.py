import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Define PID codes
PID_CODES = [
    "FLREUC5P4YDDZ9GW",
    "VMCFJ2FKHFFR7CJT",
    "CKBF8YEYFWMVGQHV",
    "NDLEUD6RV6GBSUFC",
    "CHCGRGBGZ5MBWZMM",
]

# Setup the Selenium WebDriver (Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

flipkart_url = "https://www.flipkart.com/product/p/itme?pid="

product_data = []

# Loop through each PID and extract product names
for pid in PID_CODES:
    url = f"{flipkart_url}{pid}"
    driver.get(url)
    time.sleep(3)

    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")

        product_name_element = soup.find("h1", {"class": "_6EBuvT"})
        product_name = product_name_element.text

        price_element = soup.find("div", {"class": "Nx9bqj CxhGGd"})
        price_text = price_element.text

        price = price_text.replace("₹", "").strip()

        # Create a dictionary to store the product details
        product_details = {"PID": pid, "Product Name": product_name, "Price": price}

        prod_det_table = soup.find_all("table", {"class": "_0ZhAN9"})

        for table in prod_det_table:
            rows = table.find_all("tr")

            for row in rows:
                tds = row.find_all("td")
                if len(tds) == 2:
                    key = tds[0].text.strip()
                    value_element = tds[1].find("ul")
                    if value_element:
                        value = value_element.get_text(
                            separator=", "
                        ).strip()  # Join li text if multiple items
                    else:
                        value = "N/A"

                    product_details[key] = value

        product_data.append(product_details)
    except Exception as e:
        print(f"Error extracting product name for PID {pid}: {e}")

# Create a DataFrame from the product_data list
df = pd.DataFrame(product_data)

# Save the DataFrame to a CSV file
df.to_csv("product_details.csv", index=False)

# Print the DataFrame to verify the content
print("Product Details saved to product_details.csv")
print(df.head())

# Close the browser
driver.quit()
