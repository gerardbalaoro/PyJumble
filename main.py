"""Main Script (Executable)"""

from config import *
from engine import *
from interface import *
import pygame as pg

# Initialize Game Engine
ENGINE = Engine()

# Initialize Game Interface
instance = Game()

# Run Game Loop
while instance.running:

    # Show Start Screen
    mode = instance.start_screen()

    if mode == 'i' :
        # Show Credits Screen
        instance.credits()
        continue
    elif mode == None:
        break
    else:
        # New Game, Pass Engine Instance
        instance.new(ENGINE, mode)

        # Show Game Over Screen
        instance.game_over()

pg.quit()