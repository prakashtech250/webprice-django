from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime

SEND_NOTIFICATION = True

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M')

default_info = {
    'TITLE': 'Smart Watches for Women, 1.91" HD Fitness Tracker Watch with Blood Pressure/Heart Rate Monitor, Bluetooth 5.3 Make Calls Smart Watch for Android/iOS Phones, IP68 Waterproof Fitness Watch for Women',
    'URL': 'https://www.amazon.com/dp/B0CJN5CBG9',
    'PRICE': '45.57',
    'CURRENCY': '$',
    'AVAILABILITY': 'YES',
    'ASIN': 'B0CJN5CBG9',
    'IMAGE': 'https://m.media-amazon.com/images/I/81v5g3tFvbL._AC_SX425_.jpg',
    'DOMAIN': 'www.amazon.com'
}

default_msg = 'This notification is send from the website to verify discord webhook url'

def send_notification(webhook, msg=default_msg,info=default_info):
    title = info['TITLE']
    url = info['URL']
    if info['AVAILABILITY'] == 'YES':
        availability = ':white_check_mark:'
    else:
        availability = ':x:'
    price = info['PRICE']
    currency = info['CURRENCY']
    if 'nl' in info['DOMAIN'].lower():
        country = ':flag_nl:'
    elif 'de' in info['DOMAIN'].lower():
        country = ':flag_de:'
    elif 'com' in info['DOMAIN'].lower():
        country = ':flag_us:'
    else:
        country = ':qesution:'
    asin = info.get('ASIN', ':question:')
    image = info.get('IMAGE', None)
    if price:
        if currency:
            price = f'{currency}{price}'
        else:
            pass
    else:
        price = ':question:'
    delivery = info.get('DELIVERY_DATE', ':question:')
    if SEND_NOTIFICATION:
        webhook = DiscordWebhook(url=webhook, rate_limit_retry=True)
        embed = DiscordEmbed(title=title, url=url ,color='03b2f8')
        embed.set_thumbnail(url=image)
        embed.set_author(name="prakash", url="")
        embed.set_timestamp()
        embed.add_embed_field(name='Status', value=msg, inline=False)
        embed.add_embed_field(name='ASIN', value=asin, inline=True)
        embed.add_embed_field(name="Price", value=price, inline=True)
        embed.add_embed_field(name="Country", value=country, inline=True)
        embed.add_embed_field(name="Availability", value=availability, inline=True)
        # embed.add_embed_field(name="Delivery", value=delivery, inline=True)
        webhook.add_embed(embed)

        response = webhook.execute()
        if response.status_code == 200:
            print(f'[green]{time_now()},[/green] Notification has been sent to discord.')
            return True
        else:
            print(f'[red]{time_now()},[/red] Error on sending notification to discord')
            return False