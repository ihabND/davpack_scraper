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


def get_table(products_link):
    product_table_page = requests.get(products_link, impersonate="chrome", timeout=120)
    product_table_content = BeautifulSoup(product_table_page.text, "html.parser")
    table = product_table_content.find("div", {"class": "Table"})


def parse_from_table(
    table,
):  # TODO: parsovanje nije kompletno (cijene za ranges nedostaju)
    product_codes = get_column_from_table(table, {"class": "Code"})
    product_sizes = get_column_from_table(table, {"class": "Answer_DROPDOWN"})
    product_type = get_column_from_table(table, {"class": "Answer_DROPDOWN2"})
    product_sizes_inch = get_column_from_table(table, {"class": "Answer_DROPDOWN3"})
    product_prices = get_column_from_table(table, {"class": "Answer_DROPDOWN4"})
    product_packet_size = get_column_from_table(table, {"class": "UnitDesc_Code"})
    product_info = list(
        zip(
            product_codes,
            product_sizes,
            product_type,
            product_sizes_inch,
            product_prices,
            product_packet_size,
        )
    )
    return product_info


def create_box(box_info):
    box = {
        "code": box_info[0],
        "size": box_info[1],
        "type": box_info[2],
        "size_inch": box_info[3],
        "price": box_info[4],
        "packet_size": box_info[5],
    }
    return box


def get_column_from_table(table, selector):
    column_data = table.find_all("div", selector)
    column_data = [code.span.text for code in column_data]
    return column_data
