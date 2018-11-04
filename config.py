"""Application Configuration"""

import json, os.path

#: ====================================
#: LOAD CONFIG.JSON VALUES
#: ====================================
if os.path.exists('config.json'):
    user = json.loads(open('config.json', 'r').read())
else:
    user = {}

#: ====================================
#: INTERFACE
#: ====================================
TITLE = 'PyJumble'
WIDTH = 900
HEIGHT = 600
FPS = 100
BACKGROUND = 'assets/images/background.png'
ICON = 'assets/images/icon.png'

#: ==============================================
#: DEFAULTS
#: ==============================================
DICTIONARY = user.get('dictionary', 'assets/source/dictionary.txt')
LIVES = 3
TIME = 60
SCRAMBLED_WORDS = 3
INSTRUCTIONS = 'CREATE WORDS USING THE LETTERS PROVIDED ABOVE'

#: ==============================================
#: STRICT MODE
#: ----------------------------------------------
#: (Bool) Deduct points on duplicate entries
#: ==============================================
STRICT = user.get('strict', True)

#: ==============================================
#: GAME MODES
#: ----------------------------------------------
#: lives/time: 0 = Infinite
#: key: Selection Key on Start Screen
#: exact_match: Entries must use all the letters from the anagram
#: scrambled_words: Number of words from the dictionary to scramble
#: instructions: Instructions
#: ==============================================
MODES = [
    {
        'name': 'CASUAL',
        'key': 'c',
        'lives': LIVES,
        'time': 0,
        'exact_match': False,
        'scrambled_words': SCRAMBLED_WORDS,
        'instructions': INSTRUCTIONS
    },
    {
        'name': 'TIMED',
        'key': 't',
        'lives': 0,
        'time': TIME,
        'exact_match': False,
        'scrambled_words': SCRAMBLED_WORDS,
        'instructions': INSTRUCTIONS
    },
    {
        'name': 'HYPER',
        'key': 'h',
        'lives': LIVES,
        'time': TIME,
        'exact_match': False,
        'scrambled_words': SCRAMBLED_WORDS,
        'instructions': INSTRUCTIONS
    },
    {
        'name': 'ANAGRAM FINDER',
        'key': 'a',
        'lives': LIVES,
        'time': 0,
        'exact_match': True,
        'scrambled_words': 1,
        'instructions': 'FIND WORDS THAT USES THE EXACT LETTERS ABOVE'
    }
]

#: ==============================================
#: AUDIO FILES
#: ==============================================
AUDIO = {
    'enter': 'assets/audio/swap.wav',
    'click': 'assets/audio/swap.wav',
    'success': 'assets/audio/match.wav',
    'fail': 'assets/audio/error.wav',
    'start': 'assets/audio/start.wav',
    'end': 'assets/audio/over.wav',
    'menu': 'assets/audio/yippee.wav',
    'game': 'assets/audio/happytune.wav',
}

#: ==============================================
#: CREDITS
#: ==============================================
CREDITS = [
    "Copyright (c) 2018 Gerard Balaoro",
    "This Work is under the MIT License",
    "",
    "Some of the components used are from third party sources:",
    "Interface Based on Graphic by Vecteezy (https://www.vecteezy.com)",
    "YIPPEE by Snabisch (https://opengameart.org/content/yippee)",
    "Happy Tune by syncopica (https://opengameart.org/content/happy-tune)",
    "Other Sounds are Generated using Diforb (http://diforb.com)",
    "Hearts Icon by Smashicons (https://smashicons.com/) from www.flaticon.com",
    "Three quarters of an hour Icon by Freepik (http://www.freepik.com/) from www.flaticon.com",
    "",
    "Game Structure Based on https://github.com/kidscancode/pygame_tutorials",
]

class COLOR:
    """Default Application Colors"""
    RED = (244, 67, 54)
    PURPLE = (156, 39, 176)
    BLUE = (33, 150, 243)
    GREEN = (76, 175, 80)
    YELLOW = (255, 235, 59)
    ORANGE = (255, 87, 34)
    DARK = (19, 20, 24)
    LIGHT = (236, 240, 241)
    BLUEGRAY = (52, 73, 94)
    WHITE = (100, 100, 100)
    BROWN = (89, 72, 56)
    CREAM = (242, 238, 202)