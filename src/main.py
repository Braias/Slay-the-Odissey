# Example file showing a basic pygame "game loop" 
import pygame
import entities
from world_level import CombatLevel
pygame.init()

SCREEN_DIMENSIONS = (800,700)

screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
running = True

ulisses = entities.Ulisses()

cl = CombatLevel(screen=screen,background_name='test_bg',staged_enemies=['Ogre','King'])

index = True
while running:
    entities_on_screen = [ulisses]+cl.instantiated_enemies
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            cl.handle_event(event,ulisses)
    cl.update(ulisses)
    cl.draw_level(ulisses)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()