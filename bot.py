import os
import json
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


FLOW_FILE = 'flow.json'

def load_flow():
    try:
        with open(FLOW_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the start message with the main menu."""
    flow = load_flow()
    start_node = flow.get('start')
    
    if start_node:
        await send_node(update, context, start_node)
    else:
        await update.message.reply_text(
            "Hi! I'm the SecureProxyLite assistant. You can ask me about pricing, setup, or troubleshooting. "
            "Try sending me a question!"
        )

async def send_node(update: Update, context: ContextTypes.DEFAULT_TYPE, node_data: dict):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = []
    options = node_data.get('options', {})
    
    # Create buttons (2 per row is usually good)
    row = []
    for text, callback_id in options.items():
        row.append(InlineKeyboardButton(text, callback_data=callback_id))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        # Edit existing message
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                text=node_data.get('message', "Please select an option:"),
                reply_markup=reply_markup
            )
        except Exception as e:
            # Message might not have changed, safe to ignore
            pass
    else:
        # Send new message
        await update.message.reply_text(
            text=node_data.get('message', "Please select an option:"),
            reply_markup=reply_markup
        )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    node_id = query.data
    
    flow = load_flow()
    node_data = flow.get(node_id)
    
    if node_data:
        await send_node(update, context, node_data)
    else:
        await query.answer("Option not found.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I can answer common questions. Just send me your query.\n"
        "Example: 'How much does it cost?' or 'How to setup?'\n"
        "Or type /start to see the menu."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    qna_data = load_qna()
    
    best_match = None
    
    for entry in qna_data:
        for keyword in entry.get('keywords', []):
            if keyword in user_text:
                best_match = entry.get('answer')
                break
        if best_match:
            break
    
    if best_match:
        await update.message.reply_text(best_match)
    else:
        await update.message.reply_text(
            "I'm sorry, I didn't understand that. Please try rephrasing or type /start to see the menu."
        )

if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN not found in environment variables.")
        exit(1)
        
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    button_handler = CallbackQueryHandler(handle_button)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(button_handler)
    application.add_handler(message_handler)
    
    print("Bot is running...")
    application.run_polling()
