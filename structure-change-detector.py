# import hashlib
# from selenium import webdriver
# from bs4 import BeautifulSoup

# # Step 1: Fetch the HTML content from a webpage
# url = 'https://www.amazon.in/dp/B019Z82RVC'  # Replace with your target URL

# options = webdriver.ChromeOptions()
# options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
# options.add_argument("--incognito")
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# # Step 2: Parse the HTML content with BeautifulSoup
# driver.get(url)
# soup = BeautifulSoup(driver.page_source, "html.parser")

# # Step 3: Extract structure (tags, id, class) for specific elements
# def extract_structure_for_specific_elements(soup):
#     elements_info = []

#     # Target elements and their selectors
#     target_elements = [
#         {"tag": "span", "id": "productTitle"},
#         {"tag": "span", "class": "a-price-whole"},
#         {"tag": "span", "class": "a-price-fraction"},
#         {"tag": "table", "class": "a-keyvalue prodDetTable"}
#     ]

#     for element in target_elements:
#         # Find the element by its attributes
#         if "id" in element:
#             found_tag = soup.find(element["tag"], {"id": element["id"]})
#         elif "class" in element:
#             found_tag = soup.find(element["tag"], {"class": element["class"]})
        
#         if found_tag:
#             # Collect relevant structural details
#             tag_info = {
#                 'tag': found_tag.name,
#                 'id': found_tag.get('id', None),
#                 'classes': found_tag.get('class', []),
#                 'parent_tag': found_tag.parent.name if found_tag.parent else None,
#                 'parent_id': found_tag.parent.get('id', None) if found_tag.parent else None,
#                 'parent_classes': found_tag.parent.get('class', []) if found_tag.parent else None
#             }
#             elements_info.append(tag_info)
            
#             # If the found tag is a table, process its rows (<tr>) and header cells (<th>, <td>)
#             if found_tag.name == 'table':
#                 # Traverse all rows in the table
#                 for row in found_tag.find_all('tr'):
#                     row_info = {'tag': 'tr', 'cells': []}
                    
#                     # Check for <th> (table header) and <td> (table data) tags
#                     th_cells = row.find_all('th')
#                     td_cells = row.find_all('td')
                    
#                     # Store the structure of th and td cells
#                     for cell in th_cells:
#                         row_info['cells'].append({'cell_tag': 'th', 'classes': cell.get('class', [])})
#                     for cell in td_cells:
#                         row_info['cells'].append({'cell_tag': 'td', 'classes': cell.get('class', [])})
                    
#                     # Only add to elements_info if there are cells in the row
#                     if row_info['cells']:
#                         elements_info.append(row_info)

#     return elements_info

# # Step 4: Convert the structure into a hashable form
# structure = extract_structure_for_specific_elements(soup)
# structure_str = str(structure)  # Convert the list of tag structures to a string
# print("Extracted Structure:", structure)

# # Step 5: Create a hash for the current structure
# current_hash = hashlib.md5(structure_str.encode('utf-8')).hexdigest()

# # For demonstration, we'll assume `previous_hash` is a hash we stored earlier
# # You can load it from a file or database

# try:
#     with open('previous_hash.txt', 'r') as file:
#         previous_hash = file.read().strip()
# except FileNotFoundError:
#     previous_hash = None

# # Step 6: Compare the current hash with the previous one
# if previous_hash != current_hash:
#     print("The structure of the tracked elements has changed.")
#     # Update the stored hash to the new one
#     with open('previous_hash.txt', 'w') as file:
#         file.write(current_hash)
# else:
#     print("The structure of the tracked elements has not changed.")

# driver.quit()

# ------------------------------------------------------------

import hashlib
from selenium import webdriver
from bs4 import BeautifulSoup

# Step 1: Fetch the HTML content from a webpage
url = 'https://www.amazon.in/dp/B01LZVGHB1'  # Example URL with one or more tables

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors
options.add_argument("--incognito")
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Step 2: Parse the HTML content with BeautifulSoup
driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")

# Step 3: Extract structure (tags, id, class) for specific elements
def extract_structure_for_specific_elements(soup):
    elements_info = []

    # Target elements and their selectors
    target_elements = [
        {"tag": "span", "id": "productTitle"},
        {"tag": "span", "class": "a-price-whole"},
        {"tag": "span", "class": "a-price-fraction"},
    ]

    for element in target_elements:
        # Find the element by its attributes
        if "id" in element:
            found_tag = soup.find(element["tag"], {"id": element["id"]})
        elif "class" in element:
            found_tag = soup.find(element["tag"], {"class": element["class"]})
        
        if found_tag:
            # Collect relevant structural details
            tag_info = {
                'tag': found_tag.name,
                'id': found_tag.get('id', None),
                'classes': found_tag.get('class', []),
                'parent_tag': found_tag.parent.name if found_tag.parent else None,
                'parent_id': found_tag.parent.get('id', None) if found_tag.parent else None,
                'parent_classes': found_tag.parent.get('class', []) if found_tag.parent else None
            }
            elements_info.append(tag_info)

    return elements_info

# Step 4: Convert the structure into a hashable form
structure = extract_structure_for_specific_elements(soup)
structure_str = str(structure)  # Convert the list of tag structures to a string
print("Extracted Structure:", structure)

# Step 5: Create a hash for the current structure
current_hash = hashlib.md5(structure_str.encode('utf-8')).hexdigest()

# For demonstration, we'll assume `previous_hash` is a hash we stored earlier
# You can load it from a file or database

try:
    with open('previous_hash.txt', 'r') as file:
        previous_hash = file.read().strip()
except FileNotFoundError:
    previous_hash = None

# Step 6: Compare the current hash with the previous one
if previous_hash != current_hash:
    print("The structure of the tracked elements has changed.")
    # Update the stored hash to the new one
    with open('previous_hash.txt', 'w') as file:
        file.write(current_hash)
else:
    print("The structure of the tracked elements has not changed.")

driver.quit()
