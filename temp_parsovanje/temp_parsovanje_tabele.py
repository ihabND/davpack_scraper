import sys
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from functions import *

url = "https://www.davpack.co.uk/cardboard-boxes/standard-cardboard-boxes/econobox-cartons.htm"
table = get_table(url)

prices = table.find_all("div", {"class" : "vc"})
price_groups = []
price_groups_dict = []
for price in prices:
    price_group = price.find_all("div")
    price_group = [temp.text.strip() for temp in price_group]
    price_groups.append(price_group)

spans = table.find_all("span", {"class" : "pvgh"})
spans = [temp.text.strip() for temp in spans]

# print(table)
# print(price_groups)
# print(spans) # [<span class="pvgh">1-4</span>, <span class="pvgh">5-9</span>, <span class="pvgh">10+</span>]

for price_group in price_groups:
    if len(price_group) == 1:
        new_price_group = {spans[0] : price_group[0],
                           spans[1] : price_group[0],
                           spans[2] : price_group[0]}
    else:
        new_price_group = {spans[0] : price_group[0],
                           spans[1] : price_group[1],
                           spans[2] : price_group[2]}
    price_groups_dict.append(new_price_group)
print(price_groups_dict[1:])
