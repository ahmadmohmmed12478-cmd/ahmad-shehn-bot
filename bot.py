import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

# تفعيل تسجيل الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ==========================================
# بيانات البوت والإدارة (محدثة نهائياً)
# ==========================================
TOKEN = "9259221454:AAHblTG_WxyKoGoBGkAqQkWp_6NCVqtHB8U"  # توكن بوتك الحقيقي
ADMIN_ID = 7381659405  # الـ ID الشخصي الخاص بك
BANK_ACCOUNT = "8524470"  # رقم حساب بنكك

# مراحل عملية الشحن
SELECT_GAME, SELECT_PACKAGE, ENTER_ID, UPLOAD_RECEIPT = range(4)

# الألعاب والأسعار المحدثة حسب السوق السوداني اليوم
GAMES_DATA = {
    "freefire": {
        "name": "فري فاير (Free Fire) 🔥",
        "packages": {
            "110 جوهرة": "9,500 جنيه",
            "231 جوهرة": "19,500 جنيه",
            "341 جوهرة": "25,000 جنيه",
            "583 جوهرة": "45,000 جنيه",
            "1180 جوهرة": "90,000 جنيه",
            "عضوية أسبوعية": "22,000 جنيه",
            "عضوية شهرية": "88,000 جنيه",
            "بوياه باس": "35,000 جنيه",
        },
    },
    "pubg": {
        "name": "ببجي موبايل (PUBG) 🔫",
        "packages": {
            "60 UC": "6,500 جنيه",
            "325 UC": "32,000 جنيه",
            "660 UC": "64,000 جنيه",
        },
    },
}


# 1. البداية واختيار اللعبة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    keyboard = [
        [
            InlineKeyboardButton(
                GAMES_DATA["freefire"]["name"], callback_data="freefire"
            )
        ],
        [InlineKeyboardButton(GAMES_DATA["pubg"]["name"], callback_data="pubg")],
        [InlineKeyboardButton("📞 تواصل مع الدعم الفني", callback_data="support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"أهلاً بك يا {user_name} في **متجر أحمد لشحن الألعاب في السودان** 🎮🇸🇩\n\n"
        "شحن آمن وفوري بالـ ID عبر تطبيق (بنكك).\n"
        "👇 **اختر اللعبة التي تريد شحنها:**"
    )

    if update.message:
        await update.message.reply_text(
            text, reply_markup=reply_markup, parse_mode="Markdown"
        )
    else:
        await update.callback_query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="Markdown"
        )

    return SELECT_GAME


# 2. اختيار الباقة
async def select_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "support":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 العودة للقائمة الرئيسية", callback_data="back_to_start"
                )
            ]
        ]
        await query.edit_message_text(
            "📞 **خدمة العملاء والدعم الفني:**\nللاستفسارات تواصل مع الإدارة مباشرة.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return SELECT_GAME

    if query.data == "back_to_start":
        return await start(update, context)

    game_key = query.data
    context.user_data["game_key"] = game_key
    game_info = GAMES_DATA[game_key]

    keyboard = []
    for pkg_name, price in game_info["packages"].items():
        button_text = f"{pkg_name}  —  ({price})"
        keyboard.append(
            [InlineKeyboardButton(button_text, callback_data=f"pkg_{pkg_name}")]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 تغيير اللعبة", callback_data="back_
  
