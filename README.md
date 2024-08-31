# Telegram TTS Bot

Bu Telegram bot foydalanuvchilarning matnli xabarlarini ovozli xabarlarga aylantiradi. Siz ushbu botni Telegram orqali matnni ovozli xabarga aylantirish uchun ishlatishingiz mumkin.

## Asosiy xususiyatlar

- Matnli xabarlarni ovozli xabarlarga aylantirish
- Ovozli xabarlar yuqori sifatli TTS (Text-To-Speech) texnologiyasi yordamida yaratiladi
- Foydalanuvchilarning ovozli xabarlarini saqlash va ulashish imkoniyati

## Talablar

- Python 3.7 yoki undan yuqori versiya
- `aiogram` kutubxonasi
- `gTTS` yoki boshqa TTS kutubxonasi

## O'rnatish

1. GitHub repozitoriyasini klonlang:

    ```bash
    git clone https://github.com/Nurbek333/ttsuz_bot.git
    cd your-repository
    ```

2. Virtual muhit yaratib, uni faollashtiring (ixtiyoriy):

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate     # Windows
    ```

3. Zaruriy kutubxonalarni o'rnating:

    ```bash
    pip install -r requirements.txt
    ```

4. `.env` faylini yaratib, Telegram bot tokenini qo'shing:

    ```
    BOT_TOKEN=your-telegram-bot-token
    ```



- **filters/**:
  - `admin.py`: Adminlar uchun maxsus funksiyalarni filtrlaydigan kodlar joylashgan.
  - `check_sub_channel.py`: Foydalanuvchining kerakli kanalga obuna bo‘lganligini tekshiruvchi kodlar.

- **keyboard_buttons/**:
  - `admin_keyboard.py`: Bot interfeysida adminlar uchun klaviatura tugmalari sozlanadi.

- **menucommands/**:
  - `set_bot_commands.py`: Telegram bot menyusidagi buyruqlarni o'rnatish uchun skript.
 

## Ishga tushirish

Botni ishga tushurish uchun:

```bash
python bot.py

