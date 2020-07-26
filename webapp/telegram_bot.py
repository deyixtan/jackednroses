import json
import requests


class Telegram():

    enable_webhook_endpoint = "https://api.telegram.org/bot{}/setWebhook?url={}"
    disable_webhook_endpoint = "https://api.telegram.org/bot{}/deleteWebhook"
    send_message_endpoint = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"

    def init_app(self, app):
        self.bot_token = app.config["TELEGRAM_BOT_TOKEN"]

    def enable_webhook(self, url):
        endpoint = self.enable_webhook_endpoint.format(self.bot_token, url)
        response = requests.get(endpoint).json()
        if response["description"] == "Webhook was set":
            return True
        return False

    def disable_webhook(self):
        endpoint = self.disable_webhook_endpoint.format(self.bot_token)
        response = requests.get(endpoint).json()
        if response["description"] == "Webhook was deleted":
            return True
        return False

    def send_message(self, chat_id, message):
        endpoint = self.send_message_endpoint.format(self.bot_token, chat_id, message)
        response = requests.get(endpoint).json()
        return response

    def parse_update(self, json_data):
        message = json.loads(json_data.decode("utf-8"))["message"]
        return message
