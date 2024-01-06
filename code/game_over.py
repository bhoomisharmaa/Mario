import pygame,sys
from support import import_folder
from pygame.locals import*

class Game_Over:
    def __init__(self,screen,create_level,current_level,create_overworld,score,resource_path):
        self.screen = screen
        self.create_level = create_level
        self.current_level = current_level
        self.create_overworld = create_overworld
        self.score = score
        self.coin_status = False
        self.resource_path = resource_path

        self.banner_game_over = pygame.transform.scale(pygame.image.load(self.resource_path("../graphics/GameOver/banner1.png")).convert_alpha(),(350,100))
        self.banner1_rect = self.banner_game_over.get_rect(center = (600,160))
        
        self.banner_exit = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/banner2.png')).convert_alpha(),(170,73))
        self.banner2_rect = self.banner_exit.get_rect(center = (770,570))
        
        self.button_score = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/button1.png')).convert_alpha(),(60,60))
        self.button1_rect = self.button_score.get_rect(center = (490,560))

        self.button_cont = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/button2.png')).convert_alpha(),(140,55))
        self.button2_rect = self.button_cont.get_rect(center = (603,560))
                
        self.paper_2 = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/orange_paper2.png')).convert_alpha(),(280,138))
        self.paper_rect = self.paper_2.get_rect(center = (600,350))

        self.board_1 = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/Yellow_board1.png')).convert_alpha(),(350,220))
        self.board1_rect = self.board_1.get_rect(center = (600,350))
        
        self.board_2 = pygame.transform.scale(pygame.image.load(self.resource_path('../graphics/GameOver/Yellow_board2.png')).convert_alpha(),(350,132))
        self.board2_rect = self.board_2.get_rect(center = (600,560))

        self.rect = pygame.Surface((1200,704))
        self.rect.set_alpha(130)
        self.rect.fill((0,0,0))

        self.font = pygame.font.Font(self.resource_path('../graphics/ui/ARCADEPI.ttf'),35)
        self.score_no = self.font.render(str(int(self.score)),False,'#292B3D')
        self.score_rect = self.score_no.get_rect(midleft = (650,350))

    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            self.create_level(self.current_level)
                
        if pygame.mouse.get_pressed()[0]:
            if self.banner2_rect.collidepoint(pygame.mouse.get_pos()):
                self.create_overworld(0,0,False)
            elif self.button2_rect.collidepoint(pygame.mouse.get_pos()):
                self.create_level(self.current_level)

    def blit_sprites(self):
        self.screen.blit(self.rect,(0,0))
        self.screen.blit(self.banner_game_over,self.banner1_rect)
        self.screen.blit(self.board_1,self.board1_rect)
        self.screen.blit(self.board_2,self.board2_rect)
        self.screen.blit(self.button_score,self.button1_rect)
        self.screen.blit(self.button_cont,self.button2_rect)
        self.screen.blit(self.banner_exit,self.banner2_rect)
        self.screen.blit(self.paper_2,self.paper_rect)
        self.screen.blit(self.score_no,self.score_rect)

    def run(self):
        self.get_input()
        self.blit_sprites()
