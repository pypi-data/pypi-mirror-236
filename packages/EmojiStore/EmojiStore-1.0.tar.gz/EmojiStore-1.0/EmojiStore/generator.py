# This file uses the following encoding : utf-8

import os
import requests
import binascii
from bs4 import BeautifulSoup
from datetime import datetime

EMOJI_URL = "https://www.webfx.com/tools/emoji-cheat-sheet/"

# The following categories are based on webfx categories
# Modifying them can cause this script bugs

CATEGORIES = [
    "smileys_and_people",
    "animals_and_nature",
    "food_and_drink",
    "travel_and_places",
    "activities",
    "objects",
    "symbols",
    "flags"
]

BANNER = f"""
# This file uses the following encoding : utf-8
# This file was generated automatically, don't edit it.
# Last generated on {datetime.strftime(datetime.now(), "%Y-%m-%d @ %H:%M:%S")} 
# All included emojis where extracted from https://www.webfx.com/tools/emoji-cheat-sheet

from collections import namedtuple

Emoji = namedtuple("Emoji", ["category", "emoji", "alias", "description", "unicode"])

EmojiStorage = [
"""


def iconify(emoji_alias: str, data_uri: str):
    """
    Save emoji icon file from data_uri

    :param emoji_alias : Emoji alias
    :param data_uri : Data URI scheme containing the emoji image
    """

    extension = data_uri.partition("data:image/")[2].split(";")[0]
    path = os.path.join("emojicons", f"{emoji_alias}.{extension}")

    ascii_data = data_uri.partition("base64,")[2]

    with open(path, "wb") as file:
        file.write(binascii.a2b_base64(ascii_data))


def generate_from(html):
    """
    Generate python file containing all Emoji List

    :param html : the html file from which to extract emojis
    """

    soup = BeautifulSoup(html, "html.parser")
    count = 0

    with open("storage.py", "w") as file:
        file.write(BANNER)

        for i, category in enumerate(CATEGORIES):
            container: BeautifulSoup = soup.select_one(f"div#{category}")
            items = container.select("div._item")

            for j, item in enumerate(items):
                count += 1

                description = item.get("data-alt-name")
                apple_emoji = item.select_one("div.apple.emojicon")
                img = apple_emoji.select_one("img")

                # If apple emoji icon is not present, use google emoji icon
                try:
                    emoji = img.get("alt")
                except AttributeError:
                    google_emoji = item.select_one("div.google.emojicon")
                    img = google_emoji.select_one("img")
                    emoji = img.get("alt")
                finally:
                    emojicon_data_uri = img.get("src")

                alias = item.select_one("div.shortcode").text[1:-1]
                unicode = item.select_one("div.unicode").text.split(" ")

                file.write(f"\tEmoji('{category}', '{emoji}', '{alias}', '{description}', {unicode}),\n")

                # Save emoji icon in file
                iconify(alias, emojicon_data_uri)

            file.write(f"\n\t## » {j+1} Emojis found in {category} category « ##\n\n")

        file.write("]")
        file.write(f"\n## » Total of {count} Emojis found in all categories « ##\n")


if __name__ == "__main__":
    try:
        response = requests.get(EMOJI_URL)
        html = response.text
    except requests.RequestException as e:
        print(f"Request error : {e}")
    else:
        generate_from(html)
