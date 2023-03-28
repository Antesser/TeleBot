from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b_upload = KeyboardButton("/upload")
b_delete = KeyboardButton("/delete")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(b_upload, b_delete)
