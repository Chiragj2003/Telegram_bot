from typing import Final 
from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai
from . import OPEN_API_KEY,TELEGRAM_KEY

TOKEN: Final = TELEGRAM_KEY
BOT_USERNAME : Final = "@Cool_python_test_chat_bot"

OPENAI_API_KEY: Final = OPEN_API_KEY

# Initialize OpenAI API client
openai.api_key = OPENAI_API_KEY

async def start_command(update: Update, context: CallbackContext):
    """Handle the /start command."""
    await update.message.reply_text("Welcome to this chat bot!")

async def help_command(update: Update, context: CallbackContext):
    """Handle the /help command."""
    await update.message.reply_text("How can I help you?")

async def custom_command(update: Update, context: CallbackContext):
    """Handle the /custom command."""
    await update.message.reply_text("This is a custom command.")

async def handle_message(update: Update, context: CallbackContext):
    """Handle incoming messages."""
    message_type = update.message.chat.type
    text = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: '{text}'")
    
    response = await generate_response(text)
    
    print("Bot:", response)
    await update.message.reply_text(response)

async def generate_response(input_text: str) -> str:
    """Generate response using GPT-3.5 model."""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ]
        )
        return completion.choices[0].message["content"]
    except Exception as e:
        print(f"Error generating response from GPT-3.5: {e}")
        return "Sorry, I couldn't generate a response right now."

async def error(update: Update, context: CallbackContext):
    """Log errors."""
    print(f"Update {update} caused error: {context.error}")

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands 
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Message handler 
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    # Error handler 
    app.add_error_handler(error)

    # Polling the bot 
    print("Polling...")
    app.run_polling(poll_interval=3)
