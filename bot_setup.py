import requests
from settings import *


def string_in_file(filename, string):
    with open(filename, 'r') as settings:
        data = settings.read().lower()

    return string in data


def main():
    to_create = not string_in_file('settings.py', 'bot_id')
    if not to_create:
        print('No bot created, already exists')
        return

    r = requests.request('POST', f'{base_url}/bots', params={'token': token}, headers={'Content-Type': 'application/json'},
                         data={'bot': {'name': bot_name, 'group_id': group_id}})

    if r.status_code == 201:
        with open('settings.py', 'a') as settings:
            settings.write(
                f"bot_id = '{r.json()['response']['bot']['bot_id']}'")
        print('Bot created')
    else:
        print('No bot created, there were problems with the request')


if __name__ == '__main__':
    main()
