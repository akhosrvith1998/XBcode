from flask import Flask, request, Response
import requests
import os
import threading
from main import process_update
from reply_whisper import process_reply_whisper
from logger import logger

app = Flask(__name__)
TOKEN = "7844345303:AAGyDzl4oJjm646ePdx0YQP32ARuhWL6qHk"  # هاردکد شده
URL = f"https://api.telegram.org/bot{TOKEN}/"

@app.route("/")
def home():
    return "ربات نجوا - امن در حال اجراست!"

@app.route("/keepalive")
def keepalive():
    return "I’m alive"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        logger.info("Received update: %s", update)
        if "inline_query" in update:
            def run_process_update():
                try:
                    logger.info("Starting process_update for inline query: %s", update)
                    process_update(update)
                except Exception as e:
                    logger.error("Error in process_update: %s", str(e))
            threading.Thread(target=run_process_update).start()
        elif "message" in update and "reply_to_message" in update["message"]:
            def run_process_reply_whisper():
                try:
                    logger.info("Starting process_reply_whisper: %s", update)
                    process_reply_whisper(update)
                except Exception as e:
                    logger.error("Error in process_reply_whisper: %s", str(e))
            threading.Thread(target=run_process_reply_whisper).start()
        return Response(status=200)
    except Exception as e:
        logger.error("Webhook error: %s", str(e))
        return Response(status=500)

if __name__ == "__main__":
    webhook_url = "https://xbcode-render-app.onrender.com/webhook"  # اصلاح URL
    try:
        response = requests.get(f"{URL}setWebhook?url={webhook_url}")
        logger.info("Webhook set response: %s", response.json())
        if not response.json().get("ok"):
            logger.error("Failed to set webhook: %s", response.json())
    except Exception as e:
        logger.error("Error setting webhook: %s", str(e))
    app.run(host="0.0.0.0", port=10000)  # پورت هاردکد شده