import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from helper import get_file_extension

load_dotenv()


def download_image(image_url: str, path: Path) -> None:
    response = requests.get(image_url)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)


def get_urls_for_apod(n: int):
    api_key = os.environ['API_KEY']
    url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': api_key, 'count': n}
    response = requests.get(url, params)
    return [i['hdurl'] for i in response.json() if 'hdurl' in i]


def download_nasa_apod(folder_for_pictures, count):
    urls = get_urls_for_apod(count)
    for i, url in enumerate(urls):
        ext = get_file_extension(url)
        filename = f"nasa_apod_{i}{ext}"
        filepath = Path(folder_for_pictures, filename)
        download_image(url, filepath)


if __name__ == '__main__':
    folder = 'nasa_apod'
    os.makedirs(folder, exist_ok=True)
    download_nasa_apod(folder, 5)
