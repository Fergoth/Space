import os

import telegram
from dotenv import load_dotenv

load_dotenv()

token = os.environ['BOT_API']
bot = telegram.Bot(token=token)
print(bot.get_me())
#bot.send_message(text='Hi John!', chat_id="@dvmn_nasa_test")
bot.send_document(chat_id="@dvmn_nasa_test", document=open('apod/nasa_apod_0.jpg', 'rb'))