import sys
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from functions import *

url = "https://www.davpack.co.uk/cardboard-boxes/standard-cardboard-boxes/econobox-cartons.htm"
table = get_table(url)

prices = table.find_all("div", {"class" : "vc"})
print(prices)
