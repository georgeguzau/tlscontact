import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

URL = "https://it.tlscontact.com/by/msq/page.php?pid=news"
BOT_TOKEN = "7593192564:AAFwcc6SI4fhhTBOR7uSjxi9KOiUClZXR6Y"
CHAT_ID = 572006051
CHECK_INTERVAL = 60   

bot = Bot(token=BOT_TOKEN)

processed_news = set()

async def get_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    
    news_items = soup.find_all("h3")

    news = []
    for item in news_items:
        title = item.text.strip()
        news.append(title)
    return news

async def main():
    global processed_news
    while True:
        try:
            news = await get_news()

            new_titles = [title for title in news if title not in processed_news]

            if new_titles:
                for title in new_titles:
                    await bot.send_message(chat_id=CHAT_ID, text=f"📰 Новая новость: {title}")

                processed_news.update(new_titles)

        except Exception as e:
            print(f"Ошибка: {e}")

        # Ожидание перед следующим запросом
        await asyncio.sleep(CHECK_INTERVAL)
