from functions import get_links, get_main_categories, write_to_json

base_url = "https://www.davpack.co.uk/"

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
