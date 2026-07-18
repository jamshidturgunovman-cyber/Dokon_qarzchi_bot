import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F

# Sozlamalar
GOOGLE_SHEET_URL = "Google_sheet_url"
API_TOKEN = 'Bot_Token'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Qarz qo'shish komandasi: /add ID Ism Summa Sana
@dp.message(Command("add"))
async def add_debt(message: types.Message):
    # message.text ni ajratamiz (masalan: /add 101 Ali 50000 2026-07-20)
    args = message.text.split(maxsplit=4)
    if len(args) < 5:
        await message.reply("Noto'g'ri format! \nNamuna: /add 101 Ali 50000 2026-07-20")
        return

    _, id, name, sum, date = args
    
    # Google Sheets ga yuborish
    params = {'action': 'add', 'id': id, 'name': name, 'sum': sum, 'date': date}
    try:
        response = requests.get(GOOGLE_SHEET_URL, params=params)
        if response.text == "Success":
            await message.reply(f"✅ {name} (ID: {id}) uchun {sum} so'm miqdorida qarz yozildi.")
        else:
            await message.reply("❌ Xatolik yuz berdi.")
    except Exception as e:
        await message.reply(f"❌ Xatolik: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
