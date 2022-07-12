from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as fmt

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import urlextract

from loader import dp, bot
from config.config import admin_id
from keyboards.keyboard import  key_k_1, key_k_0, key_k_2, main_menu, cancel_btn, main_menu_admin_1

from db.db_api import add_user, count_user, get_articles, get_callback, get_callback_articles

#......................КОМАНДА СТАРТ......................
async def cmd_start(message: types.Message):
    photo_main = open('image/cryptolib.png', 'rb')
    if message.from_user.id == admin_id:   
        await message.answer_photo(caption="<b>📚Добро пожаловать в CryptoLib, пожалуйста соблюдайте тишину🤫</b>",photo=photo_main, reply_markup=main_menu_admin_1)
    else:
        await message.answer_photo(caption="<b>📚Добро пожаловать в CryptoLib, пожалуйста соблюдайте тишину🤫</b>",photo=photo_main, reply_markup=main_menu)
    if message.from_user.id != admin_id:
        add_user(message.from_user.id)


#......................КНОПКА ИНФО......................
async def btn_info(message: types.Message):
    photo_main = open('image/info.png', 'rb')
    await message.answer_photo(caption=f"<b>📚CryptoLib💸 - нужная информация всегда под рукой🔥\n\n👨‍👨‍👦Ботом уже воспользовались {count_user()} юзеров🤯\n\n👨‍🚀Библиотекарь/Создатель - @VellBell69🧛‍♂️\n\n📎О багах, ошибках сообщать Библиотекарю⚙️\n\n🤗Я буду очень рад если мой бот, был вам полезным и помог🖖\n\n🙄Но также я буду ещё больше рад если ты поддержишь создателя в такое не лёгкое время, отправив пару шекелей по адресам ниже⬇️(отправишься во вкладку Спонсоры)😳</b>", photo=photo_main)
    await message.answer(text="<b>🦊Metamask - </b><code>0xd47020C697001CA045b9B10c7883Ff768b567ff1</code>⠀\n\n<b>⛄️Phantom - </b><code>7qy9TNesDMwHniqo8BKTPm7yZ71YghkBD1aYBRBN9eEX</code>\n\n<b>💎TronLink - </b><code>TKzhJrZgjq7q4LM95igjJPiJRtCfkTjs71</code>")

#......................КНОПКА СПОНСОРЫ......................
async def btn_sponsor(message: types.Message):
    photo_main = open('image/sponsors.png', 'rb')
    await message.answer_photo(caption="<b>Cпонсоров пока нет 😔</b>", photo=photo_main)

#......................КНОПКА КАТАЛОГ......................
#Открыть каталог
async def btn_katalog(message: types.Message):
    photo_main = open('image/catalog.png', 'rb')
    await message.answer_photo(photo=photo_main)
    await message.answer(text="<b>🍭Каталог статей, мануалов на любой вкус🍢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\nЕсли не переходит в какую либо категорию либо в пост, повторите попытку через 10мин.</b>", reply_markup=key_k_0())

#Открыть содержимое категории
async def btn_kategory(call: types.CallbackQuery):
    data = call.data
    await call.message.edit_text("<b>🍭Каталог статей, мануалов на любой вкус🍢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\nЕсли не переходит в какую либо категорию либо в пост, повторите попытку через 10мин.</b>", reply_markup=key_k_1(data)) 
    await call.answer()

#Открыть содержимое статьи
async def btn_article(call: types.CallbackQuery):
    data = get_articles(call.data)
    name = data[0][3]
    avtor = data[0][4]
    description = data[0][6]
    link = data[0][5]
    await call.message.edit_text(f"<b>{fmt.hide_link(link)}{name}\n\n👨‍🚀Автор: {avtor}\n\n📜{description}</b>", reply_markup=key_k_2(call.data))
    


#Кнопка назад
async def btn_back_lvl0(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=key_k_0()) 
    await call.answer()







# .....................КНОПКА ПРЕДЛОЖИТЬ МАТЕРИАЛ......................
extractor = urlextract.URLExtract()

class HelpUs(StatesGroup):
    waiting_for_link = State()

async def btn_help_us(message: types.Message):
    photo_main = open('image/material.png', 'rb')
    await message.answer_photo(photo=photo_main, caption="<b>Отправь боту ссылку на материал 😁</b>",reply_markup=cancel_btn )
    await HelpUs.waiting_for_link.set()

async def send_to_admin(message: types.Message, state: FSMContext):
    urls = extractor.find_urls(message.text)
    if message.text != "❌Отменить":
        if urls == []:
            await message.answer("<b>Пожалуйста, отправь сообщение с <u>ссылкой</u>🙏🏻</b>")
            return
            
        await bot.send_message(admin_id, f"<b>@{message.from_user.username}, предложил {message.text}</b>")
        await message.answer("<b>Данные отправлены! Спасибо за помощь ☺️</b>", reply_markup=main_menu)
    await state.finish()

async def btn_cancel(message: types.Message, state:FSMContext):
    if message.from_user.id == admin_id:
        await message.reply("<b>Ждём твоё предложение в другой раз 🙄</b>",reply_markup=main_menu_admin_1 )
    else:
        await message.reply("<b>Ждём твоё предложение в другой раз 🙄</b>",reply_markup=main_menu ) 
    await state.finish()

#......................ПОДПИСКА НА БОТА......................

async def subscribe(message: types.Message):
    await message.reply("Подписка на обновления активирована!")

async def unsubscribe(message: types.Message):
    await message.reply("Подписка на обновления деактивирована")


#......................РЕГТСТРАЦИЯ ХЕНДЛЕРОВ......................
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(btn_info, Text(equals="💎Инфо/Контакт"))
    dp.register_message_handler(btn_sponsor, Text(equals="😎Спонсоры"))

    dp.register_message_handler(btn_katalog, Text(equals="🗂Каталог"))
    dp.register_callback_query_handler(btn_kategory, Text(equals=get_callback()))
    dp.register_callback_query_handler(btn_article, Text(equals=get_callback_articles()))
    dp.register_callback_query_handler(btn_back_lvl0, Text(equals="back_to_lvl_0"))

    dp.register_message_handler(btn_cancel, Text(equals="❌Отменить"), state="*")
    dp.register_message_handler(btn_help_us, Text(equals="💁Предложить материал"))
    dp.register_message_handler(send_to_admin, state=HelpUs.waiting_for_link)

    dp.register_message_handler(subscribe, commands="subscribe")
    dp.register_message_handler(unsubscribe, commands="unsubscribe")