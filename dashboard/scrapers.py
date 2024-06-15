import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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

def float_price(price_text):
    pattern0 = r"\d+\,\d+"
    pattern1 = r"\d+\.\d+"
    pattern2 = r"\d+"
    currency_pattern = r"[^\d,.]+"
    found0 = re.search(pattern0, price_text)
    found1 = re.search(pattern1, price_text)
    found2 = re.search(pattern2, price_text)
    currency_found = re.search(currency_pattern, price_text)
    if found0:
        price = found0.group(0).replace(',','.')
    elif found1:
        price = found1.group(0)
    elif found2:
        price = found2.group(0)
    else:
        price = 0
    try:
        price = int(price)
    except:
        price = float(price)
    if currency_found:
        currency = currency_found.group(0).strip()
    else:
        currency = ''
    return price, currency

def get_data(asin, domain):
    domain_url = f"https://www.amazon.{domain}"
    product_url = urljoin(domain_url,f'/gp/aws/cart/add.html?ASIN.1={asin}')
    response = _requests(product_url)
    if response:
        soup = _soup(response)
        title = soup.find(class_='sc-product-title')
        if title:
            title = title.get_text().strip()
        price = soup.find(class_='sc-product-price')
        if price:
            price_text = price.get_text().strip()
            price, currency = float_price(price_text)
        else:
            price = 0
        imageUrl = soup.select_one('.sc-product-link img')
        if imageUrl:
            imageUrl = imageUrl.get('src')
        info = {
            'asin': asin,
            'title': title,
            'price': price,
            'image_url': imageUrl
        }
        # print(imageUrl)
        return info
    else:
        return None
