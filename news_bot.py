import requests
from bs4 import BeautifulSoup
import asyncio
from aiogram import Bot, Dispatcher

URL = "https://it.tlscontact.com/by/msq/page.php?pid=news&l=ru"
BOT_TOKEN = "7593192564:AAFwcc6SI4fhhTBOR7uSjxi9KOiUClZXR6Y"
CHAT_ID = 572006051
CHECK_INTERVAL = 60
ALLOWED_USER_ID = 572006051

# Инициализация бота
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
    for title in new_titles:
        if CHAT_ID == ALLOWED_USER_ID:
            await bot.send_message(chat_id=CHAT_ID, text=f"📰 Новая новость: {title}")
        else:
            print("Попытка отправки сообщения неавторизованному пользователю")

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