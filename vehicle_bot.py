import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8410893007:AAEaTw2xpkpjbTKLp5hx7V8R5r6tbkXZ6cs"
API_BASE = "https://org.proportalxc.workers.dev/?rc="

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚗 *Gaadi Jaankari Bot*\n\n"
        "Vehicle number bhejo\n"
        "Example: `BR05T4014`",
        parse_mode="Markdown"
    )

# Vehicle lookup
async def vehicle_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vehicle_no = update.message.text.strip().upper()

    if len(vehicle_no) < 6:
        await update.message.reply_text("❌ Invalid vehicle number")
        return

    try:
        r = requests.get(API_BASE + vehicle_no, headers=HEADERS, timeout=15)
        data = r.json()

        text = (
            "🚘 *Vehicle Information*\n\n"
            f"🔢 Number: `{vehicle_no}`\n"
            f"📄 Status: {data.get('status', 'N/A')}\n"
            f"🏢 RTO: {data.get('rto', 'N/A')}\n"
            f"📅 Reg Date: {data.get('registration_date', 'N/A')}\n"
            f"⛽ Fuel: {data.get('fuel_type', 'N/A')}"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("⚠️ Error fetching data")

# MAIN
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, vehicle_lookup))

    print("🤖 Bot running...")
    app.run_polling()
