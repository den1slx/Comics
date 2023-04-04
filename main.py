import requests
import os
import vk_api
from dotenv import load_dotenv
from random import randint
import argparse
import io


def fetch_buffered_file(url, token=None):
    headers = {
        'api_key': token,
    }
    response = requests.get(url, headers)
    response.raise_for_status()
    image = io.BytesIO(response.content)
    return image


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


def upload_to_vk(vk_session, image):
    response = vk_session.method('photos.getWallUploadServer'),
    if 'error' in response:
        raise Exception(response)
    album_id, upload_url, user_id = response[0].values()
    response = requests.post(upload_url, files={"photo": ('.jpg/.png', image)})
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
        '-id',
        help='Group or user id, can be defined in env VK_GROUP_ID',
        default=None,
    )
    return parser


def main():
    load_dotenv()
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_session = vk_api.VkApi(token=vk_access_token)
    vk = vk_session.get_api()
    parser = create_parser()
    args = parser.parse_args()
    group_id = args.id
    if not group_id:
        group_id = os.getenv('VK_GROUP_ID', default=None)
    image_url, title, alt = get_img_xkcd()
    image = fetch_buffered_file(image_url)
    attachment = upload_to_vk(vk_session, image)
    vk.wall.post(owner_id=f'-{group_id}', message=alt, attachments=attachment, from_group=1)


if __name__ == '__main__':
    main()
