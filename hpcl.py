import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
from captcha_reader import read_captcha


# Define ASIN codes
ASIN_CODES = ["B009BA7S8M", "B01MS8KUBZ", "B01LZVGHB1", "B00OO7C9MW", "B019Z82RVC"]

# Setup the Selenium WebDriver (Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

search_string = "https://hproroute.hpcl.co.in/StateDistrictMap_4/index.jsp"
print(f"Processing ASIN: {search_string}")
driver.get(search_string)

# Scroll to the bottom of the page to ensure all elements are loaded
time.sleep(3)
div_element = driver.find_element(By.ID, "img1")
# Get the location and size of the div element
location = div_element.location
size = div_element.size

img_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = 215; cnv.height = 80;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, driver.find_element(By.ID, "img1"))
with open(r"image.jpg", 'wb') as f:
    f.write(base64.b64decode(img_base64)) 

image_path = './image.jpg'
text = read_captcha(image_path)
print(text)
# Take a screenshot of the entire page
# driver.save_screenshot("screenshot.png")

# Quit the driver after finishing all ASINs
driver.quit()

print("CSV file 'amazon_product_details.csv' has been saved.")
