import math
import pygame




# Temporário ---------------------
from entities import Ulisses
from world_level import CombatLevel,RewardScreen
from map import MapScreen
from map_node import MapNode, MapNodeType
from fireplace import FireplaceScreen
from menu import MenuScreen

def init(surface: pygame.Surface):
    ulisses = Ulisses()
    map = MapScreen(surface)
    reward_screen = RewardScreen(surface,ulisses,map)
    fireplace = FireplaceScreen(surface, map, 20, ulisses)
    cyclop_combat = CombatLevel(surface, background_name="combat_bg", staged_enemies=['Ogre'], ulisses=ulisses, next_screen=reward_screen)
    water_horse_and_cyclop = CombatLevel(surface, background_name="combat_bg", staged_enemies=['cyclop', 'water_horse'], ulisses=ulisses, next_screen=reward_screen)
    water_horse_combat = CombatLevel(surface, background_name="combat_bg", staged_enemies=['water_horse'], ulisses=ulisses, next_screen=reward_screen)
    boss_combat = CombatLevel(surface, background_name="combat_bg", staged_enemies=['poseidon'], ulisses=ulisses, next_screen=reward_screen)
    cyclop_combat = CombatLevel(surface, background_name="combat_bg", staged_enemies=['cyclop'], ulisses=ulisses, next_screen=reward_screen)
    

    root = MapNode((220, 450), MapNodeType.STORY, None)

    f1 = MapNode((200,180), MapNodeType.FIREPLACE, fireplace)
    f2 = MapNode((150,100), MapNodeType.FIREPLACE, fireplace)
    f3 = MapNode((290,130), MapNodeType.FIREPLACE, fireplace)

    first_child_mid = MapNode((200, 350), MapNodeType.BATTLE, cyclop_combat)
    first_child_left = MapNode((130,380), MapNodeType.BATTLE, water_horse_combat)
    first_child_right = MapNode((300,380), MapNodeType.BATTLE, water_horse_combat)

    second_child_mid = MapNode((250, 270), MapNodeType.BATTLE, cyclop_combat)
    second_child_left = MapNode((100, 300), MapNodeType.BATTLE, cyclop_combat)
    second_child_right = MapNode((370, 310), MapNodeType.BATTLE, cyclop_combat)

    third_child_mid = MapNode((300, 262), MapNodeType.BATTLE, cyclop_combat)
    third_child_left = MapNode((120,230), MapNodeType.BATTLE, water_horse_and_cyclop)
    third_child_mid_left = MapNode((170, 250), MapNodeType.BATTLE, cyclop_combat)
    third_child_mid_right = MapNode((300, 210), MapNodeType.BATTLE, cyclop_combat)

    fourth_child_left = MapNode((100, 170), MapNodeType.BATTLE, cyclop_combat)
    fourth_child_mid = MapNode((240, 200), MapNodeType.BATTLE, cyclop_combat)

    boss = MapNode((220, 80), MapNodeType.BOSS, boss_combat)

    root.add_children(first_child_right)
    root.add_children(first_child_left)
    root.add_children(first_child_mid)
    first_child_right.add_children(second_child_right)
    first_child_left.add_children(second_child_left)
    first_child_right.add_children(second_child_mid)
    first_child_mid.add_children(second_child_mid)
    second_child_mid.add_children(third_child_mid_right)
    second_child_left.add_children(third_child_left)
    second_child_right.add_children(third_child_mid)
    second_child_mid.add_children(third_child_mid_left)
    third_child_mid_left.add_children(f1)
    third_child_left.add_children(f1)
    third_child_left.add_children(fourth_child_left)
    third_child_mid.add_children(fourth_child_mid)
    third_child_mid_right.add_children(f3)
    fourth_child_left.add_children(f2)
    fourth_child_mid.add_children(boss)
    f2.add_children(boss)
    f1.add_children(boss)
    f3.add_children(boss)
    map.load(root)

    return MenuScreen(surface, map)

# fim Temporário ---------------------





pygame.init()

SCREEN_DIMENSIONS = (1000,700) # Valores temporários
SCALE = 2

window_surface = pygame.display.set_mode(SCREEN_DIMENSIONS)
downscaled_surface = pygame.Surface(
    (SCREEN_DIMENSIONS[0] / SCALE, SCREEN_DIMENSIONS[1] / SCALE)
)
clock = pygame.time.Clock()
running = True

current_screen = init(downscaled_surface)
current_screen.onenter()

transition_progress = math.pi / 2 # Para ter uma transição no início do jogo
transition_surface = pygame.Surface(downscaled_surface.get_size())
transition_surface.fill((0,0,0))
transition_to = None


while running:
    # Roda apenas enquanto a transição estiver em progresso
    if transition_progress < math.pi:
        # Não atualiza nem processa os eventos; apenas desenha a tela atual
        current_screen.draw()

        transition_progress += 0.1

        # Troca `current_screen` na metade da transição, quando a tela estiver
        # toda preta, para o jogador não perceber
        if transition_progress > math.pi / 2 and transition_to != None:
            pygame.event.clear() # Ignora eventos acionados durante a transição
            current_screen = transition_to
            current_screen.onenter()
            transition_to = None

        # "Desenha" a transição sobre a surface principal.
        # `255 * (sin(t) ** 2)` faz uma transição suave de 0 -> 255 -> 0
        transition_surface.set_alpha(255 * (math.sin(transition_progress) ** 2))
        downscaled_surface.blit(transition_surface, (0,0))

    else:
        for event in pygame.event.get():
            # Pré-processa os eventos do mouse para que as telas não tenham
            # que lidar com `SCALE`
            if event.type == pygame.MOUSEBUTTONDOWN \
                or event.type == pygame.MOUSEBUTTONUP \
                or event.type == pygame.MOUSEMOTION:

                downscaled_pos = pygame.Vector2(event.dict["pos"])
                event.dict["pos"] = downscaled_pos // SCALE

            elif event.type == pygame.QUIT:
                running = False

            current_screen.handle_event(event)

        next_screen = current_screen.update()
        current_screen.draw()

        # Se a função `update()` retornou algo, começa a transição e armazena
        # a tela retornada para fazer a substituição depois
        if next_screen != None:
            transition_to = next_screen
            transition_progress = 0

    scaled_surface = pygame.transform.scale_by(downscaled_surface, SCALE)
    window_surface.blit(scaled_surface, (0,0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
