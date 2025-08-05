import os
import requests
import time
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

# گرفتن توکن و چت‌آیدی از متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# فاصله زمانی (دقیقه)
INTERVAL_MINUTES = 5

bot = Bot(token=TELEGRAM_TOKEN)

def get_px_price():
    try:
        url = "https://api.mexc.com/api/v3/ticker/price?symbol=PXUSDT"
        response = requests.get(url)
        data = response.json()
        price = data.get("price")
        return price
    except Exception as e:
        print("Error getting price:", e)
        return None

def send_price_message():
    price = get_px_price()
    if price:
        message = f"📈 قیمت لحظه‌ای PX/USDT در MEXC: {price} USDT"
    else:
        message = "⚠️ خطا در دریافت قیمت PX/USDT"
    bot.send_message(chat_id=CHAT_ID, text=message)

# پاسخ به دستور /price
def price_command(update: Update, context: CallbackContext):
    price = get_px_price()
    if price:
        message = f"📊 قیمت لحظه‌ای PX/USDT: {price} USDT"
    else:
        message = "❌ متأسفانه نتوانستم قیمت را دریافت کنم."
    update.message.reply_text(message)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # تعریف دستور /price
    dispatcher.add_handler(CommandHandler("price", price_command))

    # شروع دریافت دستورهای کاربر
    updater.start_polling()

    print(f"🤖 ربات فعال شد. ارسال خودکار هر {INTERVAL_MINUTES} دقیقه.")

    # ارسال خودکار قیمت هر INTERVAL_MINUTES دقیقه
    while True:
        send_price_message()
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    main()
