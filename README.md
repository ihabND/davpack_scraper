# davpack_scraper

> **Work in progress.** This project isn't finished yet, and the code and data format may change.

A scraper for the cardboard box catalogue on [davpack.co.uk](https://www.davpack.co.uk/). It walks from the main categories to the subcategories and then to the product pages. It reads each product's price-ladder table with BeautifulSoup and stores one record per box code in TinyDB (`db/boxes_db.json`). The links collected at each step are saved to `json_files/`.

This was the first version of the Davpack collector in [box-price-intelligence](https://github.com/ihabND/box-price-intelligence).
