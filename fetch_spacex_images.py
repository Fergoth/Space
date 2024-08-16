import requests
import os
from pathlib import Path
import argparse

from download_utilities import download_image, get_file_extension


def get_links_last_launch_with_pictures() -> list[str]:
    url = 'https://api.spacexdata.com/v5/launches/query'
    data = {
        "query": {
            "links.flickr.original": {"$ne": []},
            "upcoming": "false"

        },
        "options": {
            "limit": 1,
            "select": "links.flickr.original",
            "sort": {
                "flight_number": "asc"
            }}
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()['docs'][0]['links']['flickr']['original']


def get_links_by_id(launch_id):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def fetch_spacex_launch(folder_for_pictures, launch_id):
    if launch_id:
        picture_urls = get_links_by_id(launch_id)
    else:
        picture_urls = get_links_last_launch_with_pictures()

    for i, url in enumerate(picture_urls):
        ext = get_file_extension(url)
        filename = f"spacex_{i}{ext}"
        filepath = Path(folder_for_pictures, filename)
        download_image(url, filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Скачивает последний запуск spacex c картинками, если передать id '
                    'скачивает картинку по id')
    parser.add_argument('id', nargs='?', default=None, help='id картинки')
    parser.add_argument('folder', nargs='?', default='space_x', help='Имя папки для сохранения')
    args = parser.parse_args()
    os.makedirs(args.folder, exist_ok=True)
    fetch_spacex_launch(args.folder, args.id)
