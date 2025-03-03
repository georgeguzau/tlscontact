import requests
from bs4 import BeautifulSoup
import asyncio
from aiogram import Bot, Dispatcher

URL = "https://it.tlscontact.com/by/msq/page.php?pid=news&l=ru"
BOT_TOKEN = "8041916387:AAGEQF3nfSL0TZZPOfSPs2aY50j1LpQR2SY"
CHAT_ID = 572006051
CHECK_INTERVAL = 60

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хранилище обработанных новостей
processed_news = set()

async def get_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    # Ищем все теги <h3> на странице
    news_items = soup.find_all("h3")

    news = []
    for item in news_items:
        title = item.get_text(strip=True)  # Извлекаем текст из <h3>
        news.append(title)
    return news

async def send_notification(new_titles):
        if new_titles:
            message = "📰 Новые новости:\n\n" + "\n".join([f"- {title}" for title in new_titles])
            await bot.send_message(chat_id=CHAT_ID, text=message)
            await asyncio.sleep(1.5)  # Задержка в 1.5 секунды между сообщениями

async def main():
    global processed_news
    while True:
        try:
            # Получаем текущие заголовки новостей
            current_news = await get_news()

            # Определяем новые заголовки
            new_titles = [title for title in current_news if title not in processed_news]

            # Если есть новые заголовки, отправляем уведомления
            if new_titles:
                await send_notification(new_titles)
                processed_news.update(new_titles)

        except Exception as e:
            print(f"Ошибка: {e}")

        # Ожидаем перед следующей проверкой
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())