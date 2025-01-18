import os
import time
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7796219770:AAGfV11YB4YbuTSZFDLODbt7BJo4qaNfpbE"  # Your bot token

# Function to handle the /start command and display a custom keyboard
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the custom keyboard layout (2 rows)
    keyboard = [
        [KeyboardButton("🚀 TTF to H"), KeyboardButton("🚀 H to TTF")],
        [KeyboardButton("🚀 PNG to H"), KeyboardButton("🚀 H to PNG")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 **Welcome to Kaushik's Bot!**\n\n"
        "I can help you convert files easily. Use the options below to start your conversion journey. 🚀",
        reply_markup=reply_markup
    )


# Function to handle user responses from the keyboard
async def handle_keyboard_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_choice = update.message.text  # Capture the button text clicked by the user

    # Respond based on the button pressed
    if user_choice == "🚀 TTF to H":
        context.user_data["conversion_type"] = "ttf_to_h"
        await update.message.reply_text("You selected: **TTF to H**.\n📂 Please upload your TTF file to proceed.")
    elif user_choice == "🚀 H to TTF":
        context.user_data["conversion_type"] = "h_to_ttf"
        await update.message.reply_text("You selected: **H to TTF**.\n📂 Please upload your H file to proceed.")
    elif user_choice == "🚀 PNG to H":
        context.user_data["conversion_type"] = "png_to_h"
        await update.message.reply_text("You selected: **PNG to H**.\n📂 Please upload your PNG file to proceed.")
    elif user_choice == "🚀 H to PNG":
        context.user_data["conversion_type"] = "h_to_png"
        await update.message.reply_text("You selected: **H to PNG**.\n📂 Please upload your H file to proceed.")
    else:
        await update.message.reply_text("⚠️ Unknown option selected. Please try again.")


# Function to handle file uploads
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document
    conversion_type = context.user_data.get("conversion_type")

    if not conversion_type:
        await update.message.reply_text("⚠️ **Please select a conversion type first using the keyboard.**")
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
        await update.message.reply_text("⚠️ Invalid file format for the selected conversion type. Please upload the correct file.")


# Generic function to process file conversions
async def process_file(update, context, document, input_ext, output_ext, conversion_func):
    try:
        # Notify the user about the process start
        processing_message = await update.message.reply_text(f"🔄 **Processing your {input_ext} file... Please wait.**")

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
        await processing_message.edit_text("✅ **Conversion complete! Your file is ready. Sending now...**")

        # Send the converted file back to the user
        await update.message.reply_document(document=open(output_file_path, "rb"))
        await update.message.reply_text(f"🎉 Here is your converted `{output_ext}` file! Enjoy it! 😁")

        # Clean up temporary files
        os.remove(input_file_path)
        os.remove(output_file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred: {e}")


# Conversion Functions
def convert_ttf_to_h(input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as ttf_file, open(output_path, "w") as h_file:
        h_file.write("// Converted by Kaushik's Bot\n")
        ttf_data = ttf_file.read()
        size = len(ttf_data)
        h_file.write(f"const unsigned char ttf_data[{size}] = {{\n")
        h_file.write(", ".join(f"0x{byte:02X}" for byte in ttf_data))
        h_file.write("\n};\n")


def convert_h_to_ttf(input_path: str, output_path: str) -> None:
    with open(input_path, "r") as h_file, open(output_path, "wb") as ttf_file:
        for line in h_file:
            if "0x" in line:
                bytes_data = bytes(int(byte, 16) for byte in line.strip().split(",") if "0x" in byte)
                ttf_file.write(bytes_data)


def convert_png_to_h(input_path: str, output_path: str) -> None:
    with open(input_path, "rb") as png_file, open(output_path, "w") as h_file:
        h_file.write("// Converted from PNG\n")
        h_file.write("const unsigned char png_data[] = {\n")
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
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_keyboard_selection))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("Kaushik Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
