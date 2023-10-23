# This file uses the following encoding : utf-8

from . import storage

EmojiList = storage.EmojiStorage


def get_all():
    """
    Get all emojis
    :rtype: iter
    """
    return EmojiList


def get_categories():
    """
    Get all categories
    :rtype: set
    """
    return {emoji.category for emoji in EmojiList}


def get_by_category(category):
    """
    Get all emojis from category
    :param category: string
    :rtype: iter
    """
    return filter(lambda emoji: emoji.category.lower() == category.lower(), EmojiList)