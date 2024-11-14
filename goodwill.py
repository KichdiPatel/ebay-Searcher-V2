import requests
from bs4 import BeautifulSoup
import re
from eBay import get_breakeven
from helpers import addToPossibilities, addToCheck
import time

# These are the target category links that I want to search for my business
DATA = [
    (
        "https://www.goodwillfinds.com/electronics/cameras-and-photography/film-and-polaroid-cameras/?start={n}&sz=48",
        840,
    ),
    (
        "https://www.goodwillfinds.com/electronics/cameras-and-photography/digital-cameras/?start={n}&sz=48",
        600,
    ),
    (
        "https://www.goodwillfinds.com/electronics/cameras-and-photography/camcorders/?start={n}&sz=48",
        240,
    ),
]


# Getting the listings on a given page
def getListings(url):
    # Print to see progress
    print("searching: " + url)

    response = requests.get(url)
    html = response.text
    s = BeautifulSoup(html, "html.parser")

    # Get all Listings
    item_list = s.find_all("article", class_="b-product_tile js-analytics-item")
    items = []

    for item in item_list:
        # finding title
        title = item.find("p", class_="b-product_tile-title").text.replace("\n", "")

        # finding the price
        price = item.find("span", class_="b-price-item m-new")
        if price == None:
            price = item.find("span", class_="b-price-item")

        price = price.get_text(strip=True)
        price = float(re.search(r"\$([\d.]+)", price).group(1))

        # finding the href
        a_element = item.find("a", class_="b-product_tile-title_link")
        href = (
            "https://www.goodwillfinds.com/electronics/cameras-and-photography"
            + a_element.get("href")
        )

        items.append((title, price, href))

    return items


# Getting all the listings given the predefined "DATA" above
def getAllListings():
    totalListings = []

    # Searches through each link to get their listing info
    for category in DATA:
        # num is a counter for the listings being read
        num = 48
        while num < category[1]:
            link = category[0]
            link = link.format(n=num)

            arr = getListings(link)

            totalListings += arr

            num += 48

    return totalListings


# This first gets the breakeven price for the given listing title, and if the listing is deemed to be good,
# then it is added to possibilities.csv
def checkListing(listing):
    search, price, link = listing

    breakeven = get_breakeven(search)

    if breakeven > price + 40:
        addToPossibilities(search, price, breakeven, link)


# checks all the listings for all the pages in DATA
def checkAllListings():
    arr = getAllListings()

    i = 0
    for listing in arr:
        checkListing(listing)
        time.sleep(1)
        print(f"Checked Listing {i}")
        i += 1


# Example Call

# checkAllListings()
