from pathlib import Path, PurePath
import requests
from urllib.parse import urlsplit, unquote
import os
import vk_api
from dotenv import load_dotenv
from random import randint
import argparse


def create_directory(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def fetch_file(path, url, name, extension='', token=None):
    headers = {
        'api_key': token,
    }
    response = requests.get(url, headers)
    response.raise_for_status()
    fullpath = PurePath(path).joinpath(f'{name}{extension}')
    with open(fullpath, 'wb') as picture:
        picture.write(response.content)


def get_name_and_extension_file(url, is_tuple=True, name_only=False, extension_only=False):
    url_split = urlsplit(url)
    path = url_split.path
    path = unquote(path)
    head, tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    if name_only:
        return name
    if extension_only:
        return extension
    if is_tuple:
        return name, extension
    else:
        return f'{name}{extension}'


def get_img_xkcd():
    url = f'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_num = response.json()['num']
    num = randint(0, last_num)
    url = f'https://xkcd.com/{num}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    return response["img"], response['title'], response['alt']


def upload_to_vk(vk_session, image_name, image_data):
    response = vk_session.method('photos.getWallUploadServer'),
    if 'error' in response:
        raise Exception(response.text)
    album_id, upload_url, user_id = response[0].values()
    response = requests.post(upload_url, files={"photo": (image_name, image_data)})
    response.raise_for_status()
    server, photo, hash_ = response.json().values()
    photos = vk_session.method(
        "photos.saveWallPhoto",
        {"photo": photo, "server": server, "hash": hash_}
    )
    id_ = photos[0]['id']
    owner_id = photos[0]['owner_id']
    return f"photo{owner_id}_{id_}"


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-path',
        help='Path to save image, can be defined in env PATH_TO_SAVE_IMAGES',
        default=os.getenv('PATH_TO_SAVE_IMAGES', default=None),
    )
    parser.add_argument(
        '-id',
        help='Group or user id, can be defined in env VK_GROUP_ID',
        default=os.getenv('VK_GROUP_ID', default=None),
    )
    return parser


def main():
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_session = vk_api.VkApi(token=vk_access_token)
    vk = vk_session.get_api()
    parser = create_parser()
    args = parser.parse_args()
    group_id = args.id
    path_to_images = args.path
    img, title, alt = get_img_xkcd()
    default_name, default_extension = get_name_and_extension_file(img)
    path = create_directory(path_to_images)
    fetch_file(path, img, default_name, default_extension)
    img_name = f'{default_name}{default_extension}'
    fullpath = PurePath(path).joinpath(img_name)
    with open(fullpath, 'rb') as file:
        img_data = file.read()

    attachment = upload_to_vk(vk_session, img_name, img_data)
    vk.wall.post(owner_id=group_id, message=alt, attachments=attachment)
    os.remove(fullpath)


if __name__ == '__main__':
    main()
