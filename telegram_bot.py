import os

import telegram
from dotenv import load_dotenv

load_dotenv()

token = os.environ['BOT_API']
bot = telegram.Bot(token=token)
print(bot.get_me())
