import math
import pygame




# Temporário ---------------------
from entities import Ulisses
from world_level import CombatLevel
from map import MapScreen
from map_node import MapNode, MapNodeType
from fireplace import FireplaceScreen
from menu import MenuScreen

ulisses = Ulisses()
def init(surface: pygame.Surface):
    map = MapScreen(surface)
    fireplace = FireplaceScreen(surface, map, 20)
    combat = CombatLevel(surface, background_name="test_bg", staged_enemies=['Ogre'], ulisses=ulisses)

    root = MapNode((220, 450), MapNodeType.STORY, None)
    child = MapNode((250, 350), MapNodeType.FIREPLACE, fireplace)
<<<<<<< HEAD
    root.add_children(child)
    child.add_children(MapNode((200, 270), MapNodeType.FIREPLACE, fireplace))
=======
    root.add_child(child)
    child.add_child(MapNode((200, 270), MapNodeType.BATTLE, combat))
>>>>>>> 074453df1079fb6a9ab16aedded9fd319ac9bdad

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
