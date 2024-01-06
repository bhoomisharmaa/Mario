import pygame
from settings import*
from tiles import Animated_tiles,StaticTile
from support import import_folder
from random import randint,choice

class Sky:
    def __init__(self,horizon):
        self.top = pygame.image.load("../decoration/sky/sky_top.png").convert()
        self.bottom = pygame.image.load("../decoration/sky/sky_bottom.png").convert()
        self.middle = pygame.image.load("../decoration/sky/sky_middle.png").convert()
        self.horizon =  horizon

        #stretch
        self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
        self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))
        self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))     

    def draw(self,surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row == self.horizon:
                surface.blit(self.middle,(0,y))
            elif row > self.horizon:
                surface.blit(self.bottom,(0,y))

class Water:
    def __init__(self,top,level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width) / water_tile_width)
        self.water_sprite = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = Animated_tiles(192,x,y,"../decoration/water")
            self.water_sprite.add(sprite)

    def draw(self,surface):
        self.water_sprite.draw(surface)

    def update(self,shift):
        self.water_sprite.update(shift)

class Clouds:
    def __init__(self,horizon,level_width,cloud_number):
        cloud_surface_list = import_folder("../decoration/clouds")
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surface_list)
            x = randint(min_x,max_x)
            y = randint(min_y,max_y)
            sprite = StaticTile(0,x,y,cloud)
            self.cloud_sprites.add(sprite)

    def draw(self,surface,shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)