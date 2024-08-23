import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from download_utilities import get_file_extension


def download_image(image_url: str, path: Path) -> None:
    response = requests.get(image_url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)


def get_urls_for_apod(n: int) -> list[str]:
    api_key = os.environ['API_NASA_KEY']
    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'count': n}
    response = requests.get(url, params)
    return [i['hdurl'] for i in response.json() if 'hdurl' in i]


def download_nasa_apod(folder_for_pictures: str, i : int) -> None:
    ext = get_file_extension(url)
    filename = f'nasa_apod_{i}{ext}'
    filepath = Path(folder_for_pictures, filename)
    download_image(url, filepath)


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Скачивает последние изображения дня')
    parser.add_argument('count', nargs='?', default=5, help='Количество картинок')
    parser.add_argument('folder', nargs='?', default='apod', help='Имя папки для сохранения')
    args = parser.parse_args()
    os.makedirs(args.folder, exist_ok=True)
    for i, url in enumerate(get_urls_for_apod(args.count)) :
        download_nasa_apod(args.folder, i)
