# 🤖 Telegram Bot Alert System

This guide walks you through creating a Telegram bot and sending automated messages using Python. Great for notifications like visa slot availability, monitoring scripts, or alerts.

---

## 📦 Prerequisites

- Python 3.8+
- `pip` installed
- Telegram app on your phone
- Internet access from your machine (EC2, local, etc.)

---

## 🛠️ Step-by-Step Setup

### 1. 🚀 Create Your Telegram Bot

1. Open Telegram.
2. Search for `@BotFather` and start a chat.
3. Send: `/start`
4. Send: `/newbot`
5. Follow the prompts:
   - Give it a name (e.g., `Visa Slot Bot`)
   - Give it a username (must end with `bot`, like `visa_slot_checker_bot`)
6. BotFather will reply with your **bot token**:

✅ **Save this token securely.**

---

### 2. 🧑‍💻 Get Your Chat ID

1. Open Telegram and send **any message** (like `hi`) to your bot.
2. Visit the following URL in a browser:

Replace `<YOUR_BOT_TOKEN>` with your real token.

3. In the response, look for:
```json
"chat": {
  "id": 123456789,
  ...
}



3. 🐍 Set Up Python Script
Install required libraries:
bash
Copy
Edit
python3 -m venv visa-bot-env
source visa-bot-env/bin/activate
pip install requests python-dotenv
Create .env file:
env
Copy
Edit
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
