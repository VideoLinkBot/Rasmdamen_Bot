import os
import threading
from flask import Flask
from rembg import remove
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 TOKEN
TOKEN = os.environ.get("BOT_TOKEN")

# 🌐 Flask — Railway tirik tutish uchun
app = Flask(__name__)
@app.route("/")
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# 🧠 START komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Rasm yuboring, men uni Ronaldo bilan montaj qilib qaytaraman 📸")

# 🖼 Foto kelganda
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = "user_photo.png"
    await file.download_to_drive(file_path)

    # 📸 Rasmni fonini o‘chir va Ronaldo bilan birlashtir
    user_img = Image.open(file_path)
    user_no_bg = remove(user_img)
    user_resized = user_no_bg.resize((400, 400))

    celeb_img = Image.open("static/mashhurlar/ronaldo.png").resize((400, 400))

    merged = Image.new("RGBA", (800, 400))
    merged.paste(user_resized, (0, 0), user_resized)
    merged.paste(celeb_img, (400, 0), celeb_img)

    output_path = "output.png"
    merged.save(output_path)

    # ✅ Natijani yubor
    with open(output_path, "rb") as final:
        await update.message.reply_photo(final, caption="Mana siz Ronaldo bilan! 🤝")

# 🚀 Botni ishga tushirish
def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app_bot.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
