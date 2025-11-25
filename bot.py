import requests
from bs4 import BeautifulSoup
import time
import telebot

BOT_TOKEN = "8431947947:AAF4P85SFCf5iCp7gE3cF1UuqwXcw7q69_o"
CHANNEL_ID = "@orendadp"   # правильно
SEARCH_URL = "https://rieltor.ua/dnepr/flats-rent/?price_min=13000&radius=20&sort=-default"

bot = telebot.TeleBot(BOT_TOKEN)

sent_ads = set()

def parse_realtor():
    response = requests.get(SEARCH_URL, headers={
        "User-Agent": "Mozilla/5.0"
    })

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(".catalog-card")

    results = []

    for item in items:
        title = item.select_one(".catalog-card-media-title")
        price = item.select_one(".catalog-card-price")
        link = item.select_one("a")

        if title and price and link:
            href = link.get("href")
            if href:
                url = "https://rieltor.ua" + href
                results.append({
                    "title": title.text.strip(),
                    "price": price.text.strip(),
                    "url": url
                })

    return results

def format_message(ad):
    return f"""
🏠 {ad['title']}
💵 {ad['price']}

🔗 Деталі: {ad['url']}
"""

def main():
    while True:
        ads = parse_realtor()

        for ad in ads:
            if ad["url"] not in sent_ads:
                bot.send_message(CHANNEL_ID, format_message(ad))
                sent_ads.add(ad["url"])

        time.sleep(300)

if name == "__main__":
    main()
