import argparse
import os
from random import shuffle
from time import sleep

import telegram

from dotenv import load_dotenv


def get_all_files_in_folder(folder):
    return list(os.walk(folder))[0]


if __name__ == '__main__':
    load_dotenv()
    max_picture_size = 20 * 1024 * 1024
    freq = int(os.environ['POST_FREQ'])
    chat_id = os.environ['CHAT_ID']
    parser = argparse.ArgumentParser(
        description='Скрипт для публикации фотографий')
    parser.add_argument('freq', nargs='?', type=int, default=freq, help='частота публикации')
    parser.add_argument('folder', nargs='?', default='space_x', help='Имя папки для сохранения')
    args = parser.parse_args()
    token = os.environ['BOT_API']
    bot = telegram.Bot(token=token)
    root, _, filenames = get_all_files_in_folder(args.folder)
    while True:
        for name in filenames:
            filepath = os.path.join(root, name)
            if os.path.getsize(filepath) > max_picture_size:
                continue
            with open(filepath, 'rb') as f:
                bot.send_document(chat_id=chat_id, document=f)
            sleep(args.freq)
        shuffle(filenames)
