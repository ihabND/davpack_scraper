import json
import re
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
    table = product_table_content.find("div", {"id": "ListBtm"})
    return table


def parse_from_table(
    table,
    table_link
):
    product_codes = get_column_from_table(table, {"class": "Code"})
    product_sizes_mm = get_column_from_table(table, {"class": "Answer_DROPDOWN"})
    column_1 = get_column_from_table(table, {"class": "Answer_DROPDOWN2"})
    column_2 = get_column_from_table(table, {"class": "Answer_DROPDOWN3"})
    column_3 = get_column_from_table(table, {"class": "Answer_DROPDOWN4"})
    column_4 = get_column_from_table(table, {"class": "UnitDesc_Code"})
    product_price_ranges = get_price_ranges(table)
    product_info = list(
        zip(
            product_codes,
            product_sizes_mm,
            column_1,
            column_2,
            column_3,
            column_4,
            product_price_ranges
        )
    )
    print(table_link)
    return product_info


def create_box(box_info, page_link):
    box_code = box_info[0]
    box_size_mm = box_info[1]
    
    box_type = box_info[2]
    type_check = re.fullmatch(r"[a-zA-Z]+\s-\s[a-zA-Z]+", box_type)
    if type_check:
        box_type = box_info[2]
        size_inch = box_info[3]
    else:
        box_type = None
        size_inch = box_info[2]     
    
    box = {
        "code": box_code,
        "size_mm": box_size_mm,
        "type": box_type,
        "size_inch": size_inch,
        "price": box_info[4],
        "packet_size": box_info[5],
        "price_range": box_info[6],
        "page_url": page_link
    }
    return box


def get_column_from_table(table, selector):
    column_data = table.find_all("div", selector)
    column_data = [code.span.text for code in column_data]
    return column_data


def get_price_ranges(table):
    prices = table.find_all("div", {"class" : "vc"})
    price_groups = []
    price_groups_dict = []
    for price in prices:
        price_group = price.find_all("div")
        price_group = [temp.text.strip() for temp in price_group]
        price_groups.append(price_group)

    spans = table.find_all("span", {"class" : "pvgh"})
    spans = [temp.text.strip() for temp in spans]

    for price_group in price_groups:
        if len(price_group) == 1:
            new_price_group = dict()
            for span in spans:
                new_price_group[span] = price_group[0]  
        else:
            new_price_group = dict()
            zipped_data = list(zip(spans, price_group))
            for data_pair in zipped_data:
                new_price_group[data_pair[0]] = data_pair[1]
        price_groups_dict.append(new_price_group)
    price_groups_dict = price_groups_dict
    return price_groups_dict