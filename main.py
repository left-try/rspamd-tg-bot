import logging
import os

from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

from check_message import check_message

TOKEN_FILE = "token.txt"

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        print("Token file not found.")
        return None

BOT_TOKEN = load_token()
ADMIN_CHAT_ID = -1

async def handle_group_message(update: Update, context: CallbackContext):
    result = check_message(update, context)
    if not result:
        spam_msg_id = update.message.id
        spam_user_id = update.message.from_user.id
        group = update.effective_chat
        await update.message.delete()
        await context.bot.ban_chat_member(group.id, spam_user_id)
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"Message {spam_msg_id} in group {group.username}:  was deleted. Sender: {spam_user_id}"
        )

async def set_chat_as_admin(update: Update, context: CallbackContext):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        ADMIN_CHAT_ID = update.effective_chat.id
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text="Admin chat set.")

async def start(update: Update, context: CallbackContext):
    chat_admins = await update.effective_chat.get_administrators()
    if update.effective_user in (admin.user for admin in chat_admins):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot started.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Unauthorized access!")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_as_admin_chat", set_chat_as_admin))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUP, handle_group_message))
    application.run_polling()

if __name__ == "__main__":
    main()
