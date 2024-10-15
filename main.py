import logging
import os

from telegram import Update, ChatPermissions
from telegram.constants import ChatType
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

admin_chat_id = -1

async def handle_group_message(update: Update, context: CallbackContext):
    result = check_message(update, context)
    if not result:
        spam_msg_id = update.message.id
        spam_user = update.message.from_user
        group = update.effective_chat
        print(group.effective_name)
        print(spam_user.username)
        print(update.message)
        await context.bot.delete_message(group.id, spam_msg_id)
        await context.bot.send_message(
            chat_id=admin_chat_id,
            text=f"Message {spam_msg_id} in group {group.effective_name}:  was deleted. Sender: {spam_user.username}"
        )

async def start(update: Update, context: CallbackContext):
    global admin_chat_id
    admin_chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=admin_chat_id, text="Bot set up.")

def main():
    token = load_token()
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.SUPERGROUP, handle_group_message))
    application.run_polling()

if __name__ == "__main__":
    main()
