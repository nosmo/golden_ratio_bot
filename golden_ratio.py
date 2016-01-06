#!/usr/bin/env python

'''Get a random image from imgur and apply the golden ratio to it.

This is super dumb.

'''

import json
import random
import tempfile
import os

import requests

from imgurpython import ImgurClient
import PIL.Image

MIN_HEIGHT = 810
MIN_WIDTH = 1280

MAX_GETS = 5

__author__ = "nosmo@nosmo.me"

def main():
    config = {}
    with open("config.json") as config_f:
        config = json.load(config_f)

    temp_dir = tempfile.mkdtemp()
    print temp_dir

    imgur_client = ImgurClient(config["client_id"], config["client_secret"])

    random_image_list = []
    gets = 0

    while not random_image_list and gets <= MAX_GETS:
        random_image_list = [ i for i in imgur_client.gallery_random() if not i.is_album \
                              and not i.nsfw \
                              and not i.animated \
                              and (i.width/float(i.height)) >= 1.5 \
                              and (i.width/float(i.height)) <= 1.8]
        gets += 1

    if gets > MAX_GETS:
        raise SystemExit("Failed to get image list after %d gets! :(" % MAX_GETS)

    random.shuffle(random_image_list)
    random_image = random_image_list[0]
    random_image_get = requests.get("https://imgur.com/%s.png" % random_image.id)
    random_image_content = random_image_get.content

    imgur_f_path = os.path.join(temp_dir, "imgur.png")
    with open(imgur_f_path, "w") as imgur_f:
        imgur_f.write(random_image_content)

    imgur_pil = PIL.Image.open(imgur_f_path)
    fib_pil = PIL.Image.open("1280px-Fibonacci_spiral_34.svg.png")
    fib_pil = fib_pil.resize((random_image.width, random_image.height), PIL.Image.ANTIALIAS)

    imgur_pil.paste(fib_pil, (0, 0), fib_pil)
    imgur_pil.show()

if __name__ == "__main__":
    main()
