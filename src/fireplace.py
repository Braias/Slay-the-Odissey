import pygame
from screen import Screen

class FireplaceScreen(Screen):
    def __init__(self, surface: pygame.Surface, next_screen: Screen, hp: int):
        self.surface = surface
        self.map = next_screen
        surface_size = pygame.Vector2(surface.get_size())
        self.sprite_pos = surface_size / 2 - (32,32)

        font = pygame.font.SysFont("Times New Roman", 16)
        self.text_surface = font.render(f"Você recuperou {hp} HP", False, (255,255,255))
        self.text_pos = (surface_size + (-self.text_surface.get_width(), 100)) / 2

        ss = pygame.image.load("assests/fireplace.png")
        self.sprites = [
            ss.subsurface((0,0,64,64)),
            ss.subsurface((64,0,64,64)),
            ss.subsurface((128,0,64,64)),
            ss.subsurface((192,0,64,64)),
            ss.subsurface((256,0,64,64))
        ]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.dict["key"] == 32:
            self.timeout = 1000

    def update(self):
        self.timeout += 1

        if self.timeout > 120: # 2 segundos a 60 fps
            return self.map

    def draw(self):
        self.animation_time += 1

        sprite_idx = int(self.animation_time / 8) % 5
        self.surface.blit(self.sprites[sprite_idx], self.sprite_pos)
        self.surface.blit(self.text_surface, dest=self.text_pos)

    def onenter(self):
        self.animation_time = 0
        self.timeout = 0
