import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.handlers import start, handle_photo
from flask import Flask
import threading

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
