from telegram import Update
from telegram.ext import CallbackContext
import subprocess


def extract_spam_header(result_string):
    lines = result_string.splitlines()
    for line in lines:
        if line.startswith("Spam:"):
            spam_value = line.split(":", 1)[1].strip()
            return spam_value.lower() == "true"
    return None

def check_message(update: Update, context: CallbackContext):
    message = parse_message(update, context)
    filename = 'message.eml'
    with open(filename, 'w') as file:
        file.write(message)
    command = ['rspamc', filename]
    result = subprocess.run(command, capture_output=True, text=True)
    return not extract_spam_header(result.stdout)

def parse_message(update: Update, context: CallbackContext):
    message_text = update.message.text
    sender = update.message.from_user.username
    reply_message = update.message.reply_to_message
    if reply_message is None:
        to_user = update.effective_chat.username
    else:
        to_user = reply_message.from_user.username
    message = f"""
    
    From: <{sender}@example.com>
    To: <{to_user}@example.com>
    Subject: {update.message.message_id}
    Date: {update.message.date}
    MIME-Version: 1.0
    Content-Type: text/plain;
	charset="Windows-1251"
    {message_text}
    """
    return message

