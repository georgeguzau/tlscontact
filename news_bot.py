import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Настройки
URL = "https://it.tlscontact.com/by/msq/page.php?pid=news"  # Сайт для проверки
BOT_TOKEN = "7593192564:AAFwcc6SI4fhhTBOR7uSjxi9KOiUClZXR6Y"  # Токен вашего бота
CHAT_ID = 572006051           # ID вашего чата
CHECK_INTERVAL = 60   

# Инициализация бота
bot = Bot(token=BOT_TOKEN)

# Список обработанных новостей
processed_news = set()

# Асинхронная функция для получения новостей
async def get_news():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Парсим список новостей
    news_items = soup.find_all("a", class_="news__item")  # Уточните класс, если он отличается
    news = []
    for item in news_items:
        title = item.text.strip()
        link = item["href"]  # Если ссылка относительная, нужно добавить домен
        if not link.startswith("http"):
            link = f"https://it.tlscontact.com{link}"
        news.append((title, link))
    return news

# Асинхронная функция для отправки уведомлений
async def send_notification(news):
    for title, link in news:
        message = f"📰 Новая новость: {title}\nСсылка: {link}"
        await bot.send_message(chat_id=CHAT_ID, text=message)

# Основной асинхронный цикл
async def main():
    global processed_news
    while True:
        try:
            # Получаем новости
            news = await get_news()
            
            # Находим новые новости
            new_news = [item for item in news if item[1] not in processed_news]
            
            # Если есть новые новости, отправляем уведомления
            if new_news:
                await send_notification(new_news)
                processed_news.update([item[1] for item in new_news])
            
        except Exception as e:
            print(f"Ошибка: {e}")
        
        # Ожидаем перед следующей проверкой
        await asyncio.sleep(CHECK_INTERVAL)

# Запускаем асинхронный главный цикл
if __name__ == "__main__":
    asyncio.run(main())

