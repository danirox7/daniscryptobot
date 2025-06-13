import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_price():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        data = response.json()
        return f"💰 BTC/USDT: ${float(data['price']):,.2f}"
    except Exception as e:
        return f"❌ خطأ في جلب السعر: {e}"

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📊 Price Now", callback_data='price')],
        [InlineKeyboardButton("🚨 Set Alert", callback_data='alert')],
        [InlineKeyboardButton("📈 Signals", callback_data='signals')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 أهلاً بك في Dani's Crypto Bot", reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "price":
        price = get_price()
        await query.edit_message_text(text=price)
    elif query.data == "alert":
        await query.edit_message_text(text="🚨 ميزة التنبيهات قيد التطوير.")
    elif query.data == "signals":
        await query.edit_message_text(text="📈 لا توجد إشارات حالياً.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Bot is running...")
    app.run_polling(stop_signals=None)
