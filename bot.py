import logging
import sys
import asyncio
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, FSInputFile
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
from gtts import gTTS
import os
from buttons import savol_button
from filters.admin import IsBotAdminFilter
from aiogram import types
import logging
from aiogram.types import CallbackQuery, ContentType,InlineKeyboardButton, CallbackQuery, FSInputFile
from filters.admin import IsBotAdminFilter,AdminStates
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup

ADMINS = config.ADMINS
TOKEN = config.BOT_TOKEN
CHANNELS = config.CHANNELS

dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start_command(message: Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name, telegram_id=telegram_id)  # Add user to the database
        await message.answer(text="""<b>👋 Assalomu alaykum!</b>

<b>Men SifatDev IT Akademiyasi tomonidan yaratilgan botman.</b>

<b>Botning funksiyalari:</b>
1. <b>/about</b> - Bot haqida to'liq ma'lumot va yaratuvchilar haqida.
2. <b>/help</b> - Botning ishlash tartibi va yordam haqida xabar.

<b>Qanday foydalanish kerak:</b>
- Ovozli xabarlarni olish uchun matn yuboring va bot sizga ovozli xabar yuboradi.

<b>Qo'shimcha savollar yoki takliflar uchun:</b>
- <b>⚙️ Savol yoki takliflar tugmasini bosing va admin bilan bog'laning.</b>

<b>Botni ishlatganingiz uchun rahmat! 🎉</b>
""", parse_mode='html', reply_markup=savol_button)
    except Exception as e:
        # logging.exception("Foydalanuvchini qo'shishda xatolik yuz berdi", e)
        await message.answer(text="""<b>👋 Assalomu alaykum!</b>

<b>Men SifatDev IT Akademiyasi tomonidan yaratilgan botman.</b>

<b>Botning funksiyalari:</b>
1. <b>/about</b> - Bot haqida to'liq ma'lumot va yaratuvchilar haqida.
2. <b>/help</b> - Botning ishlash tartibi va yordam haqida xabar.

<b>Qanday foydalanish kerak:</b>
- Ovozli xabarlarni olish uchun matn yuboring va bot sizga ovozli xabar yuboradi.

<b>Qo'shimcha savollar yoki takliflar uchun:</b>
- <b>⚙️ Savol yoki takliflar tugmasini bosing va admin bilan bog'laning.</b>

<b>Botni ishlatganingiz uchun rahmat! 🎉</b>
""", parse_mode='html', reply_markup=savol_button)

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
    await message.answer("""<b>👋 Salom!</b>

<b>Men SifatDev IT Akademiyasi tomonidan yaratilgan botman. Quyidagi funksiyalarni taqdim etaman:</b>

1. <b>/start</b> - Botni ishga tushiradi va siz bilan salomlashadi.
2. <b>/help</b> - Botning qanday ishlashini tushuntiruvchi yordam xabari.
3. <b>/about</b> - Bot haqidagi to'liq ma'lumot va yaratuvchilar haqida.

<b>Qanday foydalanish kerak:</b>
- Ovozli xabarlarni olish uchun matn yuboring va bot sizga ovozli xabar yuboradi.

<b>Qo'shimcha savollar yoki takliflar uchun:</b>
- <b>⚙️ Savol yoki takliflar tugmasini bosing va admin bilan bog'laning.</b>

<b>Agar qo'shimcha yordam kerak bo'lsa, iltimos, biz bilan bog'laning!</b>

<b>Botni ishlatganingiz uchun rahmat! 🎉</b>
""", parse_mode='html')


@dp.message(Command("about"))
async def about_commands(message: Message):
    await message.answer(
        """<b>📢 Bot Haqida Ma'lumot</b>

<b>👋 Salom!</b>

<b>Men SifatDev IT Akademiyasi tomonidan yaratilgan botman. Quyidagi ma'lumotlarni taqdim etaman:</b>

<b>Bot Haqida:</b>
<b>Maqsad:</b> Bot sizning matnlaringizni ovozli xabarlarga aylantiradi. Har qanday matnni yuborganingizda, bot uni ovozga aylantiradi va sizga ovozli xabar sifatida yuboradi.\n
<b>Texnologiyalar:</b> Bot Python dasturlash tili yordamida yaratildi va <b>aiogram</b> kutubxonasi, <b>gTTS</b> (Google Text-to-Speech) kabi texnologiyalarni ishlatadi.\n
<b>Qanday Ishlaydi:</b> Siz matn yuborganingizda, bot uni ovozga aylantiradi va ovozli xabar sifatida qaytaradi.

<b>Qo'shimcha Ma'lumot yoki Yordam Kerak Bo'lsa:</b>
<b>⚙️ Savollar yoki takliflar uchun ⚙️ Savol yoki takliflar tugmasini bosing va admin bilan bog'laning.</b>

<b>Botni ishlatganingiz uchun rahmat! 🎉</b>""",
        parse_mode="html"
    )


@dp.message(Command("admin"), IsBotAdminFilter(ADMINS))
async def is_admin(message: Message):
    await message.answer(text="Admin menu", reply_markup=admin_keyboard.admin_button)

@dp.message(F.text == "Foydalanuvchilar soni", IsBotAdminFilter(ADMINS))
async def users_count(message: Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text, parse_mode=ParseMode.HTML)

@dp.message(F.text == "Reklama yuborish", IsBotAdminFilter(ADMINS))
async def advert_dp(message: Message, state: FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin!", parse_mode=ParseMode.HTML)

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
    
    await message.answer(f"Reklama {count} ta foydalanuvchiga yuborildi", parse_mode=ParseMode.HTML)
    await state.clear()

# Define the states for admin functionality
class AdminStates(StatesGroup):
    waiting_for_admin_message = State()
    waiting_for_reply_message = State()


class AdminStates(StatesGroup):
    waiting_for_admin_message = State()
    waiting_for_reply_message = State()


# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define admin states
class AdminStates(StatesGroup):
    waiting_for_admin_message = State()
    waiting_for_reply_message = State()

# Function to create inline keyboard for reply
def create_inline_keyboard(user_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Javob berish",
        callback_data=f"reply:{user_id}"
    )


    return keyboard_builder.as_markup()


@dp.message(lambda message: message.text == '✉️ Savollar va takliflar')
async def handle_savol_takliflar(message: Message, state: FSMContext):
    # Foydalanuvchiga admin uchun xabar yuborish uchun taklif qiluvchi matn
    await message.answer(
        "<b>📩 Sizning fikr va savollaringiz biz uchun muhim!</b>\n\n"
        "Iltimos, admin uchun xabar yuboring. Sizning savolingiz yoki taklifingiz "
        "tez orada ko'rib chiqiladi va sizga javob beriladi.\n\n"
        "<i>Matn, rasm, audio yoki boshqa turdagi fayllarni yuborishingiz mumkin.</i>",
        parse_mode='html'
    )
    await state.set_state(AdminStates.waiting_for_admin_message)

# Handle different content types for the message sent to admin
@dp.message(AdminStates.waiting_for_admin_message, F.content_type.in_([
    ContentType.TEXT, ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO,
    ContentType.PHOTO, ContentType.ANIMATION, ContentType.STICKER, 
    ContentType.LOCATION, ContentType.DOCUMENT, ContentType.CONTACT,
    ContentType.VIDEO_NOTE
]))
async def handle_admin_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ""

    # Foydalanuvchini aniqlash (foydalanuvchi nomi yoki ismi/familiyasi)
    user_identifier = f"@{username}" if username else f"{first_name} {last_name}".strip()

    video_note = message.video_note
    inline_keyboard = create_inline_keyboard(user_id)

    for admin_id in ADMINS:
        try:
            if video_note:
                await bot.send_video_note(
                    admin_id,
                    video_note.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.text:
                await bot.send_message(
                    admin_id,
                    f"👤 Foydalanuvchi: {user_identifier}\n✉️ Xabar:\n{message.text}",
                    reply_markup=inline_keyboard
                )
            elif message.audio:
                await bot.send_audio(
                    admin_id,
                    message.audio.file_id,
                    caption=f"👤 Foydalanuvchi: {user_identifier}\n🎧 Audio xabar",
                    reply_markup=inline_keyboard
                )
            elif message.voice:
                await bot.send_voice(
                    admin_id,
                    message.voice.file_id,
                    caption=f"👤 Foydalanuvchi: {user_identifier}\n🎤 Voice xabar",
                    reply_markup=inline_keyboard
                )
            elif message.video:
                await bot.send_video(
                    admin_id,
                    message.video.file_id,
                    caption=f"👤 Foydalanuvchi: {user_identifier}\n🎬 Video xabar",
                    reply_markup=inline_keyboard
                )
            elif message.photo:
                await bot.send_photo(
                    admin_id,
                    message.photo[-1].file_id,
                    caption=f"👤 Foydalanuvchi: {user_identifier}\n🖼️ Rasm xabar",
                    reply_markup=inline_keyboard
                )
            elif message.animation:
                await bot.send_animation(
                    admin_id,
                    message.animation.file_id,
                    caption=f"👤 Foydalanuvchi: {user_identifier}\n🎞️ GIF xabar",
                    reply_markup=inline_keyboard
                )
            elif message.sticker:
                await bot.send_sticker(
                    admin_id,
                    message.sticker.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.location:
                await bot.send_location(
                    admin_id,
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    reply_markup=inline_keyboard
                )
            elif message.document:
                await bot.send_document(
                    admin_id,
                    message.document.file_id,
                    caption=f"👤 Foydalanuvchi: {user_identifier}\n📄 Hujjat xabar",
                    reply_markup=inline_keyboard
                )
            elif message.contact:
                await bot.send_contact(
                    admin_id,
                    phone_number=message.contact.phone_number,
                    first_name=message.contact.first_name,
                    last_name=message.contact.last_name or "",
                    reply_markup=inline_keyboard
                )
        except Exception as e:
            logging.error(f"⚠️ Error sending message to admin {admin_id}: {e}")

    await state.clear()
    await bot.send_message(user_id, "✅ Admin sizga javob berishi mumkin.")

# Callback query handler for the reply button
@dp.callback_query(lambda c: c.data.startswith('reply:'))
async def process_reply_callback(callback_query: CallbackQuery, state: FSMContext):
    user_id = int(callback_query.data.split(":")[1])
    await callback_query.message.answer("📝 Javobingizni yozing. Sizning javobingiz foydalanuvchiga yuboriladi.")
    await state.update_data(reply_user_id=user_id)
    await state.set_state(AdminStates.waiting_for_reply_message)
    await callback_query.answer()

# Handle admin reply and send it back to the user
@dp.message(AdminStates.waiting_for_reply_message)
async def handle_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    original_user_id = data.get('reply_user_id')

    if original_user_id:
        try:
            if message.text:
                await bot.send_message(original_user_id, f"📩 Admin javobi:\n{message.text}")
            elif message.voice:
                await bot.send_voice(original_user_id, message.voice.file_id)
            elif message.video_note:
                await bot.send_video_note(original_user_id, message.video_note.file_id)
            elif message.audio:
                await bot.send_audio(original_user_id, message.audio.file_id)
            elif message.sticker:
                await bot.send_sticker(original_user_id, message.sticker.file_id)
            elif message.video:
                await bot.send_video(original_user_id, message.video.file_id)

            await bot.send_message(ADMINS[0], "✅ Foydalanuvchiga habaringiz yuborildi!")
            await state.clear()  # Clear state after sending the reply
        except Exception as e:
            logger.error(f"⚠️ Error sending reply to user {original_user_id}: {e}")
            await message.reply("❌ Xatolik: Javob yuborishda xato yuz berdi.")
    else:
        await message.reply("⚠️ Xatolik: Javob yuborish uchun foydalanuvchi ID topilmadi.")


@dp.message(F.text)
async def convert_text_to_speech(message: types.Message):
    text = message.text
    tts = gTTS(text=text, lang='en')
    file_path = 'output.mp3'
    tts.save(file_path)

    with open(file_path, 'rb') as audio:
        await message.reply_voice(
            voice=FSInputFile(file_path, filename="tts.mp3"),
            caption="<b>🎵 Ovozli xabar:</b>\nMatn quyidagi ovozli xabarga aylantirildi.",
        parse_mode='html')

    os.remove(file_path)


@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=int(admin),
                text="<b>🔔 Bot muvaffaqiyatli ishga tushdi!</b>\n\n"
                     "Bot endi to'liq faol va foydalanuvchilar bilan muloqotga tayyor. "
                     "Agar biror bir muammo yuzaga kelsa, tezda xabar bering.",
                parse_mode='html'
            )
        except Exception as err:
            logging.exception(f"Admin {admin} uchun xabar yuborishda xatolik yuz berdi: {err}")

# Bot ishdan to'xtaganda barcha adminlarni xabardor qilish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=int(admin),
                text="<b>⛔️ Bot ishdan to'xtadi!</b>\n\n"
                     "Bot faoliyati to'xtatildi. Agar bu rejalashtirilmagan bo'lsa, "
                     "iltimos, darhol tekshiring va botni qayta ishga tushiring.",
                parse_mode='html'
            )
        except Exception as err:
            logging.exception(f"Admin {admin} uchun xabar yuborishda xatolik yuz berdi: {err}")


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    from middlewares.throttling import ThrottlingMiddleware
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))

async def main() -> None:
    global bot, db
    bot = Bot(TOKEN)
    db = Database(path_to_db="main.db")
    await set_default_commands(bot)
    setup_middlewares(dispatcher=dp, bot=bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
