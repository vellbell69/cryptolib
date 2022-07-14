from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from db.db_api import article, article_data, category
def category_kb():
    row = []
    category_key = InlineKeyboardMarkup(row_width=2)
    category_info = category("get")
    for item in category_info:
        row.append(InlineKeyboardButton(text=item[1], callback_data=item[0]))

    category_key.add(*row)
    return category_key

def article_kb(key):
    key = key[key.find(":") + 1 : ]
    category_key = InlineKeyboardMarkup()
    category_info = article(key, "get")
    for item in category_info:
            category_key.add(InlineKeyboardButton(text=item[2], callback_data=item[0]))
    category_key.add(InlineKeyboardButton(text="Назад", callback_data="back_to_lvl_0"))
    return category_key

def article_kb_info(key):
    key = key[key.find(":") + 1 : ]
    category_key = InlineKeyboardMarkup()
    category_info = article_data(key)
    category_key.add(InlineKeyboardButton(text="Перейти", url=f"{category_info[0][5]}"))
    category_key.add(InlineKeyboardButton(text="Назад", callback_data=f"back_to_lvl_1:{category_info[0][1]}"))
    return category_key



def del_category_kb():
    row = []
    category_key = InlineKeyboardMarkup(row_width=2)
    category_info = category("del")
    for item in category_info:
        row.append(InlineKeyboardButton(text=item[1], callback_data=item[0]))

    category_key.add(*row)
    return category_key

def add_category_kb():
    row = []
    category_key = InlineKeyboardMarkup(row_width=2)
    category_info = category("add")
    for item in category_info:
        row.append(InlineKeyboardButton(text=item[1], callback_data=item[0]))

    category_key.add(*row)
    return category_key

def confirm_key():
    key_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="✅Постим✅"),
           KeyboardButton(text="❎Отмена")
        ]
    ], resize_keyboard=True)
    return key_confirm

def category_kb_del():
    row = []
    category_key = InlineKeyboardMarkup(row_width=2)
    category_info = category("article_del")
    for item in category_info:
        row.append(InlineKeyboardButton(text=item[1], callback_data=item[0]))

    category_key.add(*row)
    return category_key

def article_kb_del(key):
    key = key[key.find(":") + 1 : ]
    category_key = InlineKeyboardMarkup()
    category_info = article(key, "del")
    for item in category_info:
            category_key.add(InlineKeyboardButton(text=item[3], callback_data=item[0]))
    category_key.add(InlineKeyboardButton(text="Назад", callback_data="back_to_lvl_0_del"))
    return category_key