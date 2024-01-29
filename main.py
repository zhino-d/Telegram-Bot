import threading
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

class CountdownThread(threading.Thread):
    def __init__(self, update, count):
        super().__init__()
        self.update = update
        self.count = count

    def run(self):
        for i in range(self.count + 1):
            time.sleep(1)
            self.update.message.reply_text(str(i))

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(f"Hello {user.first_name}! I'm your bot. How can I help you?")

def handle_number(update: Update, context: CallbackContext) -> None:
    try:
        count = int(update.message.text)
        countdown_thread = CountdownThread(update, count)
        countdown_thread.start()
    except ValueError:
        update.message.reply_text("Please enter a valid number.")

def main() -> None:
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the /start command handler
    dp.add_handler(CommandHandler("start", start))

    # Register a message handler to handle numbers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_number))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop (e.g., by pressing Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
