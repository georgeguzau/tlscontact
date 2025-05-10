import requests
from bs4 import BeautifulSoup
import asyncio
from aiogram import Bot, Dispatcher

URL = "https://it.tlscontact.com/by/msq/page.php?pid=news&l=ru"
BOT_TOKEN = "8041916387:AAGEQF3nfSL0TZZPOfSPs2aY50j1LpQR2SY"
CHAT_ID = 572006051
CHECK_INTERVAL = 60
MAX_MESSAGE_LENGTH = 4096

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

processed_news = set()

async def get_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    news_items = soup.find_all("h3")
    news = [item.get_text(strip=True) for item in news_items]
    return news

def split_message(message, max_length=MAX_MESSAGE_LENGTH):
    """Разбивает сообщение на части, не превышающие лимит."""
    lines = message.split('\n')
    chunks = []
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 < max_length:
            current_chunk += line + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

async def send_notification(new_titles):
    if new_titles:
        full_message = "📰 Новые новости:\n\n" + "\n".join([f"- {title}" for title in new_titles])
        message_parts = split_message(full_message)

        for part in message_parts:
            await bot.send_message(chat_id=CHAT_ID, text=part)
            await asyncio.sleep(1.5)

async def main():
    global processed_news
    while True:
        try:
            current_news = await get_news()
            new_titles = [title for title in current_news if title not in processed_news]

            if new_titles:
                await send_notification(new_titles)
                processed_news.update(new_titles)

        except Exception as e:
            print(f"Ошибка: {e}")

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
