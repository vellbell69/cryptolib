from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from loader import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import aiogram.utils.markdown as fmt
from aiogram.utils.exceptions import BotBlocked

from config.config import admin_id

from keyboards.keyboard import key_cancel, key_confirm, key_k_0_del, key_k_1_del, main_menu_admin_1, main_menu_admin_2, key_k_0_add
from db.db_api import add_item, add_notify_article, del_active_user, del_item, del_notify_article, get_add_category_info, get_all_active_user_id, get_articles, get_del_callback, get_del_callback_articles, get_notify_article

#Смена клавиатуры/Вход в админку
async def set_keyboard(message: types.Message):
    if message.from_user.id == admin_id:
        await message.reply("<b>Добро пожаловать в админку</b>", reply_markup=main_menu_admin_2)
    else:
        pass

async def del_keyboard(message: types.Message):
    if message.from_user.id == admin_id:
        await message.reply("<b>Вы покинули админку</b>", reply_markup=main_menu_admin_1)
    else:
        pass

#Добавление записей
class AddState(StatesGroup):
    waiting_category = State()
    create_category = State()
    waiting_category_code = State()
    waiting_category_name = State()
    waiting_name = State()
    waiting_discription = State()
    waiting_avtor = State()
    waiting_link = State()
    article_post = State()

async def add_article(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("<b>Ты в меню добавления записей</b>", reply_markup=key_cancel())
        await message.answer("<b>В какую категорию добавим?</b>", reply_markup=key_k_0_add())
        await AddState.waiting_category.set()

async def add_article_get_category(call: types.CallbackQuery, state:FSMContext):    
    if call.data != "create_category":
        data = get_add_category_info(call.data)
        await state.update_data(category_name=data[0])
        await state.update_data(category_code=data[1])
        await call.message.answer(f"<b>Ты выбрал категорию  {data[0]}\n\nТеперь введи название для записи:</b>")
        await call.answer()
        await AddState.waiting_name.set()
    else:
        await call.message.answer(f"<b>Введи название для новой категории:</b>")
        await AddState.waiting_category_name.set()

async def add_article_get_category_name(message: types.Message, state:FSMContext):
    await state.update_data(category_name=message.text)
    await message.answer(f"<b>Ты ввёл {message.text}  \n\nТеперь введи название для кода категории:</b>")
    await AddState.waiting_category_code.set()

async def add_article_get_category_code(message: types.Message, state:FSMContext):
    await state.update_data(category_code=message.text)
    await message.answer(f"<b>Ты ввёл {message.text}  \n\nТеперь введи название для записи:</b>")    
    await AddState.waiting_name.set()



async def add_article_get_name(message: types.Message, state:FSMContext):
    await state.update_data(article_name=message.text)
    await message.answer(f"<b>Ты ввёл название '{message.text}'\n\nТеперь введи описание для записи:</b>")
    await AddState.waiting_discription.set()

async def add_article_get_discr(message: types.Message, state:FSMContext):
    await state.update_data(article_discr=message.text)
    await message.answer(f"<b>Ты ввёл описание '{message.text}'\n\nТеперь введи автора материла:</b>")
    await AddState.waiting_avtor.set()

async def add_article_get_avtor(message: types.Message, state:FSMContext):
    await state.update_data(article_avtor=message.text)
    await message.answer(f"<b>Ты ввёл автора '{message.text}'\n\nТеперь введи ссылку:</b>")
    await AddState.waiting_link.set()

async def add_article_get_link(message: types.Message, state:FSMContext):
    await state.update_data(article_link=message.text)
    await message.answer(f"<b>Ты ввёл ссылку '{message.text}'\n\nПредпросмотр:</b>")
    user_data = await state.get_data()
    await message.answer(f"<b>{fmt.hide_link(user_data['article_link'])}{user_data['article_name']}\n\n📚Категория: {user_data['category_name']}\n\n👨‍🚀Автор: {user_data['article_avtor']}\n\n📜{user_data['article_discr']}</b>", reply_markup=key_confirm())
    await AddState.article_post.set()

async def add_article_confirm(message: types.Message, state:FSMContext):
    if message.text == "✅Постим✅":
        user_data = await state.get_data()
        add_item(user_data['category_code'], user_data['category_name'], user_data['article_name'], user_data['article_avtor'], user_data['article_link'], user_data['article_discr'])
        await message.answer("<b>Запись отправленна в каталог!</b>", reply_markup=main_menu_admin_2)
        add_notify_article(f"Новый пост {user_data['article_name']} был добавленн в категорию {user_data['category_name']}")
        await state.finish()
    if message.text == "❎Отмена❎":
        pass

async def add_article_cancel(message: types.Message, state:FSMContext):
    await message.answer("<b>Отменяем...</b>", reply_markup=main_menu_admin_2)
    await state.finish()
#кнопка сохранить данные / останавливает бота
async def save_data(message: types.Message):
    await message.answer("<b>Сохраняю...</b>")
    raise SystemExit

#___________________кнопка удалить запись_________________

async def btn_katalog(message: types.Message):
    await message.answer("<b>🍭Каталог статей, выбери какую удалить🍢</b>", reply_markup=key_k_0_del())

#Открыть содержимое категории
async def btn_kategory(call: types.CallbackQuery):
    data = call.data
    await call.message.edit_text("<b>🍭Каталог статей, выбери какую удалить🍢</b>", reply_markup=key_k_1_del(data))
    await call.answer()

#Удаление категории
async def btn_article(call: types.CallbackQuery):
    key = call.data[call.data.find(":") + 1 : ]
    data = get_articles(key)
    name = data[0][3]
    kategory = data[0][2]
    await call.message.answer(f"<b>Запись '{name}' была удалена из категории {kategory}</b>")
    del_item(key)   

#Кнопка назад
async def btn_back_lvl0(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=key_k_0_del()) 
    await call.answer()

#_______________Кнопка Уведомление_____________

class NotifyState(StatesGroup):
    send_notify = State()

async def btn_notify(message: types.Message):
    await message.answer("<b>О чем уведомить пользователей</b>", reply_markup=key_cancel())
    await NotifyState.send_notify.set()

async def send_notify(message: types.Message, state:FSMContext):
    user_id = get_all_active_user_id()
    counter = 0
    for id in user_id:
        try:
            await dp.bot.send_message(id, text=message.md_text, parse_mode="MarkdownV2")
            counter += 1
        except BotBlocked:
            del_active_user(id)
    await dp.bot.send_message(admin_id, f"<b>Отправленно {counter} сообщений</b>", reply_markup=main_menu_admin_2)
    await state.finish()

async def notify_cancel(message: types.Message, state:FSMContext):
    await message.answer("<b>Отменяем...</b>", reply_markup=main_menu_admin_2)
    await state.finish()

async def get_db(message: types.Message):
    doc = open('cryptolibs.db', 'rb')
    print(datetime.today())
    await message.answer_document(document=doc, caption=f"{datetime.today()}")




#Регистрация хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(set_keyboard, Text(equals="🍒Админка➡️"))
    dp.register_message_handler(del_keyboard, Text(equals="⬅️Назад🍒"))
    dp.register_message_handler(save_data, Text(equals="📨Сохранить данные📨"))
    dp.register_message_handler(get_db, Text(equals="Запросить БД⚙️"))

    dp.register_message_handler(add_article, Text(equals="➕Добавить запись"), state="*")
    dp.register_message_handler(add_article_cancel, Text(equals=("❎Отмена", "❎Отмена❎")), state="*")
    dp.register_callback_query_handler(add_article_get_category, state=AddState.waiting_category)
    dp.register_message_handler(add_article_get_name, state= AddState.waiting_name)
    dp.register_message_handler(add_article_get_discr, state=AddState.waiting_discription)
    dp.register_message_handler(add_article_get_avtor, state=AddState.waiting_avtor)
    dp.register_message_handler(add_article_get_link, state=AddState.waiting_link)
    dp.register_message_handler(add_article_confirm, state=AddState.article_post)
    dp.register_message_handler(add_article_get_category_code, state=AddState.waiting_category_code)
    dp.register_message_handler(add_article_get_category_name, state=AddState.waiting_category_name)

    dp.register_message_handler(btn_katalog, Text(equals="Удалить запись➖"))
    dp.register_callback_query_handler(btn_kategory, Text(equals=get_del_callback()))
    dp.register_callback_query_handler(btn_article, Text(equals=get_del_callback_articles()))
    dp.register_callback_query_handler(btn_back_lvl0, Text(equals="del_back_to_lvl_0"))

    dp.register_message_handler(btn_notify, Text(equals="🔔Уведомление🔔"), state="*")
    dp.register_message_handler(send_notify, state=NotifyState.send_notify)
    dp.register_message_handler(notify_cancel, Text(equals="❎Отмена"), state="*")




async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(admin_id, "<b>🙃Бать, я проснулся😴/Данные сохранены</b>")
    data = get_notify_article()
    user_id = get_all_active_user_id()
    for id in user_id:
        for item in data:
            try:
                await dp.bot.send_message(id, text=f"<b>{item}</b>")
            except BotBlocked:
                del_active_user(id)
    del_notify_article()

async def on_shutdown_notify(dp: Dispatcher):
    await dp.bot.send_message(admin_id, "<b>🤬Опять споткнулся и упал🤯</b>")