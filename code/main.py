import pygame,sys
import os
from settings import*
from level import Level
from overworld import Overworld
from game_data import level_0,level_1
from ui import UI
from game_over import Game_Over
from tiles import Animated_tiles

class Game:
    def __init__(self):
        #game attributes
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.game_over_status = False
        self.score = 0
        self.high_score = 0

        #sound
        self.bg_music = pygame.mixer.Sound(self.resource_path('../audio/level_music.wav'))
        self.overworld_music = pygame.mixer.Sound(self.resource_path('../audio/overworld_music.wav'))

        #overworld
        self.overworld = Overworld(0,self.max_level,screen,self.create_level,False,self.resource_path)
        self.status = 'overworld'
        self.level =  Level(0,screen,self.create_overworld,self.change_coins,self.change_health,self.create_game_over,self.game_over_status,self.score,self.high_score,self.resource_path)
        self.overworld_music.play(loops = -1)
        self.ui = UI(screen)
        self.coin = 0

        #game over screen
        self.game_over = Game_Over(screen,self.create_level,0,self.create_overworld,0,self.resource_path)

    def resource_path(self,relative_path):
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

        """
        asset_url = resource_path('assets/chars/hero.png')
        hero_asset = pygame.image.load(asset_url)
        """

    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health,self.create_game_over,self.game_over_status,self.score,self.high_score,self.resource_path)
        self.status = 'level'
        self.overworld_music.stop()
        self.bg_music.play()
        
    def create_overworld(self,current_level,new_max_level,win_status):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        if self.cur_health <= 0:
            self.max_level = 0
            current_level = 0
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level,win_status,self.resource_path)
        self.status = 'overworld'
        self.coin = 0
        self.cur_health = 100
        self.bg_music.stop()

    def create_game_over(self,current_level,score):
        self.game_over = Game_Over(screen,self.create_level,current_level,self.create_overworld,score,self.resource_path)
        self.status = 'gameover'
        self.bg_music.stop()

    def change_coins(self,amount):
        self.coin += amount

    def change_health(self,amount):
        self.cur_health += amount

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health,self.max_health)
            self.ui.show_coin(self.coin)

        if self.cur_health <= 0:
            self.create_overworld(0,self.max_level,False)

        if self.status == 'gameover':
            self.game_over.run()
        

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
pygame.display.set_caption("Mario")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    game.run()
    
    pygame.display.update()
    clock.tick(60)