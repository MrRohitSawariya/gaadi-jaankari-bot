import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8410893007:AAEaTw2xpkpjbTKLp5hx7V8R5r6tbkXZ6cs"
API_BASE = "https://org.proportalxc.workers.dev/?rc="

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚗 *Welcome to Gaadi Jaankari Bot*\n\n"
        "Vehicle number bhejo (example: DL07P5121)\n\n"
        "📩 Support: @nanhipari3008",
        parse_mode="Markdown"
    )

# VEHICLE LOOKUP
async def vehicle_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vehicle_no = update.message.text.strip().upper()
    if len(vehicle_no) < 6:
        return

    try:
        response = requests.get(API_BASE + vehicle_no, headers=HEADERS, timeout=15)
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

            "👤 *Owner Information*\n"
            f"• Name : `{owner.get('legal_asset_holder','N/A')}`\n"
            f"• Guardian : `{owner.get('primary_guardian_alias','N/A')}`\n"
            f"• Address : `{owner.get('physical_location_address','N/A')}`\n\n"

            "🚗 *Registration Details*\n"
            f"• Vehicle No : `{vehicle_no}`\n"
            f"• Issuing Authority : `{reg.get('issuing_authority','N/A')}`\n"
            f"• Registration Date : `{life.get('inception_registration_date','N/A')}`\n"
            f"• Fitness Valid Till : `{life.get('fitness_certification_expiry','N/A')}`\n\n"

            "🛡 *Insurance*\n"
            f"• Company : `{insurance.get('underwriting_organization','N/A')}`\n"
            f"• Valid Till : `{insurance.get('protection_validity_limit','N/A')}`\n"
            f"• Risk Level : `{insurance.get('risk_exposure_rating','N/A')}`\n\n"

            "💰 *Finance / Legal*\n"
            f"• Hypothecation : `{finance.get('hypothecation_lien_status','N/A')}`\n"
            f"• Lien Holder : `{finance.get('lien_holder_institution','N/A')}`\n\n"

            "📍 *RTO & Tax*\n"
            f"• RTO Office : `{region.get('zonal_transport_office','N/A')}`\n"
            f"• Road Tax : `{region.get('regional_road_usage_tax','N/A')}`\n"
        )

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error fetching data\n{e}")

# BOT RUN
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, vehicle_lookup))

print("🤖 Bot running...")
app.run_polling(drop_pending_updates=True)
