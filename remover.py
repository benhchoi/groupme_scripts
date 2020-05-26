import collections
import requests
import secrets
from settings import *


def main():
    r = requests.get(f'{base_url}/groups/{group_id}', params={'token': token})
    to_remove = {member['user_id']: member['id']
                 for member in r.json()['response']['members']}
    members = {member['user_id']: member['name']
               for member in r.json()['response']['members']}

    r = requests.get(f'{base_url}/groups/{group_id}/messages',
                     params={'token': token, 'limit': '100'})
    for msg in r.json()['response']['messages']:
        if msg['system'] and final_msg in msg['text'].lower():
            start = msg['created_at'] - time_buffer
            end = msg['created_at']
            endpoint = msg
            break

    while endpoint['created_at'] > start:
        r = requests.get(f'{base_url}/groups/{group_id}/messages',
                         params={'token': token, 'before_id': endpoint['id'], 'limit': '100'})
        messages = r.json()['response']['messages']
        for i, msg in enumerate(messages):
            if len(msg['favorited_by']) > remove_threshold and msg['created_at'] > start:
                to_remove.pop(msg['user_id'], None)
            elif msg['created_at'] <= start:
                endpoint = msg
                break
            elif i == len(messages) - 1:
                endpoint = msg

    removed = []
    for user_id, member_id in to_remove.items():
        r = requests.request(
            'POST', f'{base_url}/groups/{group_id}/members/{member_id}/remove', params={'token': token})
        if r.status_code == 200:
            removed.append(user_id)

    if removed:
        requests.post(f'{base_url}/bots/post', data={'bot_id': bot_id,
                                                     'text': f'{", ".join([members[user_id] for user_id in removed])} you all failed to get more than 11 likes in the past month'})


if __name__ == "__main__":
    main()
