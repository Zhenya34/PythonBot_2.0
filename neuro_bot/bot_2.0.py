from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from bs4 import BeautifulSoup as BS  
from pyowm import OWM
import requests
import logging
import random

# токены
token1 = "6036818911:AAF7a2Z0ZwJgZGMnDi_7HKXb0e-YTOL4XYI"
owm = OWM('abee71f5d838cde57852ed360680f00a')

#настройка логов 
logging.basicConfig(level = logging.INFO)

bot = Bot(token=token1)
dp = Dispatcher(bot)

# создание памяти для хранения состояния 
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class WeatherForm(StatesGroup):
    city = State()


# обработка команды старт создание кнопок 
@dp.message_handler(commands=['start']) 
async def greetings(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🎲 рандом')
    item2 = types.KeyboardButton('🌍 новости')
    item3 = types.KeyboardButton('🌧 погода')
    item4 = types.KeyboardButton('⛩ аниме')
    item6 = types.KeyboardButton('💵 курс валют')
    item7 = types.KeyboardButton('❔ помощь')

    markup.add(item1, item2, item3, item4, item6, item7)

    sti = open('C:/Users/Asus/Desktop/mycode.py/CHAT_BOT.py/static/hello.tgs', 'rb')
    await bot.send_sticker(message.chat.id, sti)

    await message.answer("приветик", reply_markup=markup)

# основной функционал 
@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    if message.text == '🎲 рандом':
        await message.answer(random.randint(0, 100))

    elif message.text == '🌍 новости':
        markup = types.InlineKeyboardMarkup(row_width = 1)
        news1 = types.InlineKeyboardButton('Айти 📱', callback_data = '10')
        news2 = types.InlineKeyboardButton('Игры 🎮', callback_data = '20')
        news3 = types.InlineKeyboardButton('Прочие 🌍', callback_data = '30')
        
        markup.add(news1, news2, news3)
        await message.reply('Выберите любые новости', reply_markup = markup)


    elif message.text == '🌧 погода':
        await message.answer("Введите название города или страны:")
        await WeatherForm.city.set()   

    elif message.text == '⛩ аниме':
        markup = types.InlineKeyboardMarkup(row_width = 2)
        item1 = types.InlineKeyboardButton('Экшен 🔥', callback_data = '01')
        item2 = types.InlineKeyboardButton('Детектив 🔍', callback_data = '02')
        item3 = types.InlineKeyboardButton('Комедия 😁', callback_data = '03')
        item4 = types.InlineKeyboardButton('Романтика ❤️', callback_data = '04')
        item5 = types.InlineKeyboardButton('Ужасы 👻', callback_data = '05')
        item6 = types.InlineKeyboardButton('Фантастика ✨', callback_data = '06')
        item7 = types.InlineKeyboardButton('Драма 💔', callback_data = '07')
        item8 = types.InlineKeyboardButton('Повседневность 💤', callback_data = '08')
        item9 = types.InlineKeyboardButton('Приключения ⚔️', callback_data = '09')
        item10 = types.InlineKeyboardButton('Постапокалиптика 🌋', callback_data = '010')
        item11 = types.InlineKeyboardButton('Спорт ⚽️', callback_data = '011')
        item12 = types.InlineKeyboardButton('Фэнтези 🔮', callback_data = '012')
        item13 = types.InlineKeyboardButton('Киберпанк🤖', callback_data = '013')
        item14 = types.InlineKeyboardButton('Мистика 🎃', callback_data = '014')
        item15 = types.InlineKeyboardButton('Психология 💭', callback_data = '015')
        item16 = types.InlineKeyboardButton('Школа 🔔', callback_data = '016')        
        item17 = types.InlineKeyboardButton('Сёнэн 🧑', callback_data = '017')
        item18 = types.InlineKeyboardButton('Сёдзё 👩', callback_data = '018')
        item19 = types.InlineKeyboardButton('Сэйнэн 👨', callback_data = '019')
        item20 = types.InlineKeyboardButton('Дзёсэй 🧑', callback_data = '020')
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13, item14, item15, item16, item17, item18, item19, item20)
        await message.reply('Выбери жанр аниме', reply_markup = markup)

    elif message.text == '💵 курс валют':
        markup = types.InlineKeyboardMarkup(row_width = 2)
        rate1 = types.InlineKeyboardButton('USD 💵', callback_data = 'usd')
        rate2 = types.InlineKeyboardButton('EUR 💶', callback_data = 'eur')
        rate3 = types.InlineKeyboardButton('RUB 💷', callback_data = 'rub')
        rate4 = types.InlineKeyboardButton('JPY 💴', callback_data = 'jpy')
        markup.add(rate1, rate2, rate3, rate4)
        await message.reply('Выберите валюту', reply_markup = markup)

    elif message.text == '❔ помощь':
        await message.answer('Этот бот может: показывать новости игр айти и Украины, новинки аниме по разным жанрам (всего 21 жанр). Погода в любых городах, курс валют(USD, EUR, RUB, JPY), давать случайное число от 0 до 100.')

@dp.message_handler(state=WeatherForm.city)
async def process_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
        city = data['city']
        try:
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(city)
            w = observation.weather
            t = w.temperature('celsius')['temp']
            await message.answer(f'В городе {city} сейчас температура {t} градусов.')
        except:
            await message.answer(f'Не удалось получить погоду для города {city}. Попробуйте еще раз.')
    await state.finish()


@dp.callback_query_handler(lambda call: call.data in ['usd', 'eur', 'rub', 'jpy'])
async def process_callback_currency(callback_query: types.CallbackQuery):
    try:
        if callback_query.data == 'usd':
            url = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5'
        elif callback_query.data == 'eur':
            url = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5'
        elif callback_query.data == 'rub':
            url = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D1%80%D1%83%D0%B1%D0%BB%D1%8F+%D0%B2+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&oq=%D0%BA%D1%83%D1%80%D1%81+%D1%80%D1%83%D0%B1%D0%BB%D1%8F+%D0%B2+&aqs=chrome.1.69i57j35i39j0i512j0i20i263i512j0i512l6.6165j1j15&sourceid=chrome&ie=UTF-8'
        elif callback_query.data == 'jpy':
            url = 'https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B9%D0%B5%D0%BD+%D0%BA+%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B5&sxsrf=APwXEdewgg0vxIwI4T2wsl01ZcQHBQU1OQ%3A1682424462725&ei=jsJHZJDmK6qK9u8P4Ny32Ag&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B9%D0%B5%D0%BD+&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMgUIABCABDIFCAAQgAQyBQgAEIAEMgoIABCABBAUEIcCMgoIABCABBAUEIcCMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BAgAEEdKBAhBGABQ-wFY-wFg9RRoAXACeACAAYoBiAGKAZIBAzAuMZgBAKABAcgBCMABAQ&sclient=gws-wiz-serp'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BS(response.text, 'html.parser')
        articles_cards_1 = soup.find_all('div', class_='dDoNo ikb4Bb gsrt')
                    
        for article1 in articles_cards_1:
            article_title1 = article1.find('span', class_='DFlfde SwHCTb')
            if article_title1 is not None:
                exchange_rate = float(article_title1.get('data-value'))
                rounded_exchange_rate = round(exchange_rate, 2)
                await bot.send_message(callback_query.from_user.id, str(rounded_exchange_rate) + ' гривен') 
    except:
        await bot.send_message(callback_query.from_user.id, ('Не удалось получить курс валют'))
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda call: call.data in ['10', '20', '30'])
async def process_handled_news(callback_query: types.CallbackQuery):
    try:
        if callback_query.data == '10':            
            
            await bot.send_message(callback_query.from_user.id, ('Новости Айти за ближайшее время'))
            headers = {
                'user-aent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            }
            url = ('https://www.securitylab.ru/news/')
            r = requests.get(url, headers = headers)
            soup = BS(r.text, 'lxml')
            article_cards = soup.find_all('a', class_ = 'article-card')
            
            for article in article_cards:
                article_title = article.find('h2', class_ = 'article-card-title').text.strip()
                article_url = f'https://www.securitylab.ru{article.get("href")}'
                ansver1 = (f'{article_title} {article_url} ')             
                await bot.send_message(callback_query.from_user.id, (ansver1))  
        elif callback_query.data == '20':
            
            await bot.send_message(callback_query.from_user.id, 'Новости Игр за ближайшее время')
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            }
            url = 'https://stopgame.ru/news/all/p1'
            r = requests.get(url, headers=headers)
            soup = BS(r.text, 'html.parser')
            article_cards = soup.find_all('div', {'data-key': True})

            for article in article_cards:
                article_title = article.find('a', {'class': '_title_1tbpr_49'}).text.strip()
                article_url = f"https://stopgame.ru{article.find('a')['href']}"
                answer1 = f"{article_title}\n{article_url}\n"
                await bot.send_message(callback_query.from_user.id, answer1)
        elif callback_query.data == '30':
            
            await bot.send_message(callback_query.from_user.id, ('Прочие новости за ближайшее время'))
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            }
            url = 'https://www.obozrevatel.com/location/ukraina/'
            r = requests.get(url, headers=headers)
            soup = BS(r.text, 'html.parser')
            article_cards = soup.find_all('article', class_='newsImgRowTime')
            for article in article_cards:
                article_title = article.find('a', class_='newsImgRowTime_titleLink').text.strip()
                article_url = f'https://stopgame.ru{article.find("a").get("href")}'
                ansver1 = f'{article_title}\n{article_url}\n'
                await bot.send_message(callback_query.from_user.id, ansver1)
    except:
        await bot.send_message(callback_query.from_user.id, ('Не удалось узнать новости '))
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda call: call.data in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '010', '011', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021'])
async def process_callback_currency(callback_query: types.CallbackQuery):
    try:
        genres_urls = {
            '01': 'https://animestars.org/aniserials/video/action/',
            '02': 'https://animestars.org/aniserials/video/detective/',
            '03': 'https://animestars.org/aniserials/video/comedy/',
            '04': 'https://animestars.org/aniserials/video/romance/',
            '05': 'https://animestars.org/aniserials/video/horror/',
            '06': 'https://animestars.org/aniserials/video/fantastic/',
            '07': 'https://animestars.org/aniserials/video/drama/',
            '08': 'https://animestars.org/aniserials/video/natural/',
            '09': 'https://animestars.org/aniserials/video/adventure/',
            '010': 'https://animestars.org/aniserials/video/postapocalypse/',
            '011': 'https://animestars.org/aniserials/video/sports/',
            '012': 'https://animestars.org/aniserials/video/fantasy/',
            '013': 'https://animestars.org/aniserials/video/cyberpunk/',
            '014': 'https://animestars.org/aniserials/video/mystery/',
            '015': 'https://animestars.org/aniserials/video/psychological/',
            '016': 'https://animestars.org/aniserials/video/school/',
            '017': 'https://animestars.org/aniserials/video/shounen/',
            '018': 'https://animestars.org/aniserials/video/shoujo/',
            '019': 'https://animestars.org/aniserials/video/seinen/',
            '020': 'https://animestars.org/aniserials/video/josei/',
            '021': 'https://animestars.org/aniserials/video/ecchi/'
        }                    
        
        url = genres_urls.get(callback_query.data)
        await bot.send_message(callback_query.from_user.id, ('Новые аниме за выбранными жанрами'))
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        r = requests.get(url, headers=headers)
        soup = BS(r.text, 'html.parser')
        article_cards = soup.find_all('a', class_='poster grid-item d-flex fd-column has-overlay')
        for article in article_cards:
            article_title = article.find('h3', class_='poster__title ws-nowrap').text.strip()
            article_url = f'{article.get("href")}'
            answer = f'{article_title}\n{article_url}'
            await bot.send_message(callback_query.from_user.id, answer)      
    except:
        await bot.send_message(callback_query.from_user.id, ('Не удалось узнать новинки аниме'))
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)    


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

