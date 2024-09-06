import argparse
import os
import random
from pathlib import Path

import telegram
from dotenv import load_dotenv


def get_filename(filename):
    if filename:
        return filename
    images = os.listdir(args.folder)
    return random.choice(images)


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Постит одну картинку в чат')
    parser.add_argument('filename', nargs='?', default=None, help='Имя файла для отправки')
    parser.add_argument('folder', nargs='?', default='apod', help='Имя папки откуда постится фото')
    args = parser.parse_args()
    token = os.environ['BOT_API']
    chat_id = os.environ['CHAT_ID']
    bot = telegram.Bot(token=token)
    folder = Path(args.folder)
    if folder.exists():
        filename = get_filename(args.filename)
        filepath = Path(folder, filename)
        if filepath.exists():
            with open(filepath, 'rb') as f:
                bot.send_document(chat_id=chat_id, document=f)
