from tinydb import TinyDB

from functions import *

base_url = "https://www.davpack.co.uk/"
db = TinyDB("db/boxes_db.json")
boxes_db_table = db.table("boxes")

category_links = get_main_categories(base_url)
write_to_json("json_files/category_links.json", category_links)

all_subcategory_links = get_links(
    base_url=base_url,
    category_links=category_links,
    selector={"title": "View Range"},
    save_location="json_files/sub_category_links.json",
)

product_page_links = get_links(
    base_url=base_url,
    category_links=all_subcategory_links,
    selector={"class": "MIn"},
    save_location="json_files/inner_product_links.json",
)

for products_link in product_page_links:
    if "/cardboard-boxes/" not in products_link:
        break

    table = get_table(products_link)
    product_info = parse_from_table(table)

    for box_info in product_info:
        box = create_box(box_info)
        boxes_db_table.insert(box)