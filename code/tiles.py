import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x ,y)) 

    def update(self,shift):
        self.rect.x += shift 

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface

class FloatingTile(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('../graphics/terrain/terrain_image.png').convert_alpha())
        self.tile_speed =  3

    def move(self):
        self.rect.x += self.tile_speed

    def reverse_speed(self):
        self.tile_speed *= -1

    def update(self,shift):
        self.rect.x += shift 
        self.move()  

class Crate(StaticTile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y,surface)
        offset_y = y + size
        self.rect =  self.image.get_rect(bottomleft = (x + 5,offset_y)) 

class TreeConstraint(StaticTile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y,surface)
        offset_y = y + size - 2
        self.rect =  self.image.get_rect(bottomleft = (x + 5,offset_y))

class Animated_tiles(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def get_status(self,status):
        self.status = status

    def update(self,shift):
        #if self.status != 'gameover':
        self.animate()
        self.rect.x += shift 

class Coin(Animated_tiles):
    def __init__(self,size,x,y,path,value):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size) / 2
        self.rect = self.image.get_rect(center = (center_x,center_y))  
        self.value = value  
   
class Palm(Animated_tiles):
    def __init__(self,size,x,y,path,offset):
        super().__init__(size,x,y,path)
        offset_y = y - offset
        self.rect.topleft = (x,offset_y)

class Enemy_explosion:
    #to create enemy explosion particles
    def __init__(self,path,x,y,surface):
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = (x,y))
        self.display_surface = surface

    def animate(self):
        self.frame_index += 0.02
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.display_surface.blit(self.image,self.rect)

    def update(self,shift):
        self.animate()
        self.rect.x += shift