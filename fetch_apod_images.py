import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_utilities import get_file_extension, download_image


def get_urls_for_apod(n: int,api_key : str) -> list[str]:
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'count': n}
    response = requests.get(url, params)
    return [i['hdurl'] for i in response.json() if 'hdurl' in i]


def download_nasa_apod(folder_for_pictures: str, suffix_for_filename : int) -> None:
    ext = get_file_extension(url)
    filename = f'nasa_apod_{suffix_for_filename}{ext}'
    filepath = Path(folder_for_pictures, filename)
    download_image(url, filepath)


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Скачивает последние изображения дня')
    parser.add_argument('count', nargs='?', default=5, help='Количество картинок')
    parser.add_argument('folder', nargs='?', default='apod', help='Имя папки для сохранения')
    args = parser.parse_args()
    api_key = os.environ['API_NASA_KEY']
    os.makedirs(args.folder, exist_ok=True)
    for suffix_for_filename, url in enumerate(get_urls_for_apod(args.count,api_key)) :
        download_nasa_apod(args.folder, suffix_for_filename)
