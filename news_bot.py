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
    
    news_items = soup.find_all("a", class_="news__item")
    news = []
    for item in news_items:
        title = item.text.strip()
        link = item["href"]
        if not link.startswith("http"):
            link = f"https://it.tlscontact.com{link}"
        news.append((title, link))
    return news

async def send_notification(news):
    for title, link in news:
        message = f"📰 NEWS: {title}\nLink: {link}"
        await bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    global processed_news
    while True:
        try:
            news = await get_news()
            
            new_news = [item for item in news if item[1] not in processed_news]
            
            if new_news:
                await send_notification(new_news)
                processed_news.update([item[1] for item in new_news])
            
        except Exception as e:
            print(f"Error: {e}")
        
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
