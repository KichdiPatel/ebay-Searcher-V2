from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from gptCheck import get_products
from eBay import get_breakeven
from helpers import addToPossibilities, addToCheck


# returns the url that the scraper will navigate to
def getURL(page_num):
    # return f"https://boston.craigslist.org/search/ela?bundleDuplicates=1&postal=02215&search_distance=5#search=1~gallery~{page_num}~0"
    # return f"https://boston.craigslist.org/search/pha?bundleDuplicates=1&postal=02215&search_distance=5#search=1~grid~{page_num}~0"
    return f"https://cnj.craigslist.org/search/pha?bundleDuplicates=1#search=1~gallery~{page_num}~0"


# Opens a specific listing page and returns the title, price, and description
def getListingInfo(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            proxy={
                "server": "brd.superproxy.io:22225",
                "username": "brd-customer-hl_502603f3-zone-data_center",
                "password": "7mtjhcw6rp55",
            },
        )
        page = browser.new_page()

        # If the page doesn't load, break out of the method
        try:
            page.goto(url)
            page.wait_for_timeout(8000)
            html = page.inner_html(".body")
        except:
            print(f"{url}: Does not exist on Craigslist")
            browser.close()
            return None, None, None

        browser.close()

    # Getting the title and description
    s = BeautifulSoup(html, "html.parser")
    title = s.find("span", id="titletextonly").text
    try:
        price = float(s.find("span", class_="price").text[1:].replace(",", ""))
    except:
        price = 0
    description = (s.find("section", id="postingbody").text)[:9000]

    # Returning final results
    return title, price, description


def checkListing(url):
    title, price, description = getListingInfo(url)
    if title != None:
        search = get_products(title, description)

        if search[0].lower() == "none" or search[0].lower() == "none.":
            addToCheck(title, price, url)
            print(f"Checked: {title}")
            return

        breakeven = 0
        for item in search:
            try:
                breakeven += get_breakeven(item)
            except:
                breakeven += 0

        # add to possibilities.csv if deemed a good price
        if breakeven > price * 0.9:
            addToPossibilities(item, price, breakeven, url)
        print(f"Checked: {title}")


# Scraping one search page on Craigslist
def getOnePage(url, lastDate):
    searchNext = True

    # Scraping all the html data
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            proxy={
                "server": "brd.superproxy.io:22225",
                "username": "brd-customer-hl_502603f3-zone-data_center",
                "password": "7mtjhcw6rp55",
            },
        )
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        html = page.inner_html(".cl-search-results")
        browser.close()

    # Finding the href and time of each listing
    s = BeautifulSoup(html, "html.parser")
    posts = []
    listings = s.find_all("li", class_="cl-search-result cl-search-view-mode-gallery")

    for listing in listings:
        a_tag = listing.find("a", class_="cl-app-anchor text-only posting-title")
        if a_tag != None:
            href = a_tag.get("href")

            time = (
                listing.find("div", class_="meta")
                .find("span", class_="separator")
                .previous_sibling.strip()
            )
            posts.append((href, time))

    # Check each listing
    for i in range(len(posts)):
        try:
            # check if date is in format M/D
            pattern = r"^\d{1,2}/\d{1,2}$"
            if re.match(pattern, posts[i][1]):
                # Searches one extra day behind what is inputted incase anything is missed
                date = datetime.strptime(posts[i][1], "%m/%d")
                last_date = datetime.strptime(lastDate, "%m/%d")  # - timedelta(days=1)

                if date <= last_date:
                    return False
                # the date is sooner than the last check
                else:
                    checkListing(posts[i][0])

            # the date is in format x mins/hours ago, so it is a good time since this bot is only used daily
            else:
                checkListing(posts[i][0])
        except:
            print("Could not read a page")

    return True


# Make sure not to pick a really old date or else this will run forever
def getAllPages(date):
    # url = getURL(0)

    page_counter = 0

    cont = True

    while cont:
        cont = getOnePage(getURL(page_counter), date)
        print("--------------------------------")
        print("Read page ", page_counter, "...")
        page_counter += 1


def c_main(date):
    # This has issues across years so just choose dates within the same year
    getAllPages(date)
    # Fix description and title to make sure it is under a certain num of characters


# example call
# c_main('4/15')
