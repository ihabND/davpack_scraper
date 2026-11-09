import json
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://www.davpack.co.uk/"

response = requests.get(base_url, impersonate="chrome", timeout=60)
content = BeautifulSoup(response.text, 'html.parser')
categories = content.find("div", {"id" : "hd_hn"})
categories = categories.div.ul
categories = categories.find_all("a")

category_links = [urljoin(base_url, category['href']) for category in categories]
with open("json_files/category_links.json", "w", encoding="utf-8") as file:
    json.dump(category_links, file, indent=2)

all_subcategory_links = []
counter = 0
for category_link in category_links:
    counter += 1
    print("Scraping sub categories", counter)
    full_link = urljoin(base_url, category_link)
    category_page = requests.get(full_link, impersonate="chrome", timeout=60)
    category_page_content = BeautifulSoup(category_page.text, 'html.parser')
    subcategory_links = category_page_content.find_all("a", {"title" : "View Range"})
    subcategory_links = [urljoin(base_url, subcategory_link["href"]) for subcategory_link in subcategory_links]
    all_subcategory_links.extend(subcategory_links)
    with open("json_files/sub_category_links.json", "w", encoding="utf-8") as file:
        json.dump(all_subcategory_links, file, indent=2) 

product_page_links = [] # ovo su sad sub_sub_category, dalja podela od all_subcategory_links
counter = 0
for link in all_subcategory_links:
    counter += 1
    print("Scraping inner", counter)
    full_link = urljoin(base_url, link)
    inner_category_page = requests.get(full_link, impersonate="chrome", timeout=60)
    inner_category_page_content = BeautifulSoup(inner_category_page.text, 'html.parser')
    inner_links = inner_category_page_content.find_all("a", {"class" : "MIn"})
    inner_links = [urljoin(base_url, inner_link["href"]) for inner_link in inner_links]
    product_page_links.extend(inner_links)
    with open("json_files/inner_product_links.json", "w", encoding="utf-8") as file:
        json.dump(product_page_links, file, indent=2)