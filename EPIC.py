import os
import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from helper import download_image

load_dotenv()

URL = "https://api.nasa.gov/EPIC/api/natural/images"


def fetch_image_info(count, api_key):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {'api_key': api_key}
    response = requests.get(url, params)
    return response.json()[:count]


def generate_url_for_image(image):
    image_id = image['image']
    image_date = datetime.datetime.fromisoformat(image['date'])
    date = image_date.strftime("%Y/%m/%d")
    return f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image_id}.png"


def download_nasa_epic(folder, api_key, count):
    images = fetch_image_info(count, api_key)
    for i, image in enumerate(images):
        url = generate_url_for_image(image)
        filename = f"nasa_epic_{i}.png"
        filepath = Path(folder, filename)
        download_image(url, filepath, api_key)


if __name__ == '__main__':
    api_key = os.environ['API_KEY']
    folder = 'EPIC'
    os.makedirs(folder, exist_ok=True)
    download_nasa_epic(folder, api_key, count=5)
