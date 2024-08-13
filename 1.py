import requests
import os
from pathlib import Path

from helper import download_image, get_file_extension


def get_links() -> list[str]:
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


def fetch_spacex_last_launch_with_pictures(folder_for_pictures):
    for i, url in enumerate(get_links()):
        ext = get_file_extension(url)
        filename = f"spacex_{i}{ext}"
        filepath = Path(folder_for_pictures, filename)
        download_image(url, filepath)


if __name__ == "__main__":
    folder = 'images'
    os.makedirs(folder, exist_ok=True)
    fetch_spacex_last_launch_with_pictures(folder)
