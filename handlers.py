from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils import remove_bg_and_merge

# Mashhur insonlar va manzaralar uchun tugmalar
categories = {
    "manzara": ["🇦🇪 Dubay", "🇫🇷 Parij", "🇷🇺 Moskva", "🇰🇷 Seul"],
    "futbolchi": ["Cristiano Ronaldo", "Eldor Shomurodov"],
    "aktyor": ["Shahrukh Khan", "Angelina Jolie", "Lee Min Ho"],
    "tiktoker": ["Khaby Lame", "MrBeast", "Sardor Gangster"]
}

selected_category = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌆 Mashhur joyda rasm", callback_data="manzara")],
        [InlineKeyboardButton("⚽ Futbolchi bilan", callback_data="futbolchi")],
        [InlineKeyboardButton("🎬 Aktyor/Aktrisa bilan", callback_data="aktyor")],
        [InlineKeyboardButton("🎤 TikToker bilan", callback_data="tiktoker")],
    ]
    await update.message.reply_text(
        "📸 Qaysi turdagi montajni tanlaysiz?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    selected_category[query.from_user.id] = category
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"{category}:{name}")]
        for name in categories[category]
    ]
    await query.message.reply_text(f"🧑‍🎤 Tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    category_name = selected_category.get(user_id)

    if not category_name:
        await update.message.reply_text("❗ Iltimos, avval mashhurlar yoki joylardan birini tanlang.")
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_path = f"user_photos/{user_id}.png"
    await file.download_to_drive(image_path)

    bg_path = f"static/{'manzara' if category_name == 'manzara' else 'mashhurlar'}/{context.user_data.get('selected')}.jpg"
    output_path = f"user_photos/output_{user_id}.png"
    remove_bg_and_merge(image_path, bg_path, output_path)

    await update.message.reply_photo(photo=open(output_path, "rb"), caption="✅ Tayyor!")
