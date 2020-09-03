import json
import get_followers as fol
import time

def check_followers(username):
    file = 'followers/{}.json'.format(username)
    with open(file) as f:
        json_file = json.load(f)
        for i in json_file.keys():
            acc_name = i
        old_list = json_file[acc_name]
    new_list = fol.get_followers(acc_name)

    while new_list == "ERROR":
        time.sleep(5)
        new_list = fol.get_followers(acc_name)

    unfollow = [i for i in old_list if i not in new_list]
    new_followers = [i for i in new_list if i not in old_list]

    if unfollow or new_followers:
        with open(file, 'w') as f:
            json.dump({username: new_list}, f)
    return unfollow, new_followers

