from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton("/Режим_работы")
b2 = KeyboardButton("/Расположение")
b3 = KeyboardButton("/Меню")
b4 = KeyboardButton("GIMME you number", request_contact=True)
b5 = KeyboardButton("GIMME your location", request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
# kb_client.add(b3).add(b2).insert(b1)
kb_client.row(b3, b2, b1).add(b4).add(b5)
