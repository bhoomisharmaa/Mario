import pygame
from game_data import levels
from support import import_folder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,icon_speed,path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2), icon_speed, icon_speed)

    def animate(self):
        self.frame_index += 0.15           
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == 'available':
            self.animate()
        else:
            self.image.set_alpha(180)  

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self,current_level,max_level,surface,create_level,win_status,resource_path):

        #setup
        self.current_level = current_level
        self.max_level = max_level
        self.display_surface = surface
        self.create_level = create_level
        self.win_status = win_status
        self.resource_path = resource_path

        #sprites
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8)

        #movement
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        #time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_lenght = 300
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'],'available',8,node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'],'locked',8,node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface,'#a04f45',False,points,6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites() [self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.moving and self.allow_input:
            if self.current_level < 2 and self.win_status:
                self.move_direction = self.get_movement_data('next')
                self.win_status = False
                if self.current_level > 2:
                    self.current_level = 0
                else:
                    self.current_level += 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self,target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize() ##

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]

            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def input_time(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_lenght:
                self.allow_input = True

    def run(self):
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        if self.current_level > 0:
            self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.input()
        self.input_time()
