import httpx
from bs4 import BeautifulSoup
from rich import print
from datetime import datetime, date, timedelta
import time
from dotenv import load_dotenv
import psycopg2
import os

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

def main():
    conn = connect_database()
    domains_dict = get_domains(conn)
    products = get_products(conn)
    for product in products:
        product['domain_url'] = get_domainUrl(product['domain_id'], domains_dict)
        print(product)
    pass

if __name__=="__main__":
    main()