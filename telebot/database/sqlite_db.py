import sqlite3

from create_bot import bot


def create_db():
    global database, cursor
    database = sqlite3.connect("bot.db")
    cursor = database.cursor()
    if database:
        print("DB is connected")
    database.execute("""CREATE TABLE IF NOT EXISTS bot_db(img TEXT,
                     name TEXT PRIMARY KEY, description TEXT, price TEXT)""")
    database.commit()


async def add_data_to_db(state):
    async with state.proxy() as data:
        cursor.execute("""INSERT INTO bot_db VALUES(?, ?, ?, ?)""",
                       tuple(data.values()))
        database.commit()


async def read_from_db(message):
    for all_data in cursor.execute("SELECT * FROM bot_db").fetchall():
        await bot.send_photo(message.from_user.id, all_data[0],
                             f"{all_data[1]}\nDescription: {all_data[2]}"
                             f"\nPrice: {all_data[3]}")


async def read_all():
    return cursor.execute("SELECT * FROM bot_db").fetchall()


async def delete_data(data):
    cursor.execute("DELETE FROM bot_db WHERE name == ?", (data,))
    database.commit()
