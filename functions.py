import json
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from curl_cffi import requests


def write_to_json(path, content):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(content, file, indent=2)


def get_main_categories(base_url):
    response = requests.get(base_url, impersonate="chrome", timeout=60)
    content = BeautifulSoup(response.text, "html.parser")
    categories = content.find("div", {"id": "hd_hn"})
    categories = categories.div.ul
    categories = categories.find_all("a")
    category_links = [urljoin(base_url, category["href"]) for category in categories]
    return category_links


def get_links(base_url, category_links, selector, save_location):
    all_subcategory_links = []
    for category_link in category_links:
        full_link = urljoin(base_url, category_link)
        category_page = requests.get(full_link, impersonate="chrome", timeout=60)
        category_page_content = BeautifulSoup(category_page.text, "html.parser")
        subcategory_links = category_page_content.find_all("a", selector)
        subcategory_links = [
            urljoin(base_url, subcategory_link["href"])
            for subcategory_link in subcategory_links
        ]
        all_subcategory_links.extend(subcategory_links)
        write_to_json(save_location, all_subcategory_links)
    return all_subcategory_links
