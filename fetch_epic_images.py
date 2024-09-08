import argparse
import os
import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_utilities import download_image


def fetch_images(count, key):
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': key}
    response = requests.get(url, params)
    response.raise_for_status()
    decoded_response = response.json()
    if 'error' in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response['error'])
    return response.json()[:count]


def generate_url_for_image(image):
    image_id = image['image']
    image_date = datetime.datetime.fromisoformat(image['date'])
    date = image_date.strftime('%Y/%m/%d')
    return f'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image_id}.png'


def download_nasa_epic(folder, suffix_for_filename, image):
    url = generate_url_for_image(image)
    filename = f'nasa_epic_{suffix_for_filename}.png'
    filepath = Path(folder, filename)
    download_image(url, filepath, api_key)


if __name__ == '__main__':
    load_dotenv()
    api_key = os.environ['API_NASA_KEY']
    parser = argparse.ArgumentParser(
        description='Скачивает последние count Изображений Земли')
    parser.add_argument('count', nargs='?', type=int, default=5, help='Количество картинок')
    parser.add_argument('folder', nargs='?', default='epic', help='Имя папки для сохранения')
    args = parser.parse_args()
    os.makedirs(args.folder, exist_ok=True)
    try:
        images = fetch_images(args.count, api_key)
        for suffix_for_filename, image in enumerate(images):
            download_nasa_epic(args.folder, suffix_for_filename, image)
    except requests.HTTPError as error:
        print("Некорректный ответ от сервера",error)