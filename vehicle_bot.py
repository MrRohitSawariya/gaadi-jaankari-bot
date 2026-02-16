import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 🔑 BOT TOKEN (as you asked)
BOT_TOKEN = "8410893007:AAEaTw2xpkpjbTKLp5hx7V8R5r6tbkXZ6cs"

API_BASE = "https://org.proportalxc.workers.dev/?rc=br05t4014&vehicle="

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚗 *Welcome to Gaadi Jaankari Bot*\n\n"
        "👉 Vehicle number bhejo\n"
        "Example: DL01FS1211\n\n"
        "🛠 Support: @nahipari3008",
        parse_mode="Markdown"
    )

# vehicle lookup
async def vehicle_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vehicle_no = update.message.text.strip().upper()

    if len(vehicle_no) < 6:
        return

    try:
        response = requests.get(
            API_BASE + vehicle_no,
            headers=HEADERS,
            timeout=15
        )
        api = response.json()

        data = api.get("data", {})

        owner = data.get("ownership_profile_analytics", {})
        life = data.get("lifecycle_compliance_timeline", {})
        insurance = data.get("insurance_security_audit_report", {})
        finance = data.get("financial_legal_encumbrance_vault", {})
        region = data.get("regional_transport_intelligence_grid", {})
        reg = data.get("registration_identity_matrix", {})

        text = (
            "🚘 *Vehicle Information*\n\n"
            "👤 *Owner Info*\n"
            f"• Name: `{owner.get('legal_asset_holder','NA')}`\n"
            f"• Guardian: `{owner.get('primary_guardian_alias','NA')}`\n"
            f"• Address: `{owner.get('physical_location_address','NA')}`\n\n"

            "📄 *Registration*\n"
            f"• Vehicle No: `{vehicle_no}`\n"
            f"• RTO: `{reg.get('issuing_authority','NA')}`\n"
            f"• Reg Date: `{life.get('inception_registration_date','NA')}`\n"
            f"• Fitness Till: `{life.get('fitness_certification_expiry','NA')}`\n\n"

            "🛡 *Insurance*\n"
            f"• Company: `{insurance.get('underwriting_organization','NA')}`\n"
            f"• Valid Till: `{insurance.get('protection_validity_limit','NA')}`\n"
            f"• Risk: `{insurance.get('risk_exposure_rating','NA')}`\n\n"

            "💰 *Finance / Legal*\n"
            f"• Hypothecation: `{finance.get('hypothecation_lien_status','NA')}`\n"
            f"• Lien Holder: `{finance.get('lien_holder_institution','NA')}`\n\n"

            "🏢 *RTO / Tax*\n"
            f"• RTO Office: `{region.get('zonal_transport_office','NA')}`\n"
            f"• Road Tax: `{region.get('regional_road_usage_tax','NA')}`"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception:
        await update.message.reply_text("⚠️ Error fetching vehicle data")

# bot run
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, vehicle_lookup))

print("🤖 Bot running...")
app.run_polling(drop_pending_updates=True)
