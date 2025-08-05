import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_message(text):
    payload = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(URL, data=payload)
    return response.json()

def main():
    while True:
        send_message("✅ Bot is running on Railway!")
        time.sleep(3600)  # ارسال پیام هر 1 ساعت

if __name__ == "__main__":
    main()
