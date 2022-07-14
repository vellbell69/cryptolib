from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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
            KeyboardButton(text="Добавить категорию➕")
        ],
        [
            KeyboardButton(text="➖Удалить запись"),
            KeyboardButton(text="Удалить категорию➖")
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


def key_cancel():
    key_confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="❎Отмена")
        ]
    ], resize_keyboard=True)
    return key_confirm

choose_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="С картинкой"), KeyboardButton(text="Без картинки")],
        [KeyboardButton(text="❎Отмена")]
    ], resize_keyboard=True
)