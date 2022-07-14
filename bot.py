import logging
from aiogram import executor
from loader import dp

logging.basicConfig(level=logging.INFO)

from handlers import admin, client, other
from handlers.admin import on_startup_notify, on_shutdown_notify

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup_notify, on_shutdown=on_shutdown_notify)