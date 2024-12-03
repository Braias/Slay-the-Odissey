"""Módulo responsável pelo menu inicial do jogo."""


import pygame
import sys
from menu_button import Button
from screen import Screen


class MenuScreen(Screen):
    def __init__(self, surface: pygame.Surface, map):
        self._load_sprites()
        self.pos = pygame.Vector2(surface.get_size())
        self.pos -= self.menu_sprite.get_size()
        self.pos /= 2
        self.map = map
        self.buttons = []
        self.pressed_play = False
        self.surface = surface
        self.title_surface = pygame.font.Font("assets/font.ttf", 50).render("Slay the Odissey", True, "#b68f40")
        self.title_pos = (self.surface.get_width() / 2 - self.title_surface.get_width() / 2, 30)

        self.buttons.append(Button(
            (self.surface.get_width() / 2, 140),
            (200, 50),
            "Jogar",
            self.font
        ))
        self.buttons.append(Button(
            (self.surface.get_width() / 2, 220),
            (200, 50),
            "Sair",
            self.font
        ))

        self.surface = surface

    def handle_event(self, ev: pygame.event.Event):
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons[0].is_hovering:
                self.pressed_play = True
            if self.buttons[1].is_hovering:
                pygame.quit()
                sys.exit()
        elif ev.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.on_mouse_motion(ev.dict["pos"])

    def update(self):
        if self.pressed_play:
            return self.map
    
    def onenter(self):
        pass

    def draw(self):
        self.surface.fill((0,0,0))
        self.surface.blit(self.menu_sprite, self.pos)
        self.surface.blit(self.title_surface, self.title_pos)
        
        for button in self.buttons:
            button.draw(self.surface)
            
    def _load_sprites(self):
        self.menu_sprite = pygame.image.load("assets/artRio.png")
        self.font = pygame.font.Font("assets/font.ttf", 30)
