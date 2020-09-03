import twint
import time

def get_followers_process(username):
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    twint.run.Followers(c)
    list_of_followers = twint.storage.panda.Follow_df
    return list_of_followers['followers'][username]

def get_followers(username):
    for i in range(4):
        try:
            followers = get_followers_process(username)
        except KeyError:
            continue
        if followers:
            return followers
        time.sleep(5)
    return "ERROR"

