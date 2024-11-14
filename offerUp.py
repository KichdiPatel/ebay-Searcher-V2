from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from gptCheck import get_products
from helpers import addToPossibilities, addToCheck
from eBay import get_breakeven


# gets all the listings on a offerup page
def getListingInfo(url):
    url = "https://offerup.com" + url
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # If the page doesn't load, break out of the method
        try:
            page.goto(url)
            page.wait_for_timeout(8000)
            html = page.inner_html("#__next")
        except:
            print(f"{url}: Does not exist on Offerup")
            browser.close()
            return None, None, None

        browser.close()

    # Getting the title and description
    s = BeautifulSoup(html, "html.parser")
    try:
        container = s.find(
            "div",
            class_="MuiGrid-root MuiGrid-container MuiGrid-direction-xs-row-reverse MuiGrid-align-content-xs-center",
        )
        title = container.find_all("h5")[0].text
    except:
        title = ""
        print("no title")

    try:
        price = float(
            s.find(
                "p",
                class_="MuiTypography-root MuiTypography-h3 MuiTypography-colorTextPrimary MuiTypography-displayInline",
            )
            .text[1:]
            .replace(",", "")
        )
    except:
        price = 0
        print("no price")

    try:
        container = s.find(
            "div",
            class_="MuiGrid-root MuiGrid-container MuiGrid-direction-xs-row-reverse MuiGrid-align-content-xs-center",  # MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1 MuiGrid-direction-xs-column
        )

        description = container.find_all("p")[-2].text[:9000]
        # for i in range(len(description)):
        #     print(i, description[i])
        # print("description", description)
    except:
        description = ""
        print("no description")

    # Returning final results
    return title, price, description


# checks a individual listing page
def checkListing(url):
    title, price, description = getListingInfo(url)

    if title != None:
        search = get_products(title, description)
        if search[0].lower() == "none" or search[0].lower() == "none.":
            addToCheck(title, price, ("https://offerup.com" + url))
            print(f"Checked: {title}")
            return

        for item in search:
            try:
                breakeven = get_breakeven(item)
            except:
                breakeven = 0
            if breakeven > price * 0.9:
                addToPossibilities(
                    item, price, breakeven, ("https://offerup.com" + url)
                )
            print(f"Checked: {title}")


# Scraping one search page on Craigslist
# numListings = the number of Listings that should be checked from the top(1-49)
def getOnePage(url, numListings):
    # Scraping all the html data
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)
        html = page.inner_html("#__next")
        # print(page.content())
        browser.close()

    # Finding the hrefs each listing
    s = BeautifulSoup(html, "html.parser")
    posts = []
    container = s.find("div", class_="jss124 jss126")
    listings = container.find_all("a")[:numListings]

    for listing in listings:
        if listing != None:
            href = listing.get("href")
            checkListing(href)


# wrapper to get all the listings for the desired searches
def o_main(numPages):
    # MAIN PHOTO VIDEO: https://offerup.com/explore/k/1/3?DISTANCE=5&DELIVERY_FLAGS=p
    # CANON: https://offerup.com/search?q=canon&DISTANCE=5&DELIVERY_FLAGS=p
    # SONY: https://offerup.com/search?DELIVERY_FLAGS=p&DISTANCE=5&q=sony&SORT=-posted
    # NIKON: https://offerup.com/search?DELIVERY_FLAGS=p&DISTANCE=5&q=nikon
    links = [
        "https://offerup.com/search?DELIVERY_FLAGS=p&DISTANCE=30&q=sony&SORT=-posted",
        "https://offerup.com/search?SORT=-posted&DELIVERY_FLAGS=p&DISTANCE=30&q=nikon",
        "https://offerup.com/search?SORT=-posted&DELIVERY_FLAGS=p&DISTANCE=30&q=canon",
        "https://offerup.com/explore/k/1/3?DISTANCE=30&DELIVERY_FLAGS=p",
    ]

    # links = [""]

    for link in links:
        getOnePage(link, numPages)
