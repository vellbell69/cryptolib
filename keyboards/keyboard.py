from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from db.db_api import get_articles, get_categories, get_items
"""
Каталог, Спонсоры, Инфо, 

"""

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗂Каталог"),
            KeyboardButton(text="😎Спонсоры"),
            KeyboardButton(text="💎Инфо/Контакт")
        ],
        [
            KeyboardButton(text="💁Предложить материал")
        ]
], resize_keyboard=True)

main_menu_admin_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🗂Каталог"),
            KeyboardButton(text="😎Спонсоры"),
            KeyboardButton(text="💎Инфо/Контакт")
        ],
        [
            KeyboardButton(text="💁Предложить материал"),
            KeyboardButton(text="🍒Админка➡️")
        ]
], resize_keyboard=True)

main_menu_admin_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕Добавить запись"),
            KeyboardButton(text="📨Сохранить данные📨"),
            KeyboardButton(text="Удалить запись➖")
        ],
        [
            KeyboardButton(text="⬅️Назад🍒"),
            KeyboardButton(text="🔔Уведомление🔔"),
            KeyboardButton(text="Запросить БД⚙️")
        ]
], resize_keyboard=True)

cancel_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌Отменить")]
    ], resize_keyboard=True
)

#Категории в каталоге
def key_k_0():
    keyboard_katalog_0 = InlineKeyboardMarkup()
    row = []
    for item in get_categories():
        if len(row) == 2:
            keyboard_katalog_0.add(*row)
            row = []
        row.append(InlineKeyboardButton(text=item[1], callback_data=item[0]))
    keyboard_katalog_0.add(*row)
    return keyboard_katalog_0

#Статьи в каталоге
def key_k_1(key):
    keyboard_katalog_1 = InlineKeyboardMarkup()
    data = get_items(key)
    for item in data:
        keyboard_katalog_1.add(InlineKeyboardButton(text=item[3], callback_data=item[0]))
    keyboard_katalog_1.add(InlineKeyboardButton(text="⬅️Назад", callback_data="back_to_lvl_0"))
    return keyboard_katalog_1

#Кнопка открыть и назад в статье
def key_k_2(key):
    data = get_articles(key)
    link = data[0][5]
    category_code = data[0][1]
    keyboard_article = InlineKeyboardMarkup()
    keyboard_article.add(InlineKeyboardButton(text="Перейти", url=link))
    keyboard_article.add(InlineKeyboardButton(text="⬅️Назад", callback_data=category_code))
    return keyboard_article

#._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._

def key_k_0_add():
    keyboard_katalog_0 = InlineKeyboardMarkup()
    row = []
    for item in get_categories():
        if len(row) == 2:
            keyboard_katalog_0.add(*row)
            row = []
        row.append(InlineKeyboardButton(text=item[1], callback_data=f"add:{item[0]}"))
    keyboard_katalog_0.add(*row)
    keyboard_katalog_0.add(InlineKeyboardButton(text="Создать категорию", callback_data="create_category"))
    return keyboard_katalog_0

def key_confirm():
    key_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅Постим✅"), KeyboardButton(text="❎Отмена❎")
        ]
    ], resize_keyboard=True)
    return key_confirm

def key_cancel():
    key_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="❎Отмена")
        ]
    ], resize_keyboard=True)
    return key_confirm

#........................................................

#Категории в каталоге
def key_k_0_del():
    keyboard_katalog_0 = InlineKeyboardMarkup()
    row = []
    for item in get_categories():
        if len(row) == 2:
            keyboard_katalog_0.add(*row)
            row = []
        row.append(InlineKeyboardButton(text=item[1], callback_data=f"del:{item[0]}"))
    keyboard_katalog_0.add(*row)
    return keyboard_katalog_0

#Статьи в каталоге
def key_k_1_del(key):
    new_key=key[key.find(":") + 1 : ]
    keyboard_katalog_1 = InlineKeyboardMarkup()
    data = get_items(new_key)
    for item in data:
        keyboard_katalog_1.add(InlineKeyboardButton(text=item[3], callback_data=f"del:{item[0]}"))
    keyboard_katalog_1.add(InlineKeyboardButton(text="⬅️Назад", callback_data="del_back_to_lvl_0"))
    return keyboard_katalog_1
