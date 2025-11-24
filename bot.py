import requests
from bs4 import BeautifulSoup
import time
import telebot

BOT_TOKEN = "ВАШ_ТОКЕН_ТУТ"
CHANNEL_ID = "@ВАШ_КАНАЛ_ТУТ"
SEARCH_URL = "https://realtor.ua/arenda-kvartir/?city=20"  # Дніпро

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
            url = "https://realtor.ua" + link["href"]
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
                text = format_message(ad)
                bot.send_message(CHANNEL_ID, text)
                sent_ads.add(ad["url"])

        time.sleep(300)

if name == "__main__":
    main()
