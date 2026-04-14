import json
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes,
    ConversationHandler, CallbackQueryHandler, CallbackContext
)
from telegram.constants import ParseMode
import sqlite3
from datetime import datetime
from database import Database
from admin import AdminPanel
from config import ADMIN_ID

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Savolllarni yuklash
with open('questions.json', 'r', encoding='utf-8') as f:
    QUESTIONS = json.load(f)

# Bot holatlarini belgilash
SINF, FAN, MAVZU, TEST, NATIJA = range(5)
# Admin holatlar
ADMIN_MENU, ADD_QUESTION, SEARCH_QUESTIONS = range(5, 8)

# Database objekti
db = Database()

# Admin panel
admin_panel = AdminPanel()

# ==================== START HANDLER ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Bot boshlash - salomlashuv va qisqa tushuntirish"""
    user = update.effective_user
    
    # Foydalanuvchini bazaga saqlash
    db.add_user(user.id, user.first_name, user.last_name)
    
    greeting = f"""
🎓 *Salom {user.first_name}!*

Sizni *SmartDars* o'quvchi testlash botiga xush kelibsiz!

Ushbu bot orqali:
✅ O'quvchining o'z sinfi va fanida mavzularni o'tib ko'radi
✅ Har mavzu bo'yicha test savollari yechadi
✅ Natiјa va tavsiyalar oladi
✅ Statistika kuzatiladi

*Boshlash uchun /test ni bosing!*
"""
    
    await update.message.reply_text(
        greeting,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            [["🚀 Testni boshlash", "📊 Mening statistikam"]],
            resize_keyboard=True
        )
    )
    
    return ConversationHandler.END


# ==================== SINF TANLASH ====================
async def test_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Test boshlash - sinfni tanlash"""
    keyboard = [
        ["1-sinf", "2-sinf"],
        ["3-sinf", "4-sinf"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📚 *O'quvchining sinfini tanlang:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
    
    return SINF


async def sinf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sinf tanlandi - fanni tanlashga o'tish"""
    sinf_text = update.message.text
    sinf = sinf_text.split('-')[0]  # "1-sinf" -> "1"
    
    if sinf not in QUESTIONS:
        await update.message.reply_text("❌ Iltimos, to'g'ri sinfni tanlang!")
        return SINF
    
    # Foydalanuvchi ma'lumotlarini saqlash
    context.user_data['sinf'] = sinf
    context.user_data['user_id'] = update.effective_user.id
    
    # Mavjud fanlarni olish
    fanlar = list(QUESTIONS[sinf].keys())
    keyboard = [[fan.capitalize()] for fan in fanlar] + [["🔙 Orqaga"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"✅ *{sinf}-sinf* tanlandi!\n\n📖 *Fanni tanlang:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
    
    return FAN


# ==================== FAN TANLASH ====================
async def fan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Fan tanlandi - mavzuni tanlashga o'tish"""
    fan_text = update.message.text.lower()
    sinf = context.user_data['sinf']
    
    if fan_text == "🔙 orqaga":
        return await test_start(update, context)
    
    mavjud_fanlar = list(QUESTIONS[sinf].keys())
    
    if fan_text not in mavjud_fanlar:
        await update.message.reply_text("❌ Iltimos, ro'yxatdan fanni tanlang!")
        return FAN
    
    context.user_data['fan'] = fan_text
    
    # Mavjud mavzularni olish
    mavzular = list(QUESTIONS[sinf][fan_text].keys())
    keyboard = [[mavzu.capitalize()] for mavzu in mavzular] + [["🔙 Orqaga"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        f"✅ *{fan_text}* fani tanlandi!\n\n📝 *Mavzuni tanlang:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
    
    return MAVZU


# ==================== MAVZU TANLASH ====================
async def mavzu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Mavzu tanlandi - test boshlashga o'tish"""
    mavzu_text = update.message.text.lower()
    sinf = context.user_data['sinf']
    fan = context.user_data['fan']
    
    if mavzu_text == "🔙 orqaga":
        return await fan_handler(update, context)
    
    mavjud_mavzular = list(QUESTIONS[sinf][fan].keys())
    
    if mavzu_text not in mavjud_mavzular:
        await update.message.reply_text("❌ Iltimos, ro'yxatdan mavzuni tanlang!")
        return MAVZU
    
    context.user_data['mavzu'] = mavzu_text
    context.user_data['savol_index'] = 0
    context.user_data['to_gri'] = 0
    context.user_data['test_start_time'] = datetime.now()
    
    await update.message.reply_text(
        f"🎯 *Test boshlandi!*\n\n"
        f"📚 Sinf: {sinf}\n"
        f"📖 Fan: {fan}\n"
        f"📝 Mavzu: {mavzu_text.capitalize()}\n\n"
        f"⏰ 5 ta savolga javob berish kerak!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Birinchi savolni yuborish
    return await send_question(update, context)


# ==================== TEST JARAYONI ====================
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Savolni jo'natish"""
    sinf = context.user_data['sinf']
    fan = context.user_data['fan']
    mavzu = context.user_data['mavzu']
    savol_index = context.user_data['savol_index']
    
    savol_list = QUESTIONS[sinf][fan][mavzu]
    
    # Agar testning oxiri bo'lsa
    if savol_index >= len(savol_list):
        return await show_results(update, context)
    
    savol = savol_list[savol_index]
    context.user_data['current_question'] = savol
    
    # Keyboard yaratish (variantlar)
    keyboard = [
        [InlineKeyboardButton(
            text=variant,
            callback_data=f"answer_{savol['id']}_{i}_{variant}"
        )]
        for i, variant in enumerate(savol['variantlar'])
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    question_text = (
        f"❓ *Savol {savol_index + 1}/{len(savol_list)}*\n\n"
        f"{savol['savol']}\n\n"
        f"Javobni tanlang:"
    )
    
    await update.message.reply_text(
        question_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
    
    return TEST


async def answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Javobni tekshirish"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data.split('_')
    selected_answer = callback_data[-1]
    
    savol = context.user_data['current_question']
    togri_javob = savol['togri']
    
    # Javobni bazaga saqlash
    savol_index = context.user_data['savol_index']
    test_session_id = context.user_data.get('test_session_id', 
                                            db.create_test_session(
                                                context.user_data['user_id'],
                                                context.user_data['sinf'],
                                                context.user_data['fan'],
                                                context.user_data['mavzu']
                                            ))
    context.user_data['test_session_id'] = test_session_id
    
    is_correct = selected_answer == togri_javob
    if is_correct:
        context.user_data['to_gri'] += 1
    
    db.save_answer(
        test_session_id,
        savol['id'],
        selected_answer,
        is_correct
    )
    
    # Natija ko'rsatish
    emoji = "✅" if is_correct else "❌"
    result_text = f"{emoji} {'To\'g\'ri javob!' if is_correct else 'Noto\'g\'ri javob!'}\n"
    result_text += f"📌 To'g'ri javob: {togri_javob}"
    
    await query.edit_message_text(
        text=query.message.text + f"\n\n{result_text}",
        parse_mode=ParseMode.MARKDOWN
    )
    
    # Keyingi savolga o'tish
    context.user_data['savol_index'] += 1
    
    import asyncio
    await asyncio.sleep(2)  # 2 soniya kutish
    
    return await send_question(query, context)


# ==================== NATIJA ====================
async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Test natijalarini ko'rsatish"""
    to_gri = context.user_data['to_gri']
    umumiy = len(QUESTIONS[context.user_data['sinf']][context.user_data['fan']][context.user_data['mavzu']])
    foiz = (to_gri / umumiy) * 100
    
    # Natija kategoriyasi
    if foiz >= 80:
        tavsiya = "🌟 *Ajoyib natija!* Siz bu mavzuni yaxshi bilib yuldingiz!"
        emoji = "🏆"
    elif foiz >= 60:
        tavsiya = "👍 *Yaxshi natija!* Olingan bilimni mustahkamlashni tavsiya qilamiz."
        emoji = "⭐"
    elif foiz >= 40:
        tavsiya = "💪 *Orta natija.* Shunga ko'ra yanada ko'proq mashq qilish kerak."
        emoji = "📚"
    else:
        tavsiya = "📖 *Kuchli mashq kerak.* Ushbu mavzuni qayta o'rganish tavsiya qilinadi."
        emoji = "🔄"
    
    results_text = (
        f"{emoji} *TEST NATIJALARI*\n\n"
        f"📊 Natija: *{to_gri}/{umumiy}*\n"
        f"📈 Foiz: *{foiz:.1f}%*\n\n"
        f"{tavsiya}\n\n"
        f"Statistika bazaga saqlandi ✅"
    )
    
    # Test sessiyonini bazada tugatish
    db.finish_test_session(context.user_data['test_session_id'], to_gri, umumiy)
    
    keyboard = [
        [InlineKeyboardButton("📚 Yana test ishlash", callback_data="new_test")],
        [InlineKeyboardButton("🏠 Bosh menyu", callback_data="main_menu")]
    ]
    
    await update.message.reply_text(
        results_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Context ma'lumotlarini tozalash
    context.user_data.clear()
    
    return ConversationHandler.END


async def results_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Natija buttons handler"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "new_test":
        # Yangi test boshlash
        context.user_data.clear()
        msg = await query.message.reply_text(
            "🚀 *Yangi test boshlandi!*\n\n📚 Sinfni tanlang:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(
                [["1-sinf", "2-sinf"], ["3-sinf", "4-sinf"]],
                resize_keyboard=True
            )
        )
        return SINF
    
    elif query.data == "main_menu":
        # Bosh menyu
        context.user_data.clear()
        
        keyboard = [["🚀 Testni boshlash", "📊 Mening statistikam"]]
        
        await query.message.reply_text(
            "🎓 *Salom!*\n\n"
            "Sizni SmartDars o'quvchi testlash botiga xush kelibsiz!\n\n"
            "Boshlash uchun tugmani bosing:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
        
        return ConversationHandler.END


# ==================== STATISTIKA ====================
async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanuvchining statistikasini ko'rsatish"""
    user_id = update.effective_user.id
    stats = db.get_user_statistics(user_id)
    
    if not stats['total_tests']:
        await update.message.reply_text(
            "📊 Henuz test o'tmagansiz. Birinchi testni ishlang!",
            reply_markup=ReplyKeyboardMarkup(
                [["🚀 Testni boshlash"]],
                resize_keyboard=True
            )
        )
        return
    
    avg_score = (stats['correct_answers'] / (stats['total_answers'] if stats['total_answers'] > 0 else 1)) * 100
    
    stats_text = (
        f"📊 *SIZNING STATISTIKANGIZ*\n\n"
        f"🎯 O'tgan testlar: *{stats['total_tests']}*\n"
        f"✅ To'g'ri javoblar: *{stats['correct_answers']}*\n"
        f"❌ Noto'g'ri javoblar: *{stats['wrong_answers']}*\n"
        f"📈 O'rtacha ball: *{avg_score:.1f}%*\n\n"
        f"💪 Davom eting! Ko'proq test ishlang!"
    )
    
    await update.message.reply_text(
        stats_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            [["🚀 Testni boshlash", "📊 Mening statistikam"]],
            resize_keyboard=True
        )
    )


# ==================== CANCEL ====================
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Testni bekor qilish"""
    await update.message.reply_text(
        "❌ Test bekor qilindi.",
        reply_markup=ReplyKeyboardMarkup(
            [["🚀 Testni boshlash"]],
            resize_keyboard=True
        )
    )
    context.user_data.clear()
    return ConversationHandler.END


# ==================== ADMIN PANEL ====================

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Admin menyu"""
    user_id = update.effective_user.id
    
    if not admin_panel.is_admin(user_id):
        await update.message.reply_text("❌ Siz admin emassiz!")
        return ConversationHandler.END
    
    keyboard = [
        ["➕ Savol qo'shish", "🔍 Savol izlash"],
        ["📊 Statistika", "📥 Import/Export"],
        ["⚙️ Admin boshqarish", "🚪 Chiqish"]
    ]
    
    await update.message.reply_text(
        "👨‍💼 *ADMIN PANEL*\n\n"
        "Quyidagilardan birini tanlang:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    
    return ADMIN_MENU


async def admin_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Admin menu qo'shimcha"""
    user_id = update.effective_user.id
    
    if not admin_panel.is_admin(user_id):
        return ConversationHandler.END
    
    text = update.message.text
    
    if "Savol qo'shish" in text:
        msg = admin_panel.init_add_question(user_id)
        await update.message.reply_text(
            msg,
            reply_markup=ReplyKeyboardRemove()
        )
        return ADD_QUESTION
    
    elif "Statistika" in text:
        stats = admin_panel.get_statistics()
        await update.message.reply_text(
            stats,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 Orqaga"]],
                resize_keyboard=True
            )
        )
        return ADMIN_MENU
    
    elif "Savol izlash" in text:
        await update.message.reply_text(
            "🔍 Izlanish uchun so'z kiriting:",
            reply_markup=ReplyKeyboardRemove()
        )
        return SEARCH_QUESTIONS
    
    elif "Chiqish" in text:
        return await start(update, context)
    
    elif "Orqaga" in text:
        return await admin_menu(update, context)
    
    return ADMIN_MENU


async def add_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Savol qo'shish qadamlar"""
    user_id = update.effective_user.id
    
    if not admin_panel.is_admin(user_id):
        return ConversationHandler.END
    
    user_input = update.message.text
    
    if user_input == "🔙 Orqaga":
        return await admin_menu(update, context)
    
    response, finished = admin_panel.add_question_step(user_id, user_input)
    
    await update.message.reply_text(
        response,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )
    
    if finished:
        # Savolllarni qayta yuklash
        global QUESTIONS
        admin_panel.load_questions()
        with open('questions.json', 'r', encoding='utf-8') as f:
            QUESTIONS = json.load(f)
        
        return await admin_menu(update, context)
    
    return ADD_QUESTION


async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Savol izlash"""
    user_id = update.effective_user.id
    
    if not admin_panel.is_admin(user_id):
        return ConversationHandler.END
    
    query = update.message.text
    
    if query == "🔙 Orqaga":
        return await admin_menu(update, context)
    
    results = admin_panel.search_questions(query)
    
    await update.message.reply_text(
        results,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            [["🔙 Orqaga"]],
            resize_keyboard=True
        )
    )
    
    return SEARCH_QUESTIONS


# ==================== MAN SETUP ====================
def main():
    """Bot ishga tushirish"""
    # Token o'z .env fayliga qo'yish kerak
    from config import TOKEN
    
    # Application yaratish
    app = Application.builder().token(TOKEN).build()
    
    # Conversation Handler (Oddiy foydalanuvchilar)
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("test", test_start),
            MessageHandler(filters.TEXT & filters.Regex("🚀 Testni boshlash"), test_start),
            MessageHandler(filters.TEXT & filters.Regex("📊 Mening statistikam"), statistics),
        ],
        states={
            SINF: [MessageHandler(filters.TEXT, sinf_handler)],
            FAN: [MessageHandler(filters.TEXT, fan_handler)],
            MAVZU: [MessageHandler(filters.TEXT, mavzu_handler)],
            TEST: [CallbackQueryHandler(answer_handler, pattern="^answer_")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Admin Conversation Handler
    admin_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("admin", admin_menu),
        ],
        states={
            ADMIN_MENU: [MessageHandler(filters.TEXT, admin_menu_handler)],
            ADD_QUESTION: [MessageHandler(filters.TEXT, add_question_handler)],
            SEARCH_QUESTIONS: [MessageHandler(filters.TEXT, search_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Handlers qo'shish
    app.add_handler(conv_handler)
    app.add_handler(admin_conv_handler)
    app.add_handler(CallbackQueryHandler(results_callback, pattern="^(new_test|main_menu)$"))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("📊 Mening statistikam"), statistics))
    
    # Bot ishga tushirish
    print("🤖 Bot ishga tushdi! Ctrl+C bilan to'xtating...")
    app.run_polling()


if __name__ == '__main__':
    main()
