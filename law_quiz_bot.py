import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد تسجيل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# الأسئلة والأجوبة
questions = [
    {
        "question": "ما هو تعريف القانون؟",
        "options": ["مجموعة قواعد ملزمة", "نظرية علمية", "رأي شخصي"],
        "answer": "مجموعة قواعد ملزمة"
    },
    {
        "question": "من يسن القوانين؟",
        "options": ["القاضي", "البرلمان", "المحامي"],
        "answer": "البرلمان"
    },
    {
        "question": "ما هو الدستور؟",
        "options": ["كتاب قانوني", "القانون الأعلى في الدولة", "مذكرة"],
        "answer": "القانون الأعلى في الدولة"
    }
]

user_data = {}

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    question = random.choice(questions)
    user_data[chat_id] = question
    reply_markup = ReplyKeyboardMarkup(
        [[opt] for opt in question["options"]],
        one_time_keyboard=True,
        resize_keyboard=True
    )
    await update.message.reply_text(question["question"], reply_markup=reply_markup)

# التحقق من الإجابة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_answer = update.message.text
    if chat_id in user_data:
        correct_answer = user_data[chat_id]["answer"]
        if user_answer == correct_answer:
            await update.message.reply_text("إجابة صحيحة!")
        else:
            await update.message.reply_text(f"إجابة خاطئة! الصح هي: {correct_answer}")
        del user_data[chat_id]
    else:
        await update.message.reply_text("أرسل /start حتى نبدأ الاختبار.")

# التشغيل
async def main():
    bot_token = "8089643788:AAEJ8z5jEXKRFTHlQyFLGdpjzM8YfDG7KHQ"
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
