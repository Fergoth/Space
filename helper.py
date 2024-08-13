from os.path import splitext, split
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests


def download_image(image_url: str, path: Path, api_key=None) -> None:
    if api_key:
        params = {'api_key': api_key}
    else:
        params = {}
    response = requests.get(image_url, params)
    response.raise_for_status()
    with open(path, 'wb') as f:
        f.write(response.content)


def get_file_extension(url: str) -> str:
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    clear_url_path = unquote(url_path)
    _, filename = split(clear_url_path)
    _, ext = splitext(filename)
    return ext
