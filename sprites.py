"""Collection of Sprite Classes"""

import pygame as pg, math
from config import *


class Letter(pg.sprite.Sprite):
    """Character Tile Sprite"""
    def __init__(self, letter, position = 1, length = 1, size = 80, margin = 55, button = False):
        pg.sprite.Sprite.__init__(self)

        line = math.ceil(position / 8)
        line_total = math.ceil(length / 8)
        line_position = list(range(line*8-7,line*8+1)).index(position)
        line_length = line_length = 8-((8*line)-length)
        if line_length > 8:
            line_length = 8

        size = round(WIDTH * 0.10)
        if line_total > 2:
            for i in range(line_total):
                size = round(size * (0.90))      

        self.letter = letter
        self.button = button
        self.image = pg.image.load("assets/images/letter_" + letter + ".png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = margin + (size * (line - 1))      
        self.rect.x = ((WIDTH / 2) - (size * line_length / 2)) + (line_position * size)
        self.size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (size, size))    

class Image(pg.sprite.Sprite):
    """Image Sprite"""
    def __init__(self, name, scale = 1, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("assets/images/" + name).convert_alpha()
        self.image.set_alpha(128)        
        self.size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)


class Text(pg.sprite.Sprite):
    """Text Block Sprite

    Adapted from the work of Gareth Rees
    Copyright (c) 2013
    Under CC-BY-SA 3.0 License

    https://codereview.stackexchange.com/questions/31642/text-class-for-pygame
    """
    def __init__(self, text, size, color, x = 0, y = 0, font = 'GothamNarrow-Medium.ttf'):
        super(Text, self).__init__()
        self.color = color
        self.font = pg.font.Font('assets/fonts/' + font, size)     
        self.image = self.font.render(str(text), 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)

class Button(pg.sprite.Sprite):
    """Button Sprite"""
    def __init__(self, text, x, y, size = 15, scale = 0.50, color = None, image = 'button.png', font = 'GothamNarrow-Medium.ttf', text_offset = (-1,-1)):
        pg.sprite.Sprite.__init__(self)
        if color == None:
            color = COLOR.BROWN
        self.image = pg.image.load("assets/images/" + image).convert_alpha()        
        self.size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.font = pg.font.Font('assets/fonts/' + font, size)     
        self.text = self.font.render(str(text), 1, color)
        self.image.blit(self.text, [(self.image.get_width() / 2 - self.text.get_width() / 2) + text_offset[0], (self.image.get_height() / 2 - self.text.get_height() / 2) + text_offset[1]])

        