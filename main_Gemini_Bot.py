from typing import Final 
from telegram import Update 
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from . import TELEGRAM_KEY,GEMINI_KEY,GEMENI_ENDPOINTS

TOKEN: Final = TELEGRAM_KEY
BOT_USERNAME: Final = "@Cool_python_test_chat_bot"
GEMINI_API_KEY: Final = GEMINI_KEY
GEMINI_API_ENDPOINT: Final = GEMENI_ENDPOINTS

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
    """Generate response using Gemini API."""
    try:
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}"
        }
        payload = {
            "input_text": input_text,
            "model_name": "your_gemini_model_name_here"  # Adjust the model name based on your Gemini model
        }
        response = requests.post(GEMINI_API_ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["generated_text"]
        else:
            return "Sorry, I couldn't generate a response right now."
    except Exception as e:
        print(f"Error generating response from Gemini: {e}")
        return "Sorry, an error occurred."

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
