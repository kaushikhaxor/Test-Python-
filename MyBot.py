import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Replace with your bot token
BOT_TOKEN = "BOT_TOKEN"

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

# Generic function to process file conversions with progress
async def process_file(update, context, document, input_ext, output_ext, conversion_func):
    try:
        # Notify the user about the process start with professional tone
        processing_message = await update.message.reply_text(f"🔄 Processing your {input_ext} file... Please wait.")

        # Download the file
        file = await context.bot.get_file(document.file_id)
        input_file_path = document.file_name
        await file.download_to_drive(input_file_path)

        # Simulate processing delay for better UX (optional)
        for progress in range(0, 101, 10):
            time.sleep(1)  # Simulating processing time
            await processing_message.edit_text(f"🔄 Processing... {progress}%\nConverting {input_ext} to {output_ext}")

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
    # Open the TTF file in binary mode
    with open(input_path, "rb") as ttf_file, open(output_path, "w") as h_file:
        # Write the header information
        h_file.write("// MADE BY KAUSHIK\n")
        h_file.write("// ANY PROBLEM DM @Mrkaushikhaxor AT TELEGRAM\n\n")
        
        # Read the TTF file in chunks of 4 bytes (32-bit values)
        ttf_data = ttf_file.read()

        # Calculate the size (in bytes) and the number of 32-bit values
        size = len(ttf_data)
        num_elements = size // 4  # Each element is 4 bytes (32-bit)

        # Write the size and data array to the .h file
        h_file.write(f"static const unsigned int KAUSHIK_size = {size};\n")
        h_file.write(f"static const unsigned int KAUSHIK_data[{num_elements}] = {{\n")

        # Iterate over the TTF data, breaking it into 4-byte chunks and writing in the required format
        for i in range(0, size, 4):
            # Read a 4-byte chunk
            chunk = ttf_data[i:i+4]
            # Convert to a 32-bit integer
            value = int.from_bytes(chunk, byteorder='big')  # Adjust byte order if needed
            h_file.write(f"    0x{value:08X},\n")

        # Close the array declaration
        h_file.write("};\n")


def convert_h_to_ttf(input_path: str, output_path: str) -> None:
    with open(input_path, "r") as h_file, open(output_path, "wb") as ttf_file:
        for line in h_file:
            if "0x" in line:
                bytes_data = bytes(int(byte, 16) for byte in line.strip().split(",") if "0x" in byte)
                ttf_file.write(bytes_data)

def convert_png_to_h(input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as png_file, open(output_path, "w") as  h_file:
        h_file.write(f"// Converted from {input_path}\n")
        h_file.write(f"// MADE BY KAUSHIK\n")
        h_file.write(f"// ANY PROBLEM DM @Mrkaushikhaxor AT TELEGRAM\n\n")
        h_file.write("const unsigned char image_data[] = {\n")
        while chunk := png_file.read(16):
            h_file.write(", ".join(f"0x{byte:02X}" for byte in chunk) + ",\n")
        h_file.write("};\n")

def convert_h_to_png(input_path: str, output_path: str) -> None:
    with open(input_path, "r") as h_file, open(output_path, "wb") as png_file:
        for line in h_file:
            if "0x" in line:
                bytes_data = bytes(int(byte, 16) for byte in line.strip().split(",") if "0x" in byte)
                png_file.write(bytes_data)

# Main function to set up and run the bot
def main():
    # Initialize the bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers for commands and callbacks
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CallbackQueryHandler(handle_selection))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    # Run the bot
    print("Kaushik Binary Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
