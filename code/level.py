import pygame,sys
from pygame.locals import*
from support import*  
from settings import*
from tiles import*
from enemy import*
from decoration import*
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health,create_game_over,game_over_status,score,high_score,resource_path):
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None 
        self.score = score
        self.high_score = high_score
        self.score_board_status = False
        self.game_over_status = game_over_status
        self.resource_path = resource_path

        #overworld connections
        self.create_overworld = create_overworld
        self.create_game_over = create_game_over
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        #terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        #font
        self.font = pygame.font.Font(self.resource_path('../graphics/ui/ARCADEPI.ttf'),50)
        self.score_text = self.font.render("score: ",False,'white')##
        self.score_txt_rect = self.score_text.get_rect(center = (500,60))
        self.score_no = self.font.render(str(self.score),False,'white')
        self.score_rect = self.score_no.get_rect(midleft = (610,60))

        if self.current_level != 0:
            #floating tiles
            float_tile_layout = import_csv_layout(level_data['floating_tiles'])
            self.float_sprites = self.create_tile_group(float_tile_layout, 'floating_tiles')

            tile_constraint_layout = import_csv_layout(level_data['tile_constraint'])
            self.tile_constraint_sprite = self.create_tile_group(tile_constraint_layout,'tile_constraint')

        #grass
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        #crate
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        #coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprite = self.create_tile_group(coin_layout, 'coins')

        #fg palms
        fg_palm_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palm_sprite = self.create_tile_group(fg_palm_layout, 'fg_palms')

        #bg_palms
        bg_palm_layout = import_csv_layout(level_data['bg_palms'])
        self.bg_palm_sprite = self.create_tile_group(bg_palm_layout, 'bg_palms') 

        #enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        #constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprite = self.create_tile_group(constraint_layout, 'constraint')

        tree_constraint_layout = import_csv_layout(level_data['tree_constraints'])
        self.tree_constraint_sprite = self.create_tile_group(tree_constraint_layout, 'tree_constraint')

        #player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout,change_health)

        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()

        #decoration
        self.sky = Sky(8)
        level_width = 78 * tile_size
        self.water = Water(screen_height - 40,level_width * 1.5)
        self.clouds = Clouds(400,level_width,20)
        self.player_on_ground = False
        self.crate_collision = False

        #user interface
        self.change_coins = change_coins

        #sounds
        self.coin_sound = pygame.mixer.Sound(self.resource_path('../audio/effects/coin.wav'))
        self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')

        #buttons
        self.score_button = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/buttons/scoreboard.png')).convert_alpha(),(50,50))
        self.score_button_rect = self.score_button.get_rect(center = (1100,40))

    def create_tile_group(self,layout,type):

        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    sprite = False

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(self.resource_path("../graphics/terrain/terrain_tiles.png"))
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'floating_tiles':
                        sprite = FloatingTile(3*tile_size,x,y)
                                            
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics(self.resource_path("../decoration/grass/grass.png"))
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size,x,y,pygame.image.load(self.resource_path("../graphics/terrain/crate.png")).convert_alpha())

                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size,x,y,self.resource_path("../graphics/coins/gold"),5)
                        if val == '1': sprite = Coin(tile_size,x,y,self.resource_path("../graphics/coins/silver"),1)

                    if type == 'fg_palms':
                        if val == '4': sprite = Palm(tile_size,x,y,self.resource_path("../graphics/terrain/palm_small"),38)
                        elif val == '3': sprite = Palm(tile_size,x,y,self.resource_path("../graphics/terrain/palm_large"),70)

                    if type == 'bg_palms':
                        sprite = Palm(tile_size,x,y,self.resource_path("../graphics/terrain/palm_bg"),60)

                    if type == 'enemies':
                        sprite = Enemy(tile_size,x,y,self.resource_path("../graphics/enemy/run"))

                    if type == 'tree_constraint':
                        sprite = TreeConstraint(tile_size,x,y,pygame.image.load(self.resource_path("../graphics/terrain/constraintss.png")).convert_alpha())

                    if type == 'constraint':
                        sprite = Tile(tile_size,x,y)

                    if type == 'tile_constraint':
                        sprite = Tile(tile_size,x,y)

                    if not sprite: pass
                    else: sprite_group.add(sprite)
        if self.score_board_status == False:
            return sprite_group

    def player_setup(self,layout,change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x,y),self.display_surface,self.create_jump_particles,change_health,self.score_board_status)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load(self.resource_path("../graphics/character/hat.png"))
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x *player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.tree_constraint_sprite.sprites()
        if self.current_level != 0:
            collidable_sprites += self.float_sprites.sprites() 

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):

                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.collision_rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.collision_rect.right

                if self.current_level != 0:
                    for image in self.float_sprites.sprites():
                        if image == sprite:
                            player.rect.x += image.tile_speed

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidableSprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.tree_constraint_sprite.sprites()
        if self.current_level != 0:
            collidableSprites += self.float_sprites.sprites() 
        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0: 
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

                if self.current_level != 0:
                    for image in self.float_sprites.sprites():
                        if image == sprite:
                            player.collision_rect.x += image.tile_speed  * 2
                        
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def scroll_x(self):
        #to move player left and right
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width - (screen_width / 1.2) and direction_x < 0 and not self.score_board_status and not self.game_over_status:
            self.world_shift = 8
            player.speed = 0
            
        elif player_x > screen_width - (screen_width / 1.2) and direction_x > 0 and not self.score_board_status and not self.game_over_status:
            self.world_shift = -8
            player.speed = 0
    
        else:
            if not self.score_board_status and not self.game_over_status:
                self.world_shift = 0
                player.speed = 8            

    def get_player_on_ground(self):
        #to check if player is on ground
        player = self.player.sprite
        if player.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_particles(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particles = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particles)

    def enemy_collision(self):
        #to check collision between enemy and constraints(chote chote red wale )
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprite,False):
                enemy.reverse()

    def create_jump_particles(self,pos):
        #to create jump particles
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def tile_collision(self):
        #to check collision between floating tile and constraint
        for image in self.float_sprites.sprites():
            if pygame.sprite.spritecollide(image,self.tile_constraint_sprite.sprites(),False):
                image.reverse_speed()
                    
    def check_death(self):
        #to check player death
        if self.player.sprite.rect.top > screen_height:
            self.create_game_over(self.current_level,self.score)
            self.game_over_status = True

    def check_win(self):
        #to check if player won or not
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
            self.create_overworld(self.current_level,self.new_max_level,True)

    def button_func(self):
        #button functions
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and not self.game_over_status:
            self.score_board_status = True
       
        if pygame.mouse.get_pressed()[0]:
            if self.score_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.score_board_status = True

    def score_calculator(self):
        #to calculate score and high score
        self.score_no = self.font.render(str(int(self.score)),False,'white')
        if not self.score_board_status and not self.game_over_status:
            self.score += 0.002
            
        if self.score > self.high_score and not self.game_over_status:
            self.high_score = int(self.score)

    def check_coin_collisions(self):
        #to check player collision with coins
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprite,True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(coin.value)
                self.coin_sound.play()
                self.score += coin.value * 2

    def check_enemy_collision(self):
        #to check enemy collision with player
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_centery = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                exp_x = enemy.rect.x 
                exp_y = enemy.rect.y
                enemy_explosion = Enemy_explosion(self.resource_path("../graphics/enemy/explosion"),exp_x,exp_y,self.display_surface)
                if enemy_top < player_bottom < enemy_centery and self.player.sprite.direction.y >= 0 and not self.player_on_ground:
                    enemy.kill()
                    enemy_explosion.update(self.world_shift)
                    self.stomp_sound.play()
                    self.score += 30
                else:
                    self.player.sprite.get_damage()

    def score_board(self):
        green_board1 = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/green_board_1_.png')).convert_alpha(),(390,364))
        green_board1_rect = green_board1.get_rect(center = (600,270))

        green_board2 = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/green_board2.png')).convert_alpha(),(390,129))
        green_board2_rect = green_board2.get_rect(center = (600,530))

        green_button = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/green_button1.png')).convert_alpha(),(50,50))
        green_button_rect = green_button.get_rect(center = (430,110))

        high_score_txt = self.font.render(str(self.high_score),False,'#292B3D')##
        high_score_txt_rect = high_score_txt.get_rect(center = (600,230))
        score_txt = self.font.render(str(int(self.score)),False,'#292B3D')##
        score_txt_rect = score_txt.get_rect(center = (600,350))

        rect = pygame.Surface((1200,704))
        rect.set_alpha(130)
        rect.fill((0,0,0))

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RETURN]:
            self.score_board_status = False

        if pygame.mouse.get_pressed()[0]:
            if green_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.score_board_status = False                


        self.display_surface.blit(rect,(0,0))
        self.display_surface.blit(green_board1,green_board1_rect)
        self.display_surface.blit(green_board2,green_board2_rect)
        self.display_surface.blit(green_button,green_button_rect)
        self.display_surface.blit(high_score_txt,high_score_txt_rect)
        self.display_surface.blit(score_txt,score_txt_rect)

    def run(self):
        #to run entire game

        #decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)
        
        #bg_palms
        if not self.score_board_status and not self.game_over_status:
            self.bg_palm_sprite.update(self.world_shift)
        self.bg_palm_sprite.draw(self.display_surface)

        #enemy
        if not self.score_board_status and not self.game_over_status:
            self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_collision()
        
        #grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        #crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        #fg_plams
        if not self.score_board_status and not self.game_over_status:
            self.fg_palm_sprite.update(self.world_shift)
        self.fg_palm_sprite.draw(self.display_surface)

        self.tree_constraint_sprite.update(self.world_shift)

        #coins
        if not self.score_board_status and not self.game_over_status:
            self.coin_sprite.update(self.world_shift)
        self.coin_sprite.draw(self.display_surface)
        self.check_coin_collisions()

        #player
        self.player.draw(self.display_surface)
        if not self.score_board_status and not self.game_over_status:
            self.player.update()
            self.scroll_x()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.get_player_on_ground()                                                                                                                                                                                            
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()
        self.button_func()

        #dust particle
        self.create_landing_particles()
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        if self.current_level != 0:
            #constraint
            self.tile_constraint_sprite.update(self.world_shift)

            self.float_sprites.draw(self.display_surface)
            if not self.score_board_status and not self.game_over_status:
                self.float_sprites.update(self.world_shift)
            self.tile_collision()

        #constraint
        self.constraint_sprite.update(self.world_shift)

        #buttons
        self.display_surface.blit(self.score_button,self.score_button_rect)

        #water
        self.water.draw(self.display_surface)
        if not self.score_board_status and not self.game_over_status:
            self.water.update(self.world_shift)
        self.check_enemy_collision()

        #score
        self.score_calculator()
        self.display_surface.blit(self.score_text,self.score_txt_rect)
        self.display_surface.blit(self.score_no,self.score_rect)

        #scoreboard
        if self.score_board_status:
            self.score_board()
