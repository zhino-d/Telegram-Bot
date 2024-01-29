import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import logging

class CountdownThread(threading.Thread):
    def __init__(self, update, count):
        super().__init__()
        self.update = update
        self.count = count

    def run(self):
        for i in range(self.count + 1):
            time.sleep(1)
            self.update.message.reply_text(str(i))

class ChatGPTThread(threading.Thread):
    def __init__(self, update, message):
        super().__init__()
        self.update = update
        self.message = message

    def run(self):
        openai.api_key = 'API'

        # Send user's message to ChatGPT for processing using the correct endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or the model you are using
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": self.message.text},
            ],
            max_tokens=100
        )

        # Send ChatGPT's response back to the user
        self.update.message.reply_text(response['choices'][0]['message']['content'])


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(f"Hello {user.first_name}! I'm your bot. How can I help you?")

def handle_input(update: Update, context: CallbackContext) -> None:
    if update.message.text.lower() == 'start':
        return start(update, context)

    try:
        count = int(update.message.text)
        countdown_thread = CountdownThread(update, count)
        countdown_thread.start()
    except ValueError:
        # User input is not a number, create a ChatGPTThread
        chatgpt_thread = ChatGPTThread(update, update.message)
        chatgpt_thread.start()


def error_handler(update: Update, context: CallbackContext) -> None:
    """Log any errors that occur."""
    logging.error(f"Update {update} caused error {context.error}")

def main() -> None:
    updater = Updater("BOT_TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the /start command handler
    dp.add_handler(CommandHandler("start", start))

    # Register a message handler to handle user input
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_input))

    # Add the error handler
    dp.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop (e.g., by pressing Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
