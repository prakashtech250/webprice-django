import httpx
from bs4 import BeautifulSoup
from rich import print
from datetime import datetime, date, timedelta
import time
from dotenv import load_dotenv
import psycopg2
import os
import random
import re
from scrapingbee import ScrapingBeeClient
import calendar
from urllib.parse import urljoin, urlencode, unquote

load_dotenv()

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
USE_PROXY = False

def get_UA():
    result = random.choice(USER_AGENTS)
    if os.path.exists('userAgent.txt'):
        with open('userAgent.txt', 'r') as f:
            ua = f.readlines()
            ua = [x.strip() for x in ua]
            result = random.choice(ua)
    return result

def request_via_proxy(url):
    client = ScrapingBeeClient(api_key=os.getenv('SCRAPING_BEE'))
    response = client.get(url)
    print_info(f'[Proxy] Url: {url}, Status: {response.status_code}')
    return response

def _requests(url):
    HEADERS['Referer'] = url
    authority = url.replace('https://','').split('/')[0]
    HEADERS['Authority'] = authority
    while True:
        try:
            HEADERS['User-Agent'] = get_UA()
            response = httpx.get(url, headers=HEADERS)
            if response.status_code == 200:
                print_info(f'Url: {url}, Status: {response.status_code}')
                break
            elif response.status_code == 404:
                print_info(f'Url: {url}, Status: {response.status_code}', 0)
                return None 
            else:
                print_info(f'Url: {url}, Status: {response.status_code}', 0)
                randtime = random.randint(5,10)
                time.sleep(randtime)
                if 'add.html' not in url:
                    break
        except Exception as e:
            print(f'Error [REQUEST]: {e}', 0)
            time.sleep(5)
    return response

def _soup(response):
    return BeautifulSoup(response.text, 'html.parser')

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

def print_info(msg, status=1):
    if status == 1:
        print(f'[green]{time_now()}[/green] {msg}')
    elif status == 0:
        print(f'[red]{time_now()} {msg} [/red]')
    elif status == 2:
        print(f'[red]{time_now()} {msg} [/red]', end="\r")

def connect_database():
    conn = psycopg2.connect(database = os.getenv('PGNAME'), 
                            user = os.getenv('PGUSER'), 
                            host= os.getenv('PGHOST'),
                            password = os.getenv('PGPASS'),
                            port = os.getenv('PGPORT'))
    return conn

def get_domains(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM dashboard_currencyrate')
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    results_dict = []
    for row in results:
        row_dict = dict(zip(columns, row))
        results_dict.append(row_dict)
    return results_dict

def get_products(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM dashboard_productsdb')
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    results_dict = []
    for row in results:
        row_dict = dict(zip(columns, row))
        results_dict.append(row_dict)
    return results_dict

def get_domainUrl(productId, domains_dict):
    domain_url = None
    for domain_dict in domains_dict:
        if productId == domain_dict['id']:
            domain_url =  domain_dict['domain_url']
    return domain_url

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

def get_delivery_dates(delivery_text):
    delivery_text = delivery_text.lower()
    month = None
    months = list(calendar.month_name)[1:]
    for mon_index, mon in enumerate(months):
        mon_index += 1
        if mon.lower() in delivery_text:
            month = mon_index
            break
    day_pattern = r'(\d+)-(\d+)'
    day_match = re.search(day_pattern, delivery_text)
    if day_match:
        start_day = int(day_match.group(1))
        end_day = int(day_match.group(2))
    else:
        # If no range is found, try to find a single day
        day_pattern = r'\d+'
        day_found = re.findall(day_pattern, delivery_text)
        if day_found:
            start_day = end_day = int(day_found[0])
        else:
            return None
    if month:
        first_date = date(2024, month, start_day)
        last_date = date(2024, month, end_day)
        return first_date, last_date
    else:
        return None

def _details(product):
    asin = product['asin']
    domain_url = product['domain_url']
    price = product['price']
    currency = None
    delivery_date = None

    product_url = f'{domain_url}/dp/{asin}'
    
    if USE_PROXY:
        response = request_via_proxy(product_url)
    else:
        response = _requests(product_url)
    if response:
        soup = _soup(response)
        title = soup.find(id="productTitle")
        if title:
            title = title.get_text().strip()

        imageUrl = soup.select_one('#imgTagWrapperId img')
        if imageUrl:
            imageUrl = imageUrl.get('src')

        price_div = soup.find(id='corePrice_feature_div')
        if price_div:
            price_text = price_div.find(class_='a-offscreen')
            if price_text:
                price_text = price_text.get_text().strip()
                price, currency = float_price(price_text)
                delivery_block = soup.find(id="deliveryBlockMessage")
                if delivery_block:
                    delivery_text = delivery_block.find(class_='a-text-bold')
                    if delivery_text:
                        delivery_text = delivery_text.get_text()
                        delivery_4m_function = get_delivery_dates(delivery_text)
                        if delivery_4m_function:
                            fist_date, last_date = delivery_4m_function
                            delivery_date = last_date
        if price:
            availability = 'YES'
        else:
            availability = 'NO'

        info = {
            'title': title,
            'price': price,
            'image_url': imageUrl,
            'currency': currency,
            'delivery_date': delivery_date,
            'availability': availability
        }

    else:
        info = None
    return info

def details_via_cart(product):
    asin = product['asin']
    domain_url = product['domain_url']
    cart_url = urljoin(domain_url,f'/gp/aws/cart/add.html?&ASIN.1={asin}')
    cart_url = unquote(cart_url).replace('\u200e', '')
    response = _requests(cart_url)
    # response = request_via_proxy(cart_url)
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
            price, currency = 0, None
        if price:
            availability = 'YES'
        else:
            availability = 'NO'
        imageUrl = soup.select_one('.sc-product-link img')
        if imageUrl:
            imageUrl = imageUrl.get('src')

        info = dict()
        info['title'] = title
        info['price'] = price
        info['currency'] = currency
        info['image_url'] = imageUrl
        info['availability'] = availability
    else:
        info = None
    return info

def main():
    conn = connect_database()
    domains_dict = get_domains(conn)
    products = get_products(conn)
    for product in products:
        product['domain_url'] = get_domainUrl(product['domain_id'], domains_dict)
        info = details_via_cart(product)
        print(info)
        # break
    pass

if __name__=="__main__":
    main()