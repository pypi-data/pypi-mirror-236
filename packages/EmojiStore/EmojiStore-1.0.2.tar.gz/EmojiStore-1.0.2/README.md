# EmojiStore
Free unicode emojis ready to use !
This package contains a total of 1851 emojis grouped in 8 categories.

# Installation
Install with pip

`pip install EmojiStore`

or

`pip3 install EmojiStore`

# Usage
It all starts by importing the package

```python
import EmojiStore
```
### Get all emojis
You can get all available emojis by calling the `get_all()` method.

```python
emojis = EmojiStore.get_all()
```

Notice that every time you are retrieving emojis, you get an iterator of **namedtuple** elements (emojis).
Each emoji have the following properties : 
- **category** : The category from which belongs the emoji
- **emoji** : The emoji character
- **alias** : The emoji short code
- **description** : The emoji description
- **unicode** : A list of Unicode composing the emoji

```commandline
>>> ...
>>> first_emoji = emojis[0]
>>> print(first_emoji.category)
smileys_and_people

>>> print(first_emoji.emoji)
😀

>>> print(first_emoji.alias)
grinning_face

>>> print(first_emoji.description)
grinning face

>>> print(first_emoji.unicode)
['U+1F600']
```

### Get emoji categories
You can get all available categories by calling the `get_categories()` method. 
This method returns a set of all categories :
- smileys_and_people
- animals_and_nature
- food_and_drink
- travel_and_places
- activities
- objects
- symbols
- flags

```python
categories = EmojiStore.get_categories()
print(categories)
```

Output :
```
{'animals_and_nature', 'food_and_drink', 'symbols', 'flags', 'travel_and_places', 'smileys_and_people', 'objects', 'activities'}
```

### Get all emojis from a specific category

```python
import EmojiStore

smileys = EmojiStore.get_by_category("smileys_and_people")
```

# Credits
All the emojis in this package where generated from https://www.webfx.com/tools/emoji-cheat-sheet