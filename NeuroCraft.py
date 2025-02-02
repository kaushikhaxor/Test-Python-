import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Replace with your own Bot Token
TOKEN = '7691513668:AAF1D4yxxCwwOZN5M5J6zIJUcjNQiqDt8_U'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    nickname = user.first_name  # Use first name as nickname

    # Keyboard Button बनाएं
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    about_button = KeyboardButton("ℹ️ About NeuroCraft")  # Fixed: Corrected variable name
    markup.add(about_button)  

    welcome_message = (
        f"👋 *Hello {nickname}*,\n\n"
        "*I’m your AI assistant, ready to generate code and solve problems.*\n"
        "*What can I help with? Just type your query, and I’ll deliver the best solutions!* 🚀\n\n"
        "*Created by Kaushik, this AI bot offers capabilities beyond ChatGPT to help you succeed faster!* ⚡"
    )
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "ℹ️ About NeuroCraft")  # Fixed: Added message handler
def about_info(message):
    about_text = """🚀 Kaushik NeuroCraft  
An AI coding assistant designed to generate, debug, and optimize code effortlessly.  

👨‍💻 Developer: *Kaushik (@Mrkaushikhaxor)*  
📅 Launched: *June 25, 2023*  
⚡ Speed: *Super Fast & Optimized*  
🛠️ Supports: *Python, Java, C++ (more coming soon!)*  

💡 Key Features:  
✔ Code Generation & Debugging  
✔ AI-Powered Tech Assistance  
✔ Continuous Learning & Improvement  

🌍 Upcoming: *More languages, smarter AI & web version.*  

👉 *Stay tuned for updates!*"""

    bot.send_message(message.chat.id, about_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)  # Handle all other messages
def pending(message):
    pending_message = (
        "*NOTICE:*\n"
        "The bot is currently under development. Soon, NeuroCraft will launch, offering a powerful AI experience beyond ChatGPT. Stay tuned!\n\n"
        "*Rewards: @Mrkaushikhaxor*"
    )
    bot.send_message(message.chat.id, pending_message, parse_mode="Markdown")

print("🤖 NeuroCraft is Running....")
if __name__ == "__main__":
    bot.polling(none_stop=True)
