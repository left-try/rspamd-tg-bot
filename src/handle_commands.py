from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from src.scan_message import check_message
from src.db import set_up_redis


async def handle_group_message(update: Update, context: CallbackContext):
    r = set_up_redis('localhost', 6379)
    result = await check_message(update, context)
    if not result:
        spam_msg_id = update.message.id
        spam_user = update.message.from_user
        group = update.effective_chat
        await context.bot.delete_message(group.id, spam_msg_id)
        admins = await update.effective_chat.get_administrators()
        for admin in admins:
            admin_chat_id = r.hget(str(admin.user.id), 'admin_chat_id')
            print(admin_chat_id)
            if admin_chat_id is not None:
                await context.bot.send_message(
                    chat_id=int(admin_chat_id.decode('utf-8')),
                    text=f"Message {spam_msg_id} in group {group.effective_name}:  was deleted. Sender: {spam_user.username}"
                )


async def start(update: Update, context: CallbackContext):
    r = set_up_redis('localhost', 6379)
    keyboard = [[
        "/start"
    ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    admin = str(update.effective_user.id)
    chat_id = str(update.effective_chat.id)
    r.hset(admin, 'admin_chat_id', chat_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot set up.", reply_markup=reply_markup)