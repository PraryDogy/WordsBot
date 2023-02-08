from time import sleep

import clipboard
import sqlalchemy

import bot_config
from database import Dbase, Users, Words
import os
import json


def parse_urls():

    if not os.path.exists("_urls.txt"):
        with open('_urls.txt', 'w') as file:
            pass

    paste = '1'
    counter = 0

    while 'dfvdfbvdfbdf' not in paste:
        new_paste = clipboard.paste()

        if new_paste != paste:

            paste = new_paste

            with open('_urls.txt', 'a') as file:

                file.write(new_paste + '\n')

                counter += 1
                print(counter)
                print('write url')
        
        sleep(0.1)


def google_links():

    name = "_links"

    if not os.path.exists(name):
        with open(name, "w") as ff:
            pass

    with open(name, "r") as file:
        data = file.read().split("\n")

    news = []

    for i in data:
        lnk = i.split('/')[-2]
        link_add = "https://drive.google.com/uc?id="
        new_link = link_add + lnk

        news.append(new_link)

    with open(name, "w") as f:
        f.write(json.dumps(news, indent=4))



# with open("ducks.json", "r") as file:
#     g_ducks = json.loads(file.read())

# with open("dicts/ducks_url.json", "r") as file:
#     ducks_url: dict = json.loads(file.read())


# new = {}
# for k, v in zip(g_ducks, ducks_url.values()):
#     new[k] = v

# with open("ducks_google.json", "w") as file:
#     file.write(json.dumps(new, indent=4))