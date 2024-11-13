# Example file showing a basic pygame "game loop" 
import pygame
import entities
from deck import Deck
from world_level import CombatLevel
pygame.init()

SCREEN_DIMENSIONS = (800,700)

screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
clock = pygame.time.Clock()
running = True

ulisses = entities.Ulisses()

cl = CombatLevel(screen=screen,background_name='test_bg',stages=(['Ogre'],['King']))

index = True
while running:
    entities_on_screen = [ulisses]+cl.instantiated_enemies
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            if cl.is_player_turn:
                cl.player_combat_loop(ulisses,screen,current_mouse_pos)
            if ulisses.rect.collidepoint(current_mouse_pos):
                ulisses.deck.shuffle_and_allocate()
                cl.is_player_turn = not(cl.is_player_turn)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                cl.execute_enemy_combat_loop(ulisses)


    cl.draw_level()
    ulisses.draw_entity(screen)
    if cl.is_player_turn:
        ulisses.deck.draw_hand_on_screen(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()