from curl_cffi import requests
from bs4 import BeautifulSoup

base_url = "https://www.davpack.co.uk/"

response = requests.get(base_url, impersonate="chrome", timeout=30)
content = BeautifulSoup(response.text, 'html.parser')
categories = content.find("div", {"id" : "hd_hn"})
categories = categories.div.ul
categories = categories.find_all("a")

category_links = [category['href'] for category in categories]
print(category_links)
