import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from datetime import datetime

# اطلاعات ربات و گروه شما
TOKEN = os.getenv("TOKEN", "توکن_ربات_شما")
GROUP_ID = int(os.getenv("GROUP_ID", "-1002479614516"))  # آی‌دی گروه
ADMIN_ID = int(os.getenv("ADMIN_ID", "364482277"))       # آی‌دی ادمین (شما)

# فعال‌سازی لاگ‌گیری
logging.basicConfig(level=logging.INFO)

# پیام تست
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات فعال است.")

# خاموش کردن گروه
async def shutdown_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permissions = ChatPermissions(can_send_messages=False)
    await context.bot.set_chat_permissions(chat_id=GROUP_ID, permissions=permissions)
    await context.bot.send_message(chat_id=GROUP_ID, text="⛔️ گروه از ساعت {} غیرفعال شد.".format(datetime.now().strftime('%H:%M')))

# روشن کردن گروه
async def enable_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permissions = ChatPermissions(can_send_messages=True)
    await context.bot.set_chat_permissions(chat_id=GROUP_ID, permissions=permissions)
    await context.bot.send_message(chat_id=GROUP_ID, text="✅ گروه از ساعت {} دوباره فعال شد.".format(datetime.now().strftime('%H:%M')))

# ارسال پیام به ادمین
async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        message = "پیام جدید از کاربر:\n" + ' '.join(context.args)
        await context.bot.send_message(chat_id=ADMIN_ID, text=message)
        await update.message.reply_text("پیام شما به ادمین ارسال شد.")
    else:
        await update.message.reply_text("لطفاً بعد از /contact پیام خود را بنویسید.")

# تعریف اپلیکیشن
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("off", shutdown_group))
app.add_handler(CommandHandler("on", enable_group))
app.add_handler(CommandHandler("contact", contact_admin))

# اجرای ربات
app.run_polling()
