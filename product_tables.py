import json

from bs4 import BeautifulSoup
from curl_cffi import requests
from tinydb import TinyDB

db = TinyDB("boxes_db.json")
boxes_db_table = db.table("boxes")

with open("json_files/inner_product_links.json", "r", encoding="utf-8") as file:
    product_page_links = json.load(file)
print(len(product_page_links), "links to scrape")

counter = 0
total_boxes = []
for products_link in product_page_links:
    print("Scraping", counter)
    counter += 1
    # if counter == 10:
    #     break
    product_table_page = requests.get(products_link, impersonate="chrome", timeout=120)
    product_table_content = BeautifulSoup(product_table_page.text, "html.parser")
    table = product_table_content.find("div", {"class": "Table"})
    # table_off_rows = table.find_all("div", {"class" : "off"})
    # table_alt_rows = table.find_all("div", {"class" : "alt"})
    product_codes = table.find_all("div", {"class": "Code"})
    product_codes = [code.span.text for code in product_codes]

    product_sizes = table.find_all("div", {"class": "Answer_DROPDOWN"})
    product_sizes = [code.span.text for code in product_sizes]

    product_prices = table.find_all("div", {"class": "Answer_DROPDOWN4"})
    product_prices = [code.span.text for code in product_prices]

    product_packet_size = table.find_all("div", {"class": "UnitDesc_Code"})
    product_packet_size = [code.span.text for code in product_packet_size]

    product_info = zip(
        product_codes, product_sizes, product_prices, product_packet_size
    )
    product_info = list(product_info)

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

    with open("db/database.json", "w", encoding="utf-8") as file:
        json.dump(total_boxes, file, indent=2)

print(boxes)
