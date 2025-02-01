import os
import re
import time
import instaloader
from pytube import YouTube
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.error import TimedOut


# ✅ Secure Telegram Bot Token (directly in the code for simplicity)
TELEGRAM_BOT_TOKEN = "7621045054:AAHTMYYMAlFFi7genLJMkyK8wblf7JPo8E4"

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Error: TELEGRAM_BOT_TOKEN is missing!")


# ✅ Instagram Shortcode Extractor
def extract_instagram_shortcode(url):
    match = re.search(r"instagram\.com/reel/([^/?]+)", url)
    return match.group(1) if match else None


# ✅ Instagram Reels Downloader with Retry Logic
def download_instagram_reel(url, retries=3, delay=60):
    loader = instaloader.Instaloader()
    shortcode = extract_instagram_shortcode(url)
    if not shortcode:
        return None, "❌ Invalid Instagram URL!"

    attempt = 0
    while attempt < retries:
        try:
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            if not post.is_video:
                return None, "❌ This is not a video reel!"
            return post.video_url, None
        except Exception as e:
            print(f"❌ Instagram Error: {str(e)}")
            if "Please wait a few minutes before you try again" in str(e):
                print(f"⚠️ Rate limited. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            else:
                return None, "❌ Failed to download Instagram Reel!"
            attempt += 1
    return None, "❌ Failed to download Instagram Reel after multiple retries!"


# ✅ YouTube Shorts Downloader
def download_youtube_shorts(url):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()  # Best Quality
        filename = f"downloads/{yt.title}.mp4"
        video.download(output_path="downloads", filename=yt.title + ".mp4")
        return filename, None
    except Exception as e:
        print(f"❌ YouTube Error: {str(e)}")
        return None, "❌ Failed to download YouTube Short!"


# ✅ Start Command (Professional Welcome)
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = """
    👋 Welcome to the Video Downloader Bot!

    Please send a valid Instagram Reel or YouTube Shorts link to start downloading the video.

    📌 Created by Kaushik.
    """
    await update.message.reply_text(welcome_message)


# ✅ Message Handler for Downloading
async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    file_path = None  # Default
    error_message = None

    # 🔹 Instagram Reel Download
    if "instagram.com/reel" in url:
        video_url, error_message = download_instagram_reel(url)
        if video_url:
            await update.message.reply_video(video=video_url)
            await update.message.reply_text("✅ Video successfully downloaded!\n\nCreated by Kaushik.")  # Custom message after sending
        else:
            await update.message.reply_text(error_message)
        return

    # 🔹 YouTube Shorts Download
    elif "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("📥 Downloading YouTube Short...")
        file_path, error_message = download_youtube_shorts(url)

    if file_path and os.path.exists(file_path):
        try:
            await update.message.reply_video(
                video=InputFile(file_path),
                timeout=120  # Increase timeout period for larger files
            )
            os.remove(file_path)  # Delete after sending
            await update.message.reply_text("✅ Video successfully downloaded!\n\nCreated by Kaushik.")  # Custom message after sending
        except TimedOut:
            await update.message.reply_text("❌ Request timed out while sending the video.")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text(error_message or "❌ Download failed!")


# ✅ Main Function
def main():
    os.makedirs("downloads", exist_ok=True)  # Ensure 'downloads' folder exists

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Kaushik Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
