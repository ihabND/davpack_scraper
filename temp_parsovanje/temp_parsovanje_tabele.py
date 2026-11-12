import sys
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from functions import *

url = "https://www.davpack.co.uk/cardboard-boxes/standard-cardboard-boxes/econobox-cartons.htm"
table = get_table(url)

prices = table.find_all("div", {"class" : "vc"})
price_groups = []
for price in prices:
    price_group = price.find_all("div")
    price_group = [temp.text.strip() for temp in price_group]
    price_groups.append(price_group)

spans = table.find_all("span", {"class" : "pvgh"})

# print(table)
print(price_groups[1:])
print(spans)

#for price in prices:

