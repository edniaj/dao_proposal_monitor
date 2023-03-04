import os
from telegram import Bot as tgBot
from dotenv import load_dotenv

load_dotenv()


class TelegramBot(tgBot):

    def __init__(self):

        super().__init__(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        self.chat_id = os.getenv('TELEGRAM_BOT_TOKEN')

    def send_message(self, _message):
        super().sendMessage(self.chat_id, _message)


