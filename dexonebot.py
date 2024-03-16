import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables from .env file yeah
load_dotenv()

# Get Telegram bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Dictionary to store user states
user_states = {}


def start(update: Update, context: CallbackContext) -> None:
    """Starts the conversation and asks the user for their username."""
    update.message.reply_text('Enter your username:')
    user_states[update.message.chat_id] = {'state': 'username'}


def handle_username(update: Update, context: CallbackContext) -> None:
    """Handles the username input and asks for the user ID."""
    username = update.message.text
    chat_id = update.message.chat_id
    user_states[chat_id]['username'] = username
    update.message.reply_text('Enter your user ID:')
    user_states[chat_id]['state'] = 'user_id'


def handle_user_id(update: Update, context: CallbackContext) -> None:
    """Handles the user ID input and asks for the new password."""
    user_id = update.message.text
    chat_id = update.message.chat_id
    user_states[chat_id]['user_id'] = user_id
    update.message.reply_text('Enter your new password:')
    user_states[chat_id]['state'] = 'password'


def handle_password(update: Update, context: CallbackContext) -> None:
    """Handles the password input and simulates changing the password."""
    new_password = update.message.text
    chat_id = update.message.chat_id
    username = user_states[chat_id]['username']
    user_states.pop(chat_id)  # Remove user state once the conversation is done
    update.message.reply_text(f"Password for user {username} has been successfully changed.")
    

def cancel(update: Update, context: CallbackContext) -> None:
    """Cancels the current conversation."""
    chat_id = update.message.chat_id
    user_states.pop(chat_id, None)
    update.message.reply_text('The operation has been canceled.')


def main() -> None:
    """Run the bot."""
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^/cancel$'), cancel))
    dispatcher.add_handler(MessageHandler(Filters.text & (Filters.private & ~Filters.command), handle_conversation))

    updater.start_polling()
    updater.idle()


def handle_conversation(update: Update, context: CallbackContext) -> None:
    """Handles the ongoing conversation."""
    chat_id = update.message.chat_id

    if chat_id in user_states:
        state = user_states[chat_id]['state']

        if state == 'username':
            handle_username(update, context)
        elif state == 'user_id':
            handle_user_id(update, context)
        elif state == 'password':
            handle_password(update, context)
    else:
        update.message.reply_text("Please start the conversation using /start command.")


if __name__ == '__main__':
    main()
