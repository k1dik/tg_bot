import logging
import geonamescache
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
from currency_converter import CurrencyConverter
from datetime import datetime

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        'Привет! Это бот для просмотра разной полезной информации.\n'
        'Используйте команду /weather для получения текущей погоды.\n'
        'Используйте команду /schedule для получения плана на сегодняшний день.\n'
        'Используйте команду /currency для получения текушего курса валют.\n'
        'Используйте команду /birthday для получения информации о дней рождении друзей.\n'
        'Используйте команду /news для получения информации о самых главных событиях на сегодняшний день.\n'
    )

async def get_weather(update: Update, context: CallbackContext) -> None:
    CITY = 'Moscow'
    Weather_API_KEY = 'dcadaa442527ef3c9a25e034c3fe59a0'
    Weather_URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={Weather_API_KEY}&units=metric"
    response_weather = requests.get(Weather_URL)
    weather = response_weather.json()
    await update.message.reply_text(
        f'Текущая погода в Москве: {weather["weather"][0]["description"]}, {weather["main"]["temp"]}°C'
    )

async def get_currency(update: Update, context: CallbackContext) -> None:
    currency_url = "https://www.cbr-xml-daily.ru/daily_json.js"
    responce = requests.get(currency_url)
    data = responce.json()
    await update.message.reply_text(
        f'1 доллар стоит {data["Valute"]["USD"]["Value"]} рублей'
        )
    
async def get_schedule(update: Update, context: CallbackContext) -> None:
    weekday = datetime.now().strftime('%A')
    schedule = {
        "Monday": "1. Математика\n2. Физика\n3. Программирование",
        "Tuesday": "1. Литература\n2. История\n3. Английский",
        "Wednesday": "1. Химия\n2. Биология\n3. Физкультура",
        "Thursday": "1. География\n2. Обществознание\n3. Информатика",
        "Friday": "1. Экономика\n2. Искусство\n3. Спорт",
        "Saturday": "Выходной",
        "Sunday": "Выходной"
    }
    today_schedule = schedule[weekday]
    await update.message.reply_text(
        f'Сегодня по плану: {today_schedule}'
    )

async def get_birthday(update: Update, context: CallbackContext):
    birthdays = {}
    with open('birthdays.txt', 'r') as file:
        for line in file:
            name, date = line.strip().split(':')
            birthdays[name] = date
    for key, value in birthdays.items():
        if value == datetime.now().strftime('%d.%m.%Y'):
            await update.message.reply_text(
                f'Сегодня день рождения у {key}'
            )
            break
    else:
        await update.message.reply_text(
            'Сегодня день рождения никого нет')

async def get_news(update:Update, context: CallbackContext):
    NEWS_API ='d706577b13f740c08151397a8b35e8ef'
    NEWS_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API}'
    response_news = requests.get(NEWS_URL).json()
    await update.message.reply_text(
        f'Самые главные новости на сегодня:')
    for elem in response_news['articles']:
        await update.message.reply_text(
            f'{elem["author"]}: {elem["description"]} \n Ссылка: {elem["url"]}\n{'-' * 100}')

def main():
    TOKEN = '7250105051:AAG7d3gZNSctrS1JcMTFTvnrGj1E1kbqxM4'

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('weather', get_weather))
    app.add_handler(CommandHandler('currency', get_currency))
    app.add_handler(CommandHandler('schedule', get_schedule))
    app.add_handler(CommandHandler('birthday', get_birthday))
    app.add_handler(CommandHandler('news', get_news))

    app.run_polling()


if __name__ == '__main__':
    main()
