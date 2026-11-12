import json

from bs4 import BeautifulSoup
from curl_cffi import requests
from tinydb import TinyDB

from functions import get_column_from_table, write_to_json

db = TinyDB("boxes_db.json")
boxes_db_table = db.table("boxes")

with open("json_files/inner_product_links.json", "r", encoding="utf-8") as file:
    product_page_links = json.load(file)
print(len(product_page_links), "links to scrape")

total_boxes = []
for products_link in product_page_links:
    product_table_page = requests.get(products_link, impersonate="chrome", timeout=120)
    product_table_content = BeautifulSoup(product_table_page.text, "html.parser")
    table = product_table_content.find("div", {"class": "Table"})

    product_codes = get_column_from_table(table, {"class": "Code"})
    product_sizes = get_column_from_table(table, {"class": "Answer_DROPDOWN"})
    product_prices = get_column_from_table(table, {"class": "Answer_DROPDOWN4"})
    product_packet_size = get_column_from_table(table, {"class": "UnitDesc_Code"})

    product_info = list(
        zip(product_codes, product_sizes, product_prices, product_packet_size)
    )

    boxes = []
    for box_info in product_info:
        box = {
            "code": box_info[0],
            "size": box_info[1],
            "price": box_info[2],
            "packet_size": box_info[3],
        }
        if box not in total_boxes:
            boxes.append(box)
            boxes_db_table.insert(box)
    total_boxes.extend(boxes)

    write_to_json("db/database.json", total_boxes)
