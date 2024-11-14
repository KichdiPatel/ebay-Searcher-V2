# Ebay Searcher V2

## The Project

In this project, I created a scraper that looks for inventory I can sell on my eBay store through channels of Craigslist, Goodwill auctions, and OfferUp. I no longer sell on eBay so this project has not been updated since spring of 2024. So, with some slight changes to the scraping of each website, this should be fully functional for today's sites. Sourcing is a pain, and a very monotonous task. So, using this code, sourcing time is reduced and that time can be better spent on other tasks. I specifically only sold camera equipment, so all of the files are very targeted for that niche.

For this project I utilize playwright to scrape the websites, and chatGPT to analyze the listings.

## The Code

The code all runs from the app.py file. In here, you can call the craigslist, offerup, and goodwill scripts individually.

eBay.py is used to write the functinality for getting the average selling price of a specific keyword on eBay. So, the code scrapes the eBay sold listings page with some other filters, and returns the average price for a search with outliers removed.

craigslist.py is the code for scraping craigslist. Based on the structure of the site, I search through the camera listings, open each listing page to then scrape the title, description, and price. From there, the title and description are ran through chatGPT to get the keyword(s) of the products in the listing if multiple things are being sold. The get_breakeven() function is called with the specific keywords to get the breakeven prices, and this is compared with the price of the listing to either add to possibilities.csv, needCheck.csv, or to be ignored.

goodwill.py is the code for scraping the goodwill acutions. Based on the site, I have specific category links manually added that I wanted to search through. On these pages, each listing is scraped, and the same process as craigslist.py is run to then either add each listing to possibilities.csv, needCheck.csv, or be ignored.

offerUp.py is the code for scraping offerUP. Based on the site, I have specific keywords I search for on the website. On these pages, each listing is scraped, and again using chatGPT and the same process as craigslist.py, each listing is either added to possibilities.csv, needCheck.csv, or ignored.

helpers.py contains addToPossibilities() and addToCheck() where possible good inventory is added to possibilities.csv or if the program is unsure, it will add it to needCheck.csv
