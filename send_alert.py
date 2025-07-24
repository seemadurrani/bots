import requests

def send_telegram_alert(message):
    if not message:
        print("Telegram alert skipped: message is empty")
        return
    ## Replace it with your bot token
    url = "https://api.telegram.org/bot<Your bot token>/sendMessage"
    payload = {
        ##Replace it with your bot ID
        "chat_id": <Your chat ID>,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        if response.status_code != 200:
            print("❌ Failed to send Telegram alert.")
        else:
            print("✅ Telegram alert sent successfully.")
    except Exception as e:
        print("❌ Exception occurred while sending message:", e)

# Send test message
send_telegram_alert("Yo what's up 👋")
