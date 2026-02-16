import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

API_BASE = "https://org.proportalxc.workers.dev/?rc="

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Gaadi Jaankari Bot\n\n"
        "🚘 Yaha kisi bhi vehicle ki jaankari milegi\n\n"
        "✍️ Vehicle number bhejo (example: BR05T4014)\n\n"
        "📩 Support: @nanhipari3008"
    )

# vehicle lookup
async def vehicle_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vehicle_no = update.message.text.strip().upper()

    if len(vehicle_no) < 6:
        await update.message.reply_text("❌ Invalid vehicle number")
        return

    try:
        url = API_BASE + vehicle_no
        res = requests.get(url, headers=HEADERS, timeout=15)
        api = res.json()

        data = api.get("data", {})

        owner = data.get("ownership_profile_analytics", {})
        reg = data.get("registration_identity_matrix", {})
        region = data.get("regional_transport_intelligence_grid", {})

        text = (
            "🚘 *Vehicle Information*\n\n"
            "👤 *Owner Information*\n"
            f"• Name : {owner.get('legal_asset_holder', 'N/A')}\n"
            f"• Address : {owner.get('physical_location_address', 'N/A')}\n\n"
            "📄 *Registration Details*\n"
            f"• Vehicle No : {vehicle_no}\n"
            f"• RTO : {region.get('zonal_transport_office', 'N/A')}\n"
            f"• Reg Date : {reg.get('inception_registration_date', 'N/A')}\n"
            f"• Status : {reg.get('registration_status', 'N/A')}"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("⚠️ API fetch error")

# app start
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, vehicle_lookup))

print("🤖 Bot running...")
app.run_polling()
