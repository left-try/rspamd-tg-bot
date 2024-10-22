import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handle_commands import start, handle_group_message

TOKEN_FILE = "../token.txt"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        print("Token file not found.")
        return None


def main():
    token = load_token()
    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.SUPERGROUP, handle_group_message))
    application.run_polling()


if __name__ == "__main__":
    main()
