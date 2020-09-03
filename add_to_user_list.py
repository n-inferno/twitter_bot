import json

def add_user(tg_username):
    with open('list_of_users.json') as file:
        users = json.load(file)
    if tg_username not in users:
        users.append(tg_username)
    with open('list_of_users.json', 'w') as file:
        json.dump(users, file)


