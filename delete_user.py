import os
import json


def delete_user(user_id):
    try:
        with open('list_of_users.json') as file:
            users = json.load(file)
        users.remove(user_id)
        with open('list_of_users.json', 'w') as file:
            json.dump(users, file)
            os.remove('followers/{}.json'.format(user_id))
    except (ValueError, FileNotFoundError):
        pass

