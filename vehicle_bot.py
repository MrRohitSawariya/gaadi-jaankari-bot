import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8410893007:AAEaTw2xpkpjbTKLp5hx7V8R5r6tbkXZ6cs"

API_BASE = "https://org.proportalxc.workers.dev/?rc="

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Gaadi Jaankari Bot\n\n"
        "🚘 Vehicle number bhejo (example: BR05T4014)\n\n"
        "📩 Support: @nanhipari3008"
    )

async def vehicle_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vehicle_no = update.message.text.strip().upper()

    try:
        r = requests.get(API_BASE + vehicle_no, headers=HEADERS, timeout=15)
        data = r.json().get("data", {})

        owner = data.get("ownership_profile_analytics", {})
        reg = data.get("registration_identity_matrix", {})

        msg = (
            "🚘 Vehicle Information\n\n"
            "👤 Owner Information\n"
            f"• Name : {owner.get('legal_asset_holder', 'N/A')}\n"
            f"• Address : {owner.get('physical_location_address', 'N/A')}\n\n"
            "📄 Registration Details\n"
            f"• Vehicle No : {vehicle_no}\n"
            f"• RTO : {reg.get('issuing_authority', 'N/A')}\n"
            f"• Reg Date : {reg.get('inception_registration_date', 'N/A')}\n"
        )

        await update.message.reply_text(msg)

    except Exception:
        await update.message.reply_text("⚠️ API fetch error")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, vehicle_lookup))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
