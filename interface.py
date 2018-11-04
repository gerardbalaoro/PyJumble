"""Game Interface Class"""

import pygame as pg
import random, math
from engine import *
from config import *
from sprites import *

class Game:

    def __init__(self):
        """Initialize Game Instance
        
        Returns:
            None
        """
        pg.init()
        pg.mixer.init()
        self.icon = pg.image.load(ICON)
        self.background = pg.transform.scale(pg.image.load(BACKGROUND), (WIDTH, HEIGHT))
        pg.display.set_icon(self.icon)
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.load()

    def load(self):
        """Load Resources

        Returns:
            None
        """
        self.sounds = {
            'fail': pg.mixer.Sound(AUDIO['fail']),
            'success': pg.mixer.Sound(AUDIO['success']),
            'enter': pg.mixer.Sound(AUDIO['enter']),
            'click': pg.mixer.Sound(AUDIO['click']),
            'start': pg.mixer.Sound(AUDIO['start']),
            'end': pg.mixer.Sound(AUDIO['end'])
        }

        self.music = {
            'menu': AUDIO['menu'],
            'game': AUDIO['game']
        }

    def new(self, engine, mode):
        """Start a New Game

        Arguments:
            engine {Engine}
            mode {dict} : Mode configuration
        
        Returns:
            None
        """     
        self.engine = engine
        self.mode = mode
        self.pool = self.engine.combine(mode['scrambled_words'])
        self.lives = mode['lives'] if mode['lives'] != 0 else float('inf')
        self.time = mode['time'] if mode['time'] != 0 else float('inf')
        self.score = 0

        if mode['exact_match']:
            engine.search()

        self.start_time = pg.time.get_ticks()
        self.current_word = ''
        self.matched_words = []
        self.buttons = pg.sprite.Group()
        self.pool_tiles = pg.sprite.Group()
        self.word_tiles = pg.sprite.Group()
        self.pool_tiles.empty()

        for i, letter in enumerate(self.pool):
            self.pool_tiles.add(Letter(letter, i + 1, len(self.pool)))

        self.word_tiles.add(Text(self.mode['instructions'], 15, COLOR.BROWN, WIDTH / 2, int(HEIGHT * 0.6)))
        self.word_tiles.add(Text('PRESS [ ENTER ] TO SUBMIT AND [ ESC ] TO EXIT', 15, COLOR.BROWN, WIDTH / 2, int(HEIGHT * 0.6) + 25))
        self.sounds['start'].play()
        pg.mixer.music.load(self.music['game'])
        self.run()        

    def run(self):
        """Run Game Loop

        Returns:
            None
        """
        pg.mixer.music.play(loops=-1)
        self.playing = True  
        while self.playing:
            time_color = COLOR.BROWN
            if self.time != float('inf'):
                time_elapsed = int((pg.time.get_ticks() - self.start_time) / 1000)
                time_left = self.time - time_elapsed
                if time_left == 0:
                    self.playing = False
                elif time_left < 11:
                    time_color = COLOR.RED
            else:
                time_left = '--'
            
            lives_left = '--' if self.lives == float('inf') else self.lives

            if self.lives == 0:
                self.playing = False

            if self.mode['exact_match']:
                if sorted(self.matched_words) == sorted(self.engine.matchable):
                    self.playing = False

            self.clock.tick(FPS)
            self.screen.blit(self.background, (0,0))
            self.buttons.empty()
            self.buttons.add(Button(lives_left, int(WIDTH * 0.2), 5, image = 'button_lives.png', text_offset=(10,-1), color=COLOR.RED if self.lives < 3 else None))
            self.buttons.add(Button(time_left, int(WIDTH * 0.8), 5, image = 'button_timer.png', text_offset=(10,-1), color=time_color))
            self.buttons.add(Button('SCORE : ' + str(self.score), int(WIDTH * 0.5), 5))
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        """Update Game Screen
        
        Returns:
            None
        """
        self.pool_tiles.update()
        self.word_tiles.update()
        self.buttons.update()

    def events(self):
        """Handle Game Events

        Returns:
            None
        """
        for event in pg.event.get():
            # Catch Close Window Event
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYUP:                
                self.word_tiles.empty()                
                if event.key in list(ord(c) for c in self.pool):                    
                    letter = pg.key.name(event.key)
                    if self.current_word.count(letter) < self.pool.count(letter):
                        self.sounds['click'].play()
                        self.current_word += letter
                    else:
                        self.sounds['fail'].play()
                elif event.key == pg.K_BACKSPACE:  
                    self.sounds['enter'].play()                  
                    self.current_word = self.current_word[0:-1]
                elif event.key in [pg.K_KP_ENTER, pg.K_RETURN]:
                    if len(self.current_word) > 0:
                        self.sounds['enter'].play()                        
                        if self.current_word not in self.matched_words:
                            if self.mode['exact_match']:
                                if self.current_word in self.engine.matchable:
                                    check = True
                                else:
                                    check = False
                            else:
                                check = self.engine.check(self.current_word)
                            if check:
                                self.sounds['success'].play()
                                score = self.engine.score(self.current_word)
                                self.score += score
                                self.matched_words.append(self.current_word)
                                self.word_tiles.add(Button("NICE! THAT'S " + str(score) + " POINT" + ('S' if score > 1 else '') + " FOR YOU", WIDTH / 2, int(HEIGHT * 0.6), size=15, color=COLOR.GREEN))
                            else:
                                self.sounds['fail'].play()
                                self.lives -= 1
                                self.word_tiles.add(Button("OOPS! THAT'S NOT A VALID WORD", WIDTH / 2, int(HEIGHT * 0.6), size=15, color=COLOR.RED))
                        else:
                            self.sounds['fail'].play()
                            if STRICT == True:
                                self.lives -= 1
                            self.word_tiles.add(Button("NOPE! YOU TRIED THAT ALREADY", WIDTH / 2, int(HEIGHT * 0.6), size=15, color=COLOR.ORANGE))

                        self.current_word = ''
                elif event.key == pg.K_ESCAPE:
                    self.sounds['enter'].play()
                    self.playing = False
                else:
                    self.sounds['fail'].play()
                
                if len(self.current_word) > 0:
                    for i, letter in enumerate(self.current_word):
                        self.word_tiles.add(Letter(letter, i + 1, len(self.current_word), margin=int((HEIGHT - 20) / 2 + 50)))
                elif len(self.word_tiles.sprites()) == 0:
                    self.word_tiles.add(Text(self.mode['instructions'], 15, COLOR.BROWN, WIDTH / 2, int(HEIGHT * 0.6)))
                    self.word_tiles.add(Text('PRESS [ ENTER ] TO SUBMIT AND [ ESC ] TO EXIT', 15, COLOR.BROWN, WIDTH / 2, int(HEIGHT * 0.6) + 25))
                
    def draw(self):
        """Draw Game Elements
        
        Returns:
            None
        """
        self.pool_tiles.draw(self.screen)
        self.buttons.draw(self.screen)
        self.word_tiles.draw(self.screen)
        pg.display.flip()

    def start_screen(self):
        """Show Start Screen, Ask User to Select Game Mode

        Returns:
            {dict} : Game mode configuration, see config.py
        """
        self.screen.blit(self.background, (0,0))
        if pg.mixer.music.get_busy() == False:
            pg.mixer.music.load(self.music['menu'])
            pg.mixer.music.play(loops=-1)
        self.buttons = pg.sprite.Group()
        for i, letter in enumerate(TITLE):            
            self.buttons.add(Letter(letter, i + 1, len(TITLE), margin=100))
        for i, mode in enumerate(MODES):
            self.buttons.add(Button('[ ' + mode['key'].upper() + ' ] PLAY ' + mode['name'].upper(), WIDTH / 2, (HEIGHT / 2) + (i * 50)))
        self.buttons.add(Text('PRESS THE KEY OF YOUR CHOICE', 13, COLOR.BROWN, WIDTH / 2, (HEIGHT / 2) + (len(MODES) * 50)))
        self.buttons.add(Button('[i]', WIDTH - 100, (HEIGHT - 100), image='button_box.png'))
        self.buttons.draw(self.screen)        
        pg.display.flip()
        selected = self.wait_input(list(ord(mode['key']) for mode in MODES) + [pg.K_i])
        for mode in MODES:
            if mode['key'] == selected:
                pg.mixer.music.fadeout(500)
                return mode
        return selected

    def credits(self):
        """Show Credits Screen

        Returns:
            None
        """
        self.screen.blit(self.background, (0,0))
        self.buttons = pg.sprite.Group()
        for i, letter in enumerate(TITLE):            
            self.buttons.add(Letter(letter, i + 1, len(TITLE), margin=100))

        for i, line in enumerate(CREDITS + ['PRESS ANY KEY TO CONTINUE']):
            size = 15 if i < 2 else 13
            color = COLOR.BROWN if i == len(CREDITS) else COLOR.DARK
            height = 18 if i == len(CREDITS) else 17
            self.buttons.add(Text(line, size, color, WIDTH / 2, (HEIGHT / 2 - 25) + (i * height), font='Gotham-Medium.ttf'))
        self.buttons.draw(self.screen)        
        pg.display.flip()
        self.wait_input()

    def game_over(self):
        """Show Game Over Screen
        
        Returns:
            None
        """
        self.screen.blit(self.background, (0,0))
        self.buttons = pg.sprite.Group()
        for i, letter in enumerate('GAMEOVER'):
           self.buttons.add(Letter(letter, i + 1, 8, margin=100))
        self.buttons.add(Button('SCORE : ' + str(self.score), int(WIDTH * 0.5), HEIGHT / 2))
        self.buttons.add(Text('PRESS [ SPACE ] TO CONTINUE', 13, COLOR.BROWN, WIDTH / 2, (HEIGHT / 2) + 100))
        self.buttons.draw(self.screen)
        self.sounds['end'].play()
        pg.display.flip()
        self.wait_input([pg.K_SPACE])

    def wait_input(self, accepted = []):
        """Wait for User Input

        Used for Static Screens (Start Menu, Game Over, etc)

        Arguments:
            accepted {list}: List of accepted keys
        
        Returns:
            {str}: Key name, none
        """
        waiting = True
        while waiting and self.running:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    if event.key in accepted or not bool(accepted):
                        self.sounds['enter'].play()
                        waiting = False
                        return pg.key.name(event.key)