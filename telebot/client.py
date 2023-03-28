from aiogram import exceptions
from aiogram.types import ReplyKeyboardRemove
from create_bot import bot
from keyboard.client_kb import kb_client
from database.sqlite_db import read_from_db


# @dp.message_handler(commands=["start", "help"])
async def command_start(message):
    try:
        await bot.send_message(message.from_user.id,
                               f"Greetings, {message.from_user.first_name}",
                               reply_markup=kb_client)
        await message.delete()
    except exceptions.Unauthorized:
        await message.reply("Kindly start conversation with bot first:\n \
                            https://t.me/antesser_bot")


# @dp.message_handler(commands=["Режим_работы"])
async def open_command(message):
    await bot.send_message(message.from_user.id, "Режим работы")


# @dp.message_handler(commands=["Расположение"])
async def place_command(message):
    await bot.send_message(message.from_user.id, "Расположение",
                           reply_markup=ReplyKeyboardRemove())


async def menu_command(message):
    await read_from_db(message)


def handler_registration_client(dp):
    dp.register_message_handler(command_start, commands=["start", "help"])
    dp.register_message_handler(open_command, commands=["Режим_работы"])
    dp.register_message_handler(place_command, commands=["Расположение"])
    dp.register_message_handler(menu_command, commands=["Меню"])
