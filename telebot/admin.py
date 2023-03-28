from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import bot
from database.sqlite_db import add_data_to_db, read_all, delete_data
from keyboard.admin_kb import kb_admin

ID = None


class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def admin_access(message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id,
                           "What're ur biddings, master?",
                           reply_markup=kb_admin)
    await message.delete()


def check_if_admin(message):
    return message.from_user.id == ID


async def upload_photo_request(message):
    if check_if_admin(message):
        await FSMadmin.photo.set()
        await message.reply("Upload a photo")


async def upload_photo(message, state):
    if check_if_admin(message):
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
            await FSMadmin.next()
            await message.reply("Add a name now")


async def upload_name(message, state):
    if check_if_admin(message):
        async with state.proxy() as data:
            data["name"] = message.text
            await FSMadmin.next()
            await message.reply("Add a description now")


async def upload_description(message, state):
    if check_if_admin(message):
        async with state.proxy() as data:
            data["description"] = message.text
            await FSMadmin.next()
            await message.reply("Add a price now")


async def upload_price(message, state):
    if check_if_admin(message):
        async with state.proxy() as data:
            data["price"] = float(message.text)
            await message.reply("We're all set")

        await add_data_to_db(state)
        await state.finish()


async def abort_handler(message, state):
    if check_if_admin(message):
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply("Operation has been aborted")


async def delete_callback(callback_query):
    await delete_data(callback_query.data.replace("del ", ""))
    await callback_query.answer(
        text=f"{callback_query.data.replace('del ', '')} has been deleted",
        show_alert=True)


async def delete_item(message):
    if check_if_admin(message):
        read = await read_all()
        for i in read:
            await bot.send_photo(message.from_user.id, i[0],
                                 f"{i[1]}\nDescription: {i[2]}\nPrice: {i[-1]}"
                                 )
            await bot.send_message(message.from_user.id, text="^^^",
                                   reply_markup=InlineKeyboardMarkup()
                                   .add(InlineKeyboardButton(
                                       f"Delete {i[1]}",
                                       callback_data=f"del {i[1]}")))


def handler_registration_admin(dp):
    dp.register_message_handler(upload_photo_request, commands=[
                                "upload"])
    dp.register_message_handler(upload_photo, content_types=[
                                "photo"], state=FSMadmin.photo)
    dp.register_message_handler(upload_name, state=FSMadmin.name)
    dp.register_message_handler(upload_description, state=FSMadmin.description)
    dp.register_message_handler(upload_price, state=FSMadmin.price)
    dp.register_message_handler(abort_handler, state="*", commands="abort")
    dp.register_message_handler(abort_handler,
                                Text(equals="abort",
                                     ignore_case=True), state="*")
    dp.register_message_handler(admin_access, commands=["admin"],
                                is_chat_admin=True)
    dp.register_callback_query_handler(delete_callback,
                                       lambda x: x.data and
                                       x.data.startswith("del "))
    dp.register_message_handler(delete_item, commands="delete")
