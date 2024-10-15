from telegram import Update
from telegram.ext import CallbackContext

def check_message(update: Update, context: CallbackContext):
    message = parse_message(update, context)
    #TODO
    print(message)
    return True

def parse_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    message_text = update.message.text
    sender = update.message.from_user.username
    reply_message = update.message.reply_to_message
    if reply_message is None:
        to_user = update.effective_chat.username
    else:
        to_user = reply_message.from_user.username
    message = f"""
    from: {sender}
    to: {to_user}
    type: text/plain
    {message_text}
    """
    return message

