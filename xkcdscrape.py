import requests
import shutil
import os
import os.path
from os.path import isdir
import json
import sys
from tqdm import tqdm

def getxkcd(n=1):
    """
    A generator to get xkcds until there are none left (starting at 1)
    Returns a dictionary of metadata like http://xkcd.com/614/info.0.json.

    Example:
    {u'img': u'http://imgs.xkcd.com/comics/kayak.png', u'title': u'Kayak', u'month': u'1', u'num': 209, u'link': u'', u'year': u'2007', u'news': u'', u'safe_title': u'Kayak', u'transcript': u"[[Person with beret in a kayak is talking to person on pier.]]\nPerson with beret: Come explore the future with me!\nPerson on pier: Huh? What's that you're in?\nPerson with beret: A two seat kayak!\nPerson on pier: I see, but why do you have it?\nPerson with beret: We'll find out! The future is a big place!\nPerson on pier: So the kayak travels through time?\nPerson with beret: Sure! Just like everything else! It also goes over water. Come on!\n{{title text: Man, there's future *everywhere*.}}", u'alt': u"Man, there's future *everywhere*.", u'day': u'12'}
    """
    i = n
    while True:
        # xkcd doesn't have a comic 404
        if i == 404 or isdir(str(i)):
            i += 1
            continue
        response = requests.get('http://xkcd.com/{}/info.0.json'.format(i))
        if response.status_code != 200:
            break
        else:
            yield response.json()
        i += 1


def main():
    n = 1 if len(sys.argv) < 2 else int(sys.argv[1])
    dirname = os.path.dirname(os.path.abspath(__file__))
    for xkcd in tqdm(getxkcd(n)):
        url = xkcd['img'].replace('\\', '')
        comic_path = os.path.join(dirname, str(xkcd['num']))
        comic_filename = url.split('/')[-1]
        if not os.path.exists(comic_path):
            os.mkdir(comic_path)
        response = requests.get(url, stream=True)
        with open(os.path.join(comic_path, comic_filename), 'wb') as comic_file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, comic_file)
        with open(os.path.join(comic_path, 'metadata.json'), 'w') as metadata_file:
            json.dump(xkcd, metadata_file)


if __name__ == '__main__':
    main()
