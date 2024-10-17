from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from check_message import check_message

admin_chat_id = -1

async def handle_group_message(update: Update, context: CallbackContext):
    result = await check_message(update, context)
    if not result:
        spam_msg_id = update.message.id
        spam_user = update.message.from_user
        group = update.effective_chat
        await context.bot.delete_message(group.id, spam_msg_id)
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"Message {spam_msg_id} in group {group.effective_name}:  was deleted. Sender: {spam_user.username}"
        )


async def start(update: Update, context: CallbackContext):
    keyboard = [[
        "/start"
    ]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    global admin_chat_id
    admin_chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=admin_chat_id, text="Bot set up.", reply_markup=reply_markup)