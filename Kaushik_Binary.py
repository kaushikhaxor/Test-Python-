import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Replace with your bot token
BOT_TOKEN = "7796219770:AAGfV11YB4YbuTSZFDLODbt7BJo4qaNfpbE"  # Add Bot Token Else Give Err

# User nickname (can be dynamically set if desired)
USER_NICKNAME = "KAUSHIK"

# Function to handle the /start command with the customized message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.from_user.first_name  # Get the user's first name
    response = f'''👋 Welcome, {user_name}!
I'm your best bot, here to help you with file conversions. 😎

📂 Choose a conversion type:
   - TTF to H
   - H to TTF
   - PNG to H
   - H to PNG

🔄 Use /convert to get started.

💬 Need Help: @Mrkaushikhaxor

✅ Join here: https://t.me/KaushikCracking to stay connected!

Enjoy the experience!'''
    await update.message.reply_text(response)

# Function to handle the /convert command and show the selection panel
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("TTF to H", callback_data="ttf_to_h"),
            InlineKeyboardButton("H to TTF", callback_data="h_to_ttf"),
        ],
        [
            InlineKeyboardButton("PNG to H", callback_data="png_to_h"),
            InlineKeyboardButton("H to PNG", callback_data="h_to_png"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📂 Choose a conversion type below:", reply_markup=reply_markup)

# Function to handle selection from the panel
async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Save the selected conversion type
    context.user_data["conversion_type"] = query.data

    # Modify the popup message to be more professional
    await query.edit_message_text(
        f"You've selected: {query.data.replace('_', ' ').title()}\n\n"
        "📤 Please upload the file you wish to convert. Our bot will handle the rest for you."
    )

# Function to handle file uploads
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document
    conversion_type = context.user_data.get("conversion_type")

    if not conversion_type:
        await update.message.reply_text("Please use /convert to select a conversion type first.")
        return

    # Process based on the selected conversion type
    if conversion_type == "ttf_to_h" and document.file_name.endswith(".ttf"):
        await process_file(update, context, document, ".ttf", ".h", convert_ttf_to_h)
    elif conversion_type == "h_to_ttf" and document.file_name.endswith(".h"):
        await process_file(update, context, document, ".h", ".ttf", convert_h_to_ttf)
    elif conversion_type == "png_to_h" and document.file_name.endswith(".png"):
        await process_file(update, context, document, ".png", ".h", convert_png_to_h)
    elif conversion_type == "h_to_png" and document.file_name.endswith(".h"):
        await process_file(update, context, document, ".h", ".png", convert_h_to_png)
    else:
        await update.message.reply_text("⚠️ Invalid file for the selected conversion type. Please upload the correct file.")

# Generic function to process file conversions with animation
async def process_file(update, context, document, input_ext, output_ext, conversion_func):
    try:
        # Notify the user about the process start
        processing_message = await update.message.reply_text(f"🔄 Processing your {input_ext} file... Please wait.")

        # Download the file
        file = await context.bot.get_file(document.file_id)
        input_file_path = document.file_name
        await file.download_to_drive(input_file_path)

        # Simulate processing with animation
        animation = [
            "▰▱▱▱▱▱▱▱▱▱ 10% Please Wait...",
            "▰▰▱▱▱▱▱▱▱▱ 20% Please Wait...",
            "▰▰▰▱▱▱▱▱▱▱ 30% Please Wait...",
            "▰▰▰▰▱▱▱▱▱▱ 40% Please Wait...",
            "▰▰▰▰▰▱▱▱▱▱ 50% Halfway There...",
            "▰▰▰▰▰▰▱▱▱▱ 60% Processing...",
            "▰▰▰▰▰▰▰▱▱▱ 70% Almost Done...",
            "▰▰▰▰▰▰▰▰▱▱ 80% Finalizing...",
            "▰▰▰▰▰▰▰▰▰▱ 90% Wrapping Up...",
            "▰▰▰▰▰▰▰▰▰▰ 100% Done!",
        ]

        for frame in animation:
            time.sleep(1)  # Simulating processing time
            await processing_message.edit_text(f"🔄 {frame}")

        # Convert the file
        output_file_path = input_file_path.replace(input_ext, output_ext)
        conversion_func(input_file_path, output_file_path)

        # Notify the user about the successful conversion
        await processing_message.edit_text("✅ Conversion complete! Your file is ready. Sending now...")

        # Send the converted file back to the user
        await update.message.reply_document(document=open(output_file_path, "rb"))
        await update.message.reply_text(f"🎉 Here is your converted {output_ext} file! Enjoy it! 😁")

        # Clean up temporary files
        os.remove(input_file_path)
        os.remove(output_file_path)

        # Ask if the user wants to do another conversion
        await update.message.reply_text("🔁 Do you want to convert another file?\n Use /convert to start again.")

    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {e}")

# Functions for specific conversions
def convert_ttf_to_h(input_path: str, output_path: str) -> None:
    # Conversion logic
    pass

def convert_h_to_ttf(input_path: str, output_path: str) -> None:
    # Conversion logic
    pass

def convert_png_to_h(input_path: str, output_path: str) -> None:
    # Conversion logic
    pass

def convert_h_to_png(input_path: str, output_path: str) -> None:
    # Conversion logic
    pass

# Main function to set up and run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers for commands and callbacks
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CallbackQueryHandler(handle_selection))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("Kaushik Binary Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
