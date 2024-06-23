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
PRODUCT_TABLE = 'dashboard_productsdb'
CURRENCY_TABLE = 'dashboard_currencyrate'

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
                randtime = random.randint(1,10)
                time.sleep(randtime)
                if 'add.html' not in url:
                    break
        except Exception as e:
            print(f'Error [REQUEST]: {e}', 0)
            randtime = random.randint(1,10)
            time.sleep(randtime)
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

def get_domains(cur):
    cur.execute(f'SELECT * FROM {CURRENCY_TABLE}')
    results = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    results_dict = []
    for row in results:
        row_dict = dict(zip(columns, row))
        results_dict.append(row_dict)
    return results_dict

def get_products(cur):
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
                price, currency = convert_price_format(price_text)
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
            price, currency = convert_price_format(price_text)
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

def update_data(cur, product, info):
    try:
        record_id = product['id']
        last_title = product['title']
        last_price = product['price']
        last_image = product['image_url']
        
        new_title = info['title']
        new_price = info['price']
        new_image = info['image_url']

        select_query = f"""
        SELECT title, price, last_checked_price, image_url 
        FROM {PRODUCT_TABLE}
        WHERE id = %s;
        """
        cur.execute(select_query, (record_id,))
        current_details = cur.fetchone()
        if current_details:
            update_query = f"""
            UPDATE {PRODUCT_TABLE}
            SET price = %s,
                last_checked_price = %s,
                title = %s,
                image_url = %s
            WHERE id = %s;
            """

            cur.execute(update_query, (
                new_price, 
                last_price, 
                new_title, 
                new_image, 
                record_id
            ))
            print_info(f"Record with ID {record_id} has been updated.")
        else:
            print_info(f"No record found with ID {record_id}.")
    except Exception as e:
        print_info(f"Error while updating data in PostgreSQL: {e}", 0)

def main():
    conn = connect_database()
    cur = conn.cursor()
    domains_dict = get_domains(cur)
    products = get_products(cur)
    for product in products:
        product['domain_url'] = get_domainUrl(product['domain_id'], domains_dict)
        info = details_via_cart(product)
        update_data(cur, product, info)
        conn.commit()
    if conn:
        cur.close()
        conn.close()
        print_info("PostgreSQL connection is closed")
    pass

if __name__=="__main__":
    main()