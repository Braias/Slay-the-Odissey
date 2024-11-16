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

cl = CombatLevel(screen=screen,background_name='test_bg',stages=(['Ogre','King'], ['King']))

index = True
while running:
    entities_on_screen = [ulisses]+cl.instantiated_enemies
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            if cl.is_player_turn:
                cl.player_combat_loop(ulisses,current_mouse_pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                cl.end_player_turn(ulisses)
            elif event.key == pygame.K_SPACE:
                ulisses.deck.shuffle_and_allocate()
            elif event.key == pygame.K_a:
                print("bundaa")
                ulisses.attack_animate()

    cl.draw_level()
    ulisses.draw_entity(screen)
    if cl.is_player_turn:
        ulisses.deck.draw_hand_on_screen(screen)
    else:
        cl.execute_enemy_combat_loop(ulisses)
        cl.end_enemies_turn()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()