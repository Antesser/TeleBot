from admin import handler_registration_admin
from aiogram import executor
from client import handler_registration_client
from create_bot import dp
from database.sqlite_db import create_db


async def on_startup(_):
    print("Bot is online")
    create_db()


handler_registration_client(dp)
handler_registration_admin(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
