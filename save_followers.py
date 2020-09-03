import os
import json

def savind_followers(followers, username_twitter, username_telegramm):
    with open('followers/%s.json' % (username_telegramm), 'w') as file:
        json.dump({username_twitter: followers}, file)


