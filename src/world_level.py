import pygame
from entities import Enemy

class CombatLevel:
    def __init__(self,screen:pygame.display,background_name:str,stages:tuple):
        try:
            self.background_img = pygame.image.load(f'./assests/{background_name}.png')
            self.game_state = 0
            self.screen = screen
            self.stages = stages
            self.staged_enemies = stages[self.game_state]
            self.instantiated_enemies = []
        except FileNotFoundError as error:
            print(f"{error}: background assest not found in 'assests")
    def draw_level(self):
        self.screen.blit(self.background_img,(0,0))
        pygame.draw.rect(self.screen,color='brown',rect=pygame.Rect(0, 540,800,160))
        self.draw_enemies()
    def draw_enemies(self):
        for staged_enemy in self.staged_enemies:
            self.instantiated_enemies.append(Enemy(name=staged_enemy))
        for instantiated_enemy in self.instantiated_enemies:
            instantiated_enemy.draw_entity(screen=self.screen)
    def next_game_state(self):
        try:
            self.game_state += 1
            self.staged_enemies = self.stages[self.game_state]
            self.instantiated_enemies = []
        except IndexError as error:
            print(f'{error}: attempted to pass to next stage when no following stage existed')
                