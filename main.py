from config import *
from engine import *
from interface import *
import pygame as pg

# Initialize Game Engine
ENGINE = Engine()

# Initialize Game Windows
instance = Game()

# Run Game Loop
while instance.running:

    # Show Start Screen
    mode = instance.start_screen()

    if mode != None:
        # New Game, Pass Engine Instance
        instance.new(ENGINE, mode['lives'], mode['time'])

        # Show Game Over Screen
        instance.game_over()

pg.quit()