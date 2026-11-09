import json
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://www.davpack.co.uk/"

response = requests.get(base_url, impersonate="chrome", timeout=30)
content = BeautifulSoup(response.text, 'html.parser')
categories = content.find("div", {"id" : "hd_hn"})
categories = categories.div.ul
categories = categories.find_all("a")

category_links = [category['href'] for category in categories]
with open("category_links.json", "w", encoding="utf-8") as file:
    json.dump(category_links, file, indent=2)

all_subcategory_links = []
for category_link in category_links:
    full_link = urljoin(base_url, category_link)
    category_page = requests.get(full_link, impersonate="chrome", timeout=30)
    category_page_content = BeautifulSoup(category_page.text, 'html.parser')
    subcategory_links = category_page_content.find_all("a", {"title" : "View Range"})
    subcategory_links = [subcategory_link["href"] for subcategory_link in subcategory_links]
    all_subcategory_links.extend(subcategory_links)
    with open("sub_category_links.json", "w", encoding="utf-8") as file:
        json.dump(all_subcategory_links, file, indent=2) 
