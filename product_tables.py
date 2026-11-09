import json
from curl_cffi import requests
from bs4 import BeautifulSoup

with open("json_files/inner_product_links.json", "r", encoding="utf-8") as file:
    product_page_links = json.load(file)

for products_link in product_page_links:
    product_table_page = requests.get(products_link, impersonate="chrome", timeout=60)
    product_table_content = BeautifulSoup(product_table_page.text, 'html.parser')
    table = product_table_content.find("div", {"class" : "Table"})
    # table_off_rows = table.find_all("div", {"class" : "off"})
    # table_alt_rows = table.find_all("div", {"class" : "alt"})
    product_codes = table.find_all("div", {"class" : "Code"})
    product_codes = [code.span for code in product_codes]
    product_sizes = table.find_all("div", {"class" : "Answer_DROPDOWN"})
    product_sizes = [code.span for code in product_sizes]
    break

print(product_codes)  
print(product_sizes)