import os
import time
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7796219770:AAGfV11YB4YbuTSZFDLODbt7BJo4qaNfpbE"  # Your bot token

# Function to handle the /start command and display a custom keyboard
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.from_user.first_name  # Get the user's first name

    # Define the custom keyboard layout
    keyboard = [
        [KeyboardButton("🚀 TTF to H"), KeyboardButton("🚀 H to TTF")],
        [KeyboardButton("🚀 PNG to H"), KeyboardButton("🚀 H to PNG")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Welcome message
    response = f'''👋 Welcome, {user_name}!
I'm here to assist you with file conversions. 😎

📂 Available conversions:
   - TTF to H
   - H to TTF
   - PNG to H
   - H to PNG

💬 For assistance: @Mrkaushikhaxor
✅ Stay updated: https://t.me/KaushikCracking

Enjoy the experience! 🚀'''

    await update.message.reply_text(response, reply_markup=reply_markup)

# Function to handle keyboard selections
async def handle_keyboard_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_choice = update.message.text

    # Handle user selection
    conversion_types = {
        "🚀 TTF to H": "ttf_to_h",
        "🚀 H to TTF": "h_to_ttf",
        "🚀 PNG to H": "png_to_h",
        "🚀 H to PNG": "h_to_png",
    }

    if user_choice in conversion_types:
        context.user_data["conversion_type"] = conversion_types[user_choice]
        await update.message.reply_text(f"✅ You selected: {user_choice}\n📂 Please upload your file to proceed.")
    else:
        await update.message.reply_text("⚠️ Invalid option. Please select a valid conversion type.")

# Function to handle file uploads and initiate conversion
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document
    conversion_type = context.user_data.get("conversion_type")

    if not conversion_type:
        await update.message.reply_text("⚠️ Please select a conversion type first.")
        return

    # Determine valid extensions for the selected conversion
    valid_extensions = {
        "ttf_to_h": ".ttf",
        "h_to_ttf": ".h",
        "png_to_h": ".png",
        "h_to_png": ".h",
    }

    input_ext = valid_extensions.get(conversion_type)
    output_ext = input_ext.replace(".ttf", ".h").replace(".h", ".ttf").replace(".png", ".h").replace(".h", ".png")
    conversion_funcs = {
        "ttf_to_h": convert_ttf_to_h,
        "h_to_ttf": convert_h_to_ttf,
        "png_to_h": convert_png_to_h,
        "h_to_png": convert_h_to_png,
    }

    if document.file_name.endswith(input_ext):
        await process_file(update, context, document, input_ext, output_ext, conversion_funcs[conversion_type])
    else:
        await update.message.reply_text(f"⚠️ Invalid file format. Please upload a file with the `{input_ext}` extension.")

# Function to process the file conversion
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
#ttf > .h
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
            if "0x" in line:  # Check for lines containing hex values
                hex_values = [
                    int(value, 16) for value in line.strip().split(",") if "0x" in value
                ]
                for value in hex_values:
                    # Convert the 32-bit integer into 4 bytes and write to file
                    ttf_file.write(value.to_bytes(4, byteorder="big"))

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
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_keyboard_selection))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("Kaushik Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
