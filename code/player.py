import pygame
from support import import_folder
from pygame.locals import*
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surface,create_jump_particles,change_health,score_board_status):
        super().__init__()
        self.import_character_assests()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.player_sprite = pygame.sprite.Group()
        self.score_board_status = score_board_status

        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -19
        self.collision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))

        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        #health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 400
        self.hurt_time = 0

        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        #sound
        self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

    def import_character_assests(self):
        character_path = '../graphics/character/'
        self.animations = {'idle' : [], 'run' : [], 'jump' : [], 'fall' : [], 'attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation 
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        if self.frame_index >= (len(animation) - 1):
            self.frame_index = 0
        else:
            self.frame_index += self.animation_speed

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            fipped_image = pygame.transform.flip(image,True,False)
            self.image = fipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.status == 'attack':
            scaled_image = pygame.transform.scale(image,(88,90))
            self.image = scaled_image

        if self.invincible:
            alpha_val = self.wave_value()
            self.image.set_alpha(alpha_val)
        else:
            self.image.set_alpha(255)
     
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
                
            
            #full_run_dust_path = self.dust_run_particles + self.dust_ani[int(self.dust_frame_index)]
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right and self.on_ground:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle,pos)

            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust = pygame.transform.flip(dust_particle,True,False)
                self.display_surface.blit(flipped_dust,pos)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x > 0 or  self.direction.x < 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def get_input(self):
        #to get input of keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)
            self.jump_sound.play()

        if keys[pygame.K_x]:
            self.status = 'attack'
        """
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_x:
                self.status = 'attack'
        """

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
       self.direction.y = self.jump_speed
    
    def get_damage(self):
        if not self.invincible:
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            self.hit_sound.play()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0

    def sword(self):
        self.sword_image = pygame.image.load('../graphics/character/sword/sword.png').convert_alpha()
        sword_x = self.rect.x + 55
        sword_y = self.rect.y + 39
        self.sword_rect = self.sword_image.get_rect(center = (sword_x,sword_y))
        if not self.on_ceiling and self.facing_right and self.status != 'attack':
            self.display_surface.blit(self.sword_image,self.sword_rect)
        elif not self.facing_right and self.status != 'attack':
            sword_transform =  pygame.transform.flip(self.sword_image,True,False)
            swordX = self.rect.x - 7
            swordY = sword_y
            transform_rect = sword_transform.get_rect(center = (swordX,sword_y))
            self.display_surface.blit(sword_transform,transform_rect)
    
    def update(self):
        if self.score_board_status == False:
            self.get_input()
            self.animate()
            self.get_status()
            self.run_dust_animation()
            self.invincibility_timer()
