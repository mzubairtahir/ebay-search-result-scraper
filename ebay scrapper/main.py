from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd


# ===============================

# enter name of product that you want to search on ebay
search_query = "mouse for laptop"

total_pages = 5  #<--- Total pages you want to scrape?


Headless=False  #opening scraper without gui browser


# =================================

search_query = '+'.join(search_query.split())

finalData = []

# =========================================


def parsing_results(soup):
    allResults = soup.find_all('div', class_='s-item__wrapper clearfix')
    for card in allResults:

        try:
            cardLink = card.find('a', class_='s-item__link').get('href')
        except:
            cardLink = None

        try:
            heading = card.find(
                'span', {'role': 'heading'}).get_text(strip=True)
        except:
            heading = None

        try:

            status = card.find('span', class_='SECONDARY_INFO').get_text(
                strip=True)  # Pre owned or brand new
        except:
            status = None

        try:

            price = card.find(
                'span', class_='s-item__price').get_text(strip=True)
        except:
            price = None

        try:
            sellerInfo = card.find(
                'span', class_='s-item__seller-info-text').get_text(strip=True)

        except:
            sellerInfo = None

        try:
            itemLocation = card.find(
                'span', class_='s-item__location s-item__itemLocation').get_text(strip=True)
        except:
            itemLocation = None

        finalData.append(
            {
                'Item link': cardLink,
                'Heading': heading,
                'Status': status,
                'Price': price,
                'Seller info': sellerInfo,
                'Item Location': itemLocation
            }
        )


with sync_playwright() as p:
    browser = p.chromium.launch(headless=Headless)
    new_page = browser.new_page()
    for page in range(1, total_pages+1):
        link = f"https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={search_query}&_sacat=0&_pgn={page}"
        new_page.goto(link, timeout=100000)

        # main div in which our all the results are present

        resultsSection = new_page.query_selector(
            '#mainContent')  # getting element by its id
        html = resultsSection.inner_html()
        soup = BeautifulSoup(html, 'html.parser')
        parsing_results(soup)


df = pd.DataFrame(data=finalData)
df.to_excel('output.xlsx', index=False)
