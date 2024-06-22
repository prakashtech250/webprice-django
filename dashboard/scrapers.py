import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import re
import time
import os
from dotenv import load_dotenv
import random

load_dotenv()
API = os.getenv('SCRAPER_API')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json'
}

USER_AGENTS = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20190101 Firefox/70.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
        ]

def _requests(url):
    # url = 'https://www.amazon.com/dp/B0D676886N'
    HEADERS['Referer'] = url
    HEADERS['Authority'] = 'www.amazon.com'
    HEADERS['User-Agent'] = get_UA()
    # payload = {'api_key': API, 'url': url}
    # r = requests.get('https://api.scraperapi.com', params=payload, headers=headers)
    while True:
        try:
            r = requests.get(url, headers=HEADERS)
            if r.status_code == 200:
                break
        except Exception as e:
            print(f'Error: {e}')
            time.sleep(3)
            return None
    return r

def get_UA():
    result = random.choice(USER_AGENTS)
    if os.path.exists('userAgent.txt'):
        with open('userAgent.txt', 'r') as f:
            ua = f.readlines()
            ua = [x.strip() for x in ua]
            result = random.choice(ua)
    return result


def _soup(response):
    return BeautifulSoup(response.text, 'html.parser')

def convert_price_format(price_str):
    # Remove any whitespace around the price string
    price_str = price_str.strip()

    # Regular expressions for detecting currency symbols
    currency_pattern = re.compile(r'^(?P<currency>[^\d]+)?(?P<price>[\d,.]+)(?P<currency2>[^\d]+)?$')
    match = currency_pattern.match(price_str)
    
    if not match:
        raise ValueError("The price format is not recognized")

    currency = match.group('currency') if match.group('currency') else match.group('currency2')
    price = match.group('price')

    # Check the last three characters to determine the format
    if len(price) >= 3:
        last_char = price[-1]
        second_last_char = price[-2]
        third_last_char = price[-3]
        
        # Check if the second last character is a dot or a comma
        if second_last_char == '.' and last_char.isdigit():
            # Price is already in dot format, e.g., 19.95
            return currency, price
        elif second_last_char == ',' and last_char.isdigit():
            # Price is in comma format, e.g., 19,95
            return currency, price.replace(',', '.')
        elif ',' in price and '.' in price:
            # Determine which one is used as the decimal separator by looking at the last three characters
            if price.rfind(',') > price.rfind('.'):
                # The comma is likely used as the decimal separator
                return currency, price.replace('.', '').replace(',', '.')
            else:
                # The dot is likely used as the decimal separator
                return currency, price.replace(',', '')

    # Regular expressions to match the common formats
    comma_format = re.compile(r'^\d{1,3}(,\d{3})*,\d{2}$')
    dot_format = re.compile(r'^\d{1,3}(\.\d{3})*\.\d{2}$')

    # Check if the price is in comma format
    if comma_format.match(price):
        converted_price = price.replace(',', '.')
        return converted_price, price
    
    # Check if the price is already in dot format
    elif dot_format.match(price):
        return currency, price
    else:
        return None, 0

def get_data(asin, domain):
    domain_url = f"{domain}"
    product_url = urljoin(domain_url,f'/gp/aws/cart/add.html?ASIN.1={asin}')
    product_url = unquote(product_url).replace('\u200e', '')
    print(product_url)
    response = _requests(product_url)
    if response:
        soup = _soup(response)
        title = soup.find(class_='sc-product-title')
        if title:
            title = title.get_text().strip()
        price = soup.find(class_='sc-product-price')
        if price:
            price_text = price.get_text().strip()
            price, currency = convert_price_format(price_text)
        else:
            price, currency = 0, None
        imageUrl = soup.select_one('.sc-product-link img')
        if imageUrl:
            imageUrl = imageUrl.get('src')
        
        info = {
            'asin': asin,
            'title': title,
            'price': price,
            'image_url': imageUrl,
            'currency': currency,
        }
        print(info)
        return info
    else:
        return None
