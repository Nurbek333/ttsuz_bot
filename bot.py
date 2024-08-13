import logging
import sys
import asyncio
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton,FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from data import config
from menucommands.set_bot_commands import set_default_commands
from baza.sqlite import Database
from filters.admin import IsBotAdminFilter
from filters.check_sub_channel import IsCheckSubChannels
from states.reklama import Adverts
from keyboard_buttons import admin_keyboard
from gtts import gTTS  # Yangi qo'shildi
import os  # Yangi qo'shildi

ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start_command(message: Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name, telegram_id=telegram_id)  # Foydalanuvchi bazaga qo'shildi
        await message.answer(text="""Men [Bot nomi] botiman, sizga quyidagi funksiyalarni taqdim etaman:

2. **/about** - Bot haqidagi to'liq ma'lumot va yaratuvchilar haqida.
   
3. **/help** - Botning qanday ishlashini tushuntiruvchi yordam xabari.

**Qanday foydalanish kerak:**
- Ovozli xabarlarni yuborish uchun `/convert` komandasini matn bilan birga yuboring.

Agar qo'shimcha savollar yoki yordam kerak bo'lsa, iltimos, [email:\nnurbekuktamov333@gmail.com/telegram username:\n@me_nurbek] orqali biz bilan bog'laning!

Botni ishlatganingiz uchun rahmat! 🎉
""")
    except Exception as e:
        # logging.exception("Foydalanuvchini qo'shishda xatolik yuz berdi", e)
        await message.answer(text="""Men [Bot nomi] botiman, sizga quyidagi funksiyalarni taqdim etaman:

2. **/about** - Bot haqidagi to'liq ma'lumot va yaratuvchilar haqida.
   
3. **/help** - Botning qanday ishlashini tushuntiruvchi yordam xabari.

**Qanday foydalanish kerak:**
- Ovozli xabarlarni yuborish uchun `/convert` komandasini matn bilan birga yuboring.

Agar qo'shimcha savollar yoki yordam kerak bo'lsa, iltimos, [email:\nnurbekuktamov333@gmail.com/telegram username:\n@me_nurbek] orqali biz bilan bog'laning!

Botni ishlatganingiz uchun rahmat! 🎉
""")

@dp.message(IsCheckSubChannels())
async def kanalga_obuna(message: Message):
    text = ""
    inline_channel = InlineKeyboardBuilder()
    for index, channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal", url=ChatInviteLink.invite_link))
    inline_channel.adjust(1, repeat=True)
    button = inline_channel.as_markup()
    await message.answer(f"{text} kanallarga a'zo bo'ling", reply_markup=button)

@dp.message(Command("help"))
async def help_commands(message: Message):
    await message.answer("""👋 Salom! Men [Bot nomi] botiman. Sizga quyidagi funksiyalarni taqdim etaman:

1. **/start** - Botni ishga tushiradi va siz bilan salomlashadi.
2. **/help** - Botning qanday ishlashini tushuntiruvchi yordam.
3. **/about** - Bot yaratuvchilari va bot haqidagi tuliq malumotlar.

📌 **Qanday foydalanish kerak:**
- Matn yuboring va men uni ovozli xabarga aylantiraman.

Agar qo'shimcha yordam kerak bo'lsa, iltimos, [email/telegram username] orqali biz bilan bog'laning!

🔧 **Yordam uchun:** 
- Muammo yoki savollar bo'lsa, yordam uchun [email/telegram username] bilan bog'laning.

Rahmat, [Bot nomi]!
""")

@dp.message(Command("about"))
async def about_commands(message: Message):
    await message.answer("""📢 **/about** - Bot Haqida Ma'lumot

👋 **Salom! Men [Bot nomi] botiman.**

**Bot Yaratuvchilari:**
- **Yaratuvchi:** Nurbek Uktamov
- **Tajriba:** Backend dasturchi, Django bo'yicha mutaxassis
- **Maqsad:** Ushbu bot sizga matnni ovozga aylantirish va boshqa funktsiyalarni taqdim etish uchun yaratilgan.

**Bot Haqida:**
- **Maqsad:** [Bot nomi] bot sizning matnlaringizni ovozli xabarlarga aylantiradi. Har qanday matnni yuboring va men uni sizga ovozli xabar sifatida qaytaraman.
- **Texnologiyalar:** Bot Python dasturlash tili yordamida yaratildi va `aiogram` kutubxonasi, `gTTS` (Google Text-to-Speech) kabi texnologiyalarni ishlatadi.
- **Qanday Ishlaydi:** Siz matn yuborganingizda, bot uni ovozga aylantiradi va ovozli xabar sifatida yuboradi.

**Agar Qo'shimcha Ma'lumot yoki Yordam Kerak Bo'lsa:**
- **Kontakt:** [nurbekuktamov@gmail.com]
- **Websayt:** [nurbek333.pythonanywhere.com]

Rahmat va botni ishlatganingiz uchun rahmat! 🎉
""")

@dp.message(Command("admin"), IsBotAdminFilter(ADMINS))
async def is_admin(message: Message):
    await message.answer(text="Admin menu", reply_markup=admin_keyboard.admin_button)

@dp.message(F.text == "Foydalanuvchilar soni", IsBotAdminFilter(ADMINS))
async def users_count(message: Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text == "Reklama yuborish", IsBotAdminFilter(ADMINS))
async def advert_dp(message: Message, state: FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin!")

@dp.message(Adverts.adverts)
async def send_advert(message: Message, state: FSMContext):
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0], from_chat_id=from_chat_id, message_id=message_id)
            count += 1
        except Exception as e:
            logging.exception(f"Foydalanuvchiga reklama yuborishda xatolik: {user[0]}", e)
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count} ta foydalanuvchiga yuborildi")
    await state.clear()


# @dp.message(F.text)
# async def convert_text_to_speech(message: Message):
#     text = message.text
#     tts = gTTS(text=text, lang='en') 
#     tts.save('output.mp3')
    
#     with open('output.mp3', 'rb') as audio:
#         await message.reply_voice(voice=audio)

#     os.remove('output.mp3')
    
import io
@dp.message(F.text)
async def convert_text_to_speech(message: types.Message):
    text = message.text
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    file_path = 'output.mp3'
    tts.save(file_path)

    with open(file_path, 'rb') as audio:
            await message.reply_voice(voice=FSInputFile(file_path,filename="tts.mp3"))



@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin), text="Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin), text="Bot ishdan to'xtadi!")
        except Exception as err:
            logging.exception(err)

def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    from middlewares.throttling import ThrottlingMiddleware
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))

async def main() -> None:
    global bot, db
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    db = Database(path_to_db="main.db")
    await set_default_commands(bot)
    setup_middlewares(dispatcher=dp, bot=bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
