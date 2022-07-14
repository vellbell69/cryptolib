from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from handlers.client import btn_cancel
from keyboards.katalog import add_category_kb, article_kb_del, category_kb_del, confirm_key, del_category_kb
from loader import dp

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import aiogram.utils.markdown as fmt
from aiogram.utils.exceptions import BotBlocked

from config.config import admin_id

from keyboards.keyboard import key_cancel, main_menu_admin_1, main_menu_admin_2
from db.db_api import article_add, article_del, category, category_add, category_del, del_active_user, get_all_active_user_id

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

async def cancel(message: types.Message, state:FSMContext):
    await message.answer("<b>Отменяем...</b>", reply_markup=main_menu_admin_2)
    await state.finish()

async def get_db(message: types.Message):
    doc = open('db\cryptolibs.db', 'rb')
    print(datetime.today())
    await message.answer_document(document=doc, caption=f"{datetime.today()}")
    

#___________________________________Робота с каталогом___________________________________________
class AddCategoryState(StatesGroup):
    get_name = State()

async def add_category_start(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Введи название новой категории:", reply_markup=key_cancel())
        await AddCategoryState.get_name.set()

async def add_category(message: types.Message, state:FSMContext):
    name = message.text
    category_add(name)
    await message.answer(f"Категория {name} была создана", reply_markup=main_menu_admin_2)
    await state.finish()

async def del_category_start(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Выбери какую категорию удалить", reply_markup=del_category_kb())

async def del_category(call: types.CallbackQuery):
    category_del(call.data[call.data.find(":") + 1 : ])
    await call.message.answer("Категория удалена")

#Добавление поста
class AddArticleState(StatesGroup):
    waiting_category = State()
    waiting_name = State()
    waiting_discription = State()
    waiting_avtor = State()
    waiting_link = State()
    article_post = State()


async def add_article_start(message: types.Message):
    if message.from_user.id == admin_id:
        await message.answer("Ты в меню добавления записей", reply_markup=key_cancel())
        await message.answer("Выбери в какую категорию добавим", reply_markup=add_category_kb())
        await AddArticleState.waiting_category.set()

async def add_article_get_category(call: types.CallbackQuery, state:FSMContext):
    category_code = call.data[call.data.find(":") + 1 : ]
    await state.update_data(category_code=category_code)
    await call.message.answer(f"<b>Ты выбрал категорию {category_code}\n\nТеперь введи название для записи:</b>")
    await call.answer()
    await AddArticleState.waiting_name.set()

async def add_article_get_name(message: types.Message, state:FSMContext):
    await state.update_data(article_name=message.text)
    await message.answer(f"<b>Ты ввёл название '{message.text}'\n\nТеперь введи описание для записи:</b>")
    await AddArticleState.waiting_discription.set()

async def add_article_get_discr(message: types.Message, state:FSMContext):
    await state.update_data(article_discr=message.text)
    await message.answer(f"<b>Ты ввёл описание '{message.text}'\n\nТеперь введи автора материла:</b>")
    await AddArticleState.waiting_avtor.set()

async def add_article_get_avtor(message: types.Message, state:FSMContext):
    await state.update_data(article_avtor=message.text)
    await message.answer(f"<b>Ты ввёл автора '{message.text}'\n\nТеперь введи ссылку:</b>")
    await AddArticleState.waiting_link.set()

async def add_article_get_link(message: types.Message, state:FSMContext):
    await state.update_data(article_link=message.text)
    await message.answer(f"<b>Ты ввёл ссылку '{message.text}'\n\nПредпросмотр:</b>")
    user_data = await state.get_data()
    await message.answer(f"<b>{fmt.hide_link(user_data['article_link'])}{user_data['article_name']}\n\n👨‍🚀Автор: {user_data['article_avtor']}\n\n📜{user_data['article_discr']}</b>", reply_markup=confirm_key())
    await AddArticleState.article_post.set()

async def add_article_confirm(message: types.Message, state:FSMContext):
    if message.text == "✅Постим✅":
        user_data = await state.get_data()
        article_add(user_data['category_code'], user_data['article_name'], user_data['article_avtor'], user_data['article_discr'], user_data['article_link'])
        await message.answer("<b>Запись отправленна в каталог!</b>", reply_markup=main_menu_admin_2)
        await state.finish()

#Удаление записи
async def btn_catalog_del(message: types.Message):
    await message.answer("Выбери какую запись удалить", reply_markup=category_kb_del())

async def btn_category_del(call: types.CallbackQuery):
    category_id = call.data
    await call.message.edit_reply_markup(reply_markup=article_kb_del(category_id))
    await call.answer()

async def btn_article_del(call: types.CallbackQuery):
    article_id = call.data[call.data.find(":") + 1 : ]
    article_del(article_id)
    await call.message.answer("Запись была удалена!")

async def btn_back_lvl_0(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=category_kb_del())

#Регистрация хендлеров
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(set_keyboard, Text(equals="🍒Админка➡️"))
    dp.register_message_handler(del_keyboard, Text(equals="⬅️Назад🍒"))
    dp.register_message_handler(get_db, Text(equals="Запросить БД⚙️"))

    dp.register_message_handler(btn_notify, Text(equals="🔔Уведомление🔔"), state="*")
    dp.register_message_handler(send_notify, state=NotifyState.send_notify)
    dp.register_message_handler(cancel, Text(equals="❎Отмена"), state="*")

    dp.register_message_handler(add_category_start, Text(equals="Добавить категорию➕"))
    dp.register_message_handler(add_category, state=AddCategoryState.get_name)

    dp.register_message_handler(del_category_start, Text(equals="Удалить категорию➖"))
    dp.register_callback_query_handler(del_category, Text(equals=category("call_del")))

    dp.register_message_handler(add_article_start, Text(equals="➕Добавить запись"), state="*")
    dp.register_callback_query_handler(add_article_get_category, state=AddArticleState.waiting_category)
    dp.register_message_handler(add_article_get_name, state= AddArticleState.waiting_name)
    dp.register_message_handler(add_article_get_discr, state=AddArticleState.waiting_discription)
    dp.register_message_handler(add_article_get_avtor, state=AddArticleState.waiting_avtor)
    dp.register_message_handler(add_article_get_link, state=AddArticleState.waiting_link)
    dp.register_message_handler(add_article_confirm, state=AddArticleState.article_post)

    dp.register_message_handler(btn_catalog_del, Text(equals="➖Удалить запись"))
    dp.register_callback_query_handler(btn_category_del, Text(startswith="article_del:"))
    dp.register_callback_query_handler(btn_article_del, Text(startswith="article_del_call:"))
    dp.register_callback_query_handler(btn_back_lvl_0, Text(equals="back_to_lvl_0_del"))

async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(admin_id, "<b>🙃Бать, я проснулся😴/Данные сохранены</b>")

async def on_shutdown_notify(dp: Dispatcher):
    await dp.bot.send_message(admin_id, "<b>🤬Опять споткнулся и упал🤯</b>")