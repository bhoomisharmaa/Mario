import pygame
from tiles import*
from random import randint

class Enemy(Animated_tiles):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y,surface)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(2,4)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        #to reverse speed 
        self.speed *= -1

    def update(self,shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()