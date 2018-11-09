<h1 align="center">PyJumble: Powered by PyGame</h1>
<p align="center">
    A Python Based Word Unscramble Game<br>
    Developed by <b>Gerard Ian M. Balaoro</b>
</p>
<p align="center">
    <img src="00-title.png">
</p>
<hr>




<h1 align="center">Documentation</h1>



## Overview

The execution process of application is contained in **main.py**.

1. External modules and the **[PyGame](https://www.pygame.org)** package are imported first.

   ```python
   from config import *
   from engine import *
   from interface import *
   import pygame as pg
   ```

2. The **[Game](#game-class)** and **[Engine](#engine-class)** classes are initialized and the game interface is shown.

   ```python
   # Initialize Game Engine
   ENGINE = Engine()
   
   # Initialize Game Interface
   instance = Game()
   ```

3. At this point, the property `running` of the [Game class](#game-class) is set to `True`. While that is, show the user interface and run the game.

   ```python
   while instance.running:
       # Show Start Screen
       mode = instance.start_screen()
       # If the user pressed 'i'
       if mode == 'i' :
           # Show Credits Screen
           instance.credits()
           continue
       # If the user clicked the close button
       elif mode == None:
           break
       # If the user selected a valid game mode
       else:
           # New Game, Pass Engine Instance, and mode configuration
           # This will run until the game is over or escaped
           instance.new(ENGINE, mode)
           # Show Game Over Screen
           instance.game_over()
   ```

4. Quit PyGame and destroy the window at the end.

   ```python
   pg.quit()
   ```

 

### File Structure

The source files of the application are arranged according to the diagram below.

```
.
├── ...
├── assets # Application Assets
│ ├── audio # Sounds / Music Files (*.wav)
│ ├── fonts # Font Files (*.ttf)
│ ├── images # Images (*.png)
│ └── source # Dictionary Files (.*txt)
├── config.json # User Configuration
├── config.py # Application Configuration
├── engine.py # Game Logic Engine Class
├── interface.py # PyGame Interface Class and Methods
├── main.py # Main / Entry Script
├── setup.py # Distutils Setup Script
├── sprites.py # Sprites / Game Object Classes
└── ...
```



## Interface

The application interface powered by the **[PyGame Library](https://www.pygame.org)**  are composed of two parts: the **[Game](#game-class)** and **[Sprite](#sprites)** classes.



### Game Class

The **Game** class is located at the **interface.py** file and serves as the primary provider and manager of the application's interface.

```python
game = Game()
```

When called, the class uses the values stored at the **[configuration](#configuration)** to initialize the game window and the resources required by each of its components.

#### load

```python
game.load()
```

Load Resources

Returns: **`None`**

#### new

```python
game.new(engine, mode)
```

Start a New Game

> From the engine instance passed, this method automatically retrieves 3 words from the dictionary using the `random.sample()` function and creates a new letter pool.
>
> It also sets the global variables `lives` and `time`.

* Arguments:
  * **engine** `Engine`: an instance of **[game engine](#engine-class)**
  * **mode** `dict` : Game mode, as defined in **[configuration](#game-modes)**
* Returns:  **`None`**

#### run

```python
game.new()
```

Run the Game Proper

> The play screen is shown and a global variable `playing` is set to `True`. While is it, a loop that updates the screen elements such as the tiles and the other controls is executed until the `lives` or `timer` has reached zero, or the user ends the game by closing window or pressing the escape key.

- Returns:  **`None`**

#### update

```python
game.update()
```

Refresh Game Window

- Returns:  **`None`**

#### events

```python
game.events()
```

Handles Game Events _[ i.e. user input and key press ]_

- Returns:  **`None`**

#### draw

```python
game.draw()
```

Draw Game Elements

- Returns: **`None`**

#### start_screen

```python
game.start_screen()
```

Show Start Screen

- Returns:
  - **`dict`**: Game mode, as defined in **[configuration](#game-modes)**
  - **`str`**: Only if `'i'` is selected, which shows the credits screen

#### credits

```python
game.credits()
```

Show Credits Screen

- Returns: **`None`**

#### game_over

```python
game.game_over()
```

Show Game Over Screen

- Returns: **`None`**

#### wait_input

```python
game.wait_input()
```

Wait for User Input

>  Used for Static Screens (Start Menu, Game Over, etc.)

* Arguments:
  * **accepted** `list`:  List of accepted keys
* Returns:
  * **`str`**:  Key name, none



### Sprites

The **sprites.py** contains `pygame.sprite.Sprite` classes that are used throughout the interface

#### Letter

```python
Letter(letter [, position = 1, length = 1, size = 80, margin = 55, button = False])
```

Produces a single letter tile

#### Image

```python
Image(name [, scale = 1, x = 0, y = 0])
```

Produces an image block

#### Text

```python
Text(text, size, color [, x = 0, y = 0, font = 'GothamNarrow-Medium.ttf'])
```

Produces a text block

> Adapted from the [work of Gareth Rees](https://codereview.stackexchange.com/questions/31642/text-class-for-pygame)
>
> Copyright (c) 2013. Under CC-BY-SA 3.0 License

#### Button

```python
Button(text, x, y [, size = 15, scale = 0.50, color = None, image = 'button.png', font = 'GothamNarrow-Medium.ttf', text_offset = (-1,-1)])
```

Produces a button



### Media

All media used on the **[Game](#game-class)** class are loaded through the `__init__()` and `load` functions. Sources are declared at the **[configuration](#configuration)**.



## Engine Class

The `Engine` class defined at the **engine.py** contains the core program logic of the application.

```python
engine = Engine([, path = ''])
```

* Arguments:
  * **path** `str`: Optional path to dictionary file

When called, the class automatically loads the default dictionary file from **config.py** if no path is passed.

### seed

```python
engine.seed(path)
```

Read Dictionary Text File

> The file contents are assigned to the global variable `dictionary` accessible in-class using `self.dictionary` and outside the class using `engine.dictionary`

* Arguments:
  * **path** `str`: Path to dictionary file
* Returns: **`None`**

### pick

```python
engine.pick([, number = 3, indices = []])
```

Get List of Words from Dictionary

> This method implements the method `random.sample()` to select words form the global `dictionary` and defines a global variable `picked` containing the selected words

- Arguments:
  - **number** `int`: Number of words to pick
  - **indices** `list`: List of indices
- Returns: 
  - **`list`**: List of words

### search

```python
engine.search([, source = ''])
```

Find Anagrams from Dictionary

> If no source is provider, the global variable `pool` will be used. This method also sets a global variable `matchable` containing the anagrams found.
>
> Note that if `source` was passed, the `matchable` variable will not be defined or updated.

- Arguments:
  - **source** `str|list`: Characters to use
- Returns: 
  - **`list`**: List of words

### combine

```python
engine.combine([, number = 3, words = []])
```

Create a Scrambled Character Pool

> Automatically calls `pick()` method, unless the variable `words` was passed. The pool characters are then assigned to a global variable `pool`.
>
> If the variable `words` was passed, the global `pool` will not be defined or updated.

- Arguments:
  - **number** `int`: Number of words, passed on to `pick()` method
  - **words** `list`
- Returns: 
  - **`list`**: List of letters

### check

```python
engine.check(word, [, pool = []])
```

Check if `word` can be formed using the characters from `pool` and exists in the global variable `dictionary`

> If `pool` was not passed, the method uses the global variable `pool`

- Arguments:
  - **word** `str`
  - **pool** `list`
- Returns: **`bool`**

### score

```python
engine.score(word)
```

Calculates the Score of a Word using Scrabble Points

- Arguments:
  - **word** `str`
- Returns: **`int`**



## Configuration

All constants and other objects that are used throughout the application are defined at the **config.py**. This file is imported in all of the scripts that constitute the program.

### User Settings

The **config.json**, if exists, overrides some values defined in **config.py**.

```json
{
    "dictionary" : "assets/source/dictionary.txt",
    "strict"     : true
}
```

At the beginning of **config.py**, the module attempts to load **config.json** values.

```python
#: ====================================
#: LOAD CONFIG.JSON VALUES
#: ====================================
if os.path.exists('config.json'):
    user = json.loads(open('config.json', 'r').read())
else:
    user = {}
```

### Interface Settings

```python
#: ====================================
#: INTERFACE
#: ====================================
TITLE = 'PyJumble'                             # Window Title
WIDTH = 900                                    # Window Width
HEIGHT = 600                                   # Window Height
FPS = 60                                       # Window Refresh Rate
BACKGROUND = 'assets/images/background.png'    # Background Image
ICON = 'assets/images/icon.png'                # Window Icon
```

### Default Values

```python
#: ==============================================
#: DEFAULTS
#: ==============================================
DICTIONARY = user.get('dictionary', 'assets/source/dictionary.txt')
#: Used in Game Modes
LIVES = 3
TIME = 60
SCRAMBLED_WORDS = 3
INSTRUCTIONS = 'CREATE WORDS USING THE LETTERS PROVIDED ABOVE'
```

### Game Modes

```python
#: ====================================
#: GAME MODES
#: ------------------------------------
#: lives/time: 0 = Infinite
#: key: Selection Key on Start Screen
#: exact_match: Entries must use all the letters from the anagram
#: scrambled_words: Number of words from the dictionary to scramble
#: instructions: Instructions
#: ====================================
MODES = [
    {
        'name': 'BASIC',
        'key': 'b',
        'lives': 3,
        'time': 0,
        'exact_match': False,
        'scrambled_words': SCRAMBLED_WORDS,
        'instructions': INSTRUCTIONS
    }
]
```

### Audio Files

```python
#: ====================================
#: AUDIO FILES
#: ====================================
AUDIO = {
    'enter': 'assets/audio/swap.wav',        # Enter/Backspace/Esc Key Press
    'click': 'assets/audio/swap.wav',	     # Alpha Key Press
    'success': 'assets/audio/match.wav',     # Correct Answer
    'fail': 'assets/audio/error.wav',        # Wrong Answer
    'start': 'assets/audio/start.wav',       # Start of a New Game
    'end': 'assets/audio/over.wav',          # End of Game
    'menu': 'assets/audio/yippee.wav',       # Background Music on Start Screen
    'game': 'assets/audio/happytune.wav',    # Background Music on Game Screen
}
```

### Miscellaneous

```python
#: ====================================
#: STRICT MODE
#: ------------------------------------
#: Deduct points on duplicate entries
#: ====================================
STRICT = user.get('strict', True)
```



## Running the Game

This application requires the **[PyGame](https://www.pygame.org)** package. Install it by using **pip** by running the command:
```
pip install pygame
```
> See their [documentation](https://www.pygame.org/wiki/GettingStarted) for information on installing the package without **pip**.

Run the main script.
```
python main.py
```
> **Note**: This version of the program has only been tested in Python 3.4 to 3.7



## Building Distributables

The **[cx_Freeze](https://anthony-tuininga.github.io/cx_Freeze/)** package is used to compile executable binaries and create installers.
Currently, only Windows distributables are supported. The package uses Python 3.6 binaries during build, as such **Python 3.6 is required**. Problems were encountered during install or build when using other Python versions.

The build configuration is defined in **setup.py**. For more information, read **[cx_Freeze documentation](https://cx-freeze.readthedocs.io/en/latest/distutils.html)**.

Install **[cx_Freeze](https://anthony-tuininga.github.io/cx_Freeze/)** using **pip** by running the command:
```
py -3.6 -m pip install cx_Freeze
```

Build Windows Binaries (32-bit)
```
py -3.6 setup.py build
```

Build Windows Installer (MSI)
```
py -3.6 setup.py bdist_msi
```





<h1 align="center">Credits</h1>

* Interface Based on Graphic by **[Vecteezy](https://www.vecteezy.com)**
* [YIPPEE by **Snabisch**](https://opengameart.org/content/yippee)
* [Happy Tune by **syncopica**](https://opengameart.org/content/happy-tune)
* Other Sounds are Generated using **[Diforb](http://diforb.com)**
* Hearts Icon by **[Smashicons](https://smashicons.com/)** from www.flaticon.com
* Three quarters of an hour Icon by **[Freepik](http://www.freepik.com/)** from www.flaticon.com
* The Code Structure as Based on Jumpy Platformer by **[KidsCanCode](http://kidscancode.org/)**
