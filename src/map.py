""" Módulo responsável pelas mecânicas do mapa do jogo """


import pygame
from map_node import MapNode, MapNodeType, Point


SCROLL_SPEED = 7
MARGIN = 20

COLOR_MAP = (255, 194, 161)


def _get_sprite(rect, spritesheet: pygame.Surface):
    rect = pygame.Rect(rect)
    sprite = pygame.Surface(rect.size)
    sprite.blit(spritesheet, (0, 0), rect)
    sprite.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    return sprite
    

class MapScreen(pygame.Surface): # TODO: implicações de herdar Surface
    def __init__(self, target: pygame.Surface, root: MapNode):
        self._load_sprites()
        self.size = self.map_sprite.get_size()
        self.pos = (
            (target.get_width() - self.size[0]) >> 1,
            (target.get_height() - self.size[1]) >> 1
        )

        pygame.Surface.__init__(self, (self.size[0], self.size[1]))
        self.target = target
        
        self.root = root
        self.nodes = set([root])
        self._add_children(root)

        self.hovered_node = None
        self.current_node = root
        self.choosen_node = None
        root.begin()

        self.scrolling = False
        self.scroll_initial_y = 0

        self.scroll_interval = (target.get_height() - self.size[1] - MARGIN, MARGIN)
        self._scroll_to(root)

    def handle_event(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEMOTION:
            self._mouse_motion(ev.dict["pos"])

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_down(ev.dict["pos"], ev.dict["button"])

        elif ev.type == pygame.MOUSEBUTTONUP:
            self._mouse_up(ev.dict["pos"], ev.dict["button"])

        elif ev.type == pygame.MOUSEWHEEL:
            self.hovered_node = None
            self.pos = (
                self.pos[0],
                pygame.math.clamp(
                    self.pos[1] + ev.dict["y"] * SCROLL_SPEED,
                    self.scroll_interval[0],
                    self.scroll_interval[1],
                )
            )

    def get(self):
        node = self.choosen_node
        self.choosen_node = None
        if node != None:
            self._scroll_to(node)
            return node.data

    def render(self):
        self.blit(self.map_sprite, (0,0))

        self._render_edges(self.root)
        for node in self.nodes:
            self._render_node(node)

        self.target.blit(self, (self.pos[0], self.pos[1]))

    def _scroll_to(self, node: MapNode):
        self.pos = (
            self.pos[0],
            pygame.math.clamp(
                (self.target.get_height() * 3/4) - node.pos[1],
                self.scroll_interval[0],
                self.scroll_interval[1],
            )
        )

    def _mouse_motion(self, mouse_pos: Point):
        if self.scrolling:
            self.pos = (
                self.pos[0],
                pygame.math.clamp(
                    mouse_pos[1] - self.scroll_initial_y,
                    self.scroll_interval[0],
                    self.scroll_interval[1],
                )
            )

        for node in self.nodes:
            if not node.is_navigable: continue
            
            diff = (node.pos[0] - mouse_pos[0] + self.pos[0]) ** 2 + \
                   (node.pos[1] - mouse_pos[1] + self.pos[1]) ** 2

            if (diff < self._node_radius(node) ** 2):
                self.hovered_node = node
                return

        self.hovered_node = None

    def _mouse_down(self, mouse_pos: Point, button: int):
        if button != 1: return
        
        if self.hovered_node != None:
            self.current_node.navigate_to(self.hovered_node)
            self.current_node = self.hovered_node
            self.choosen_node = self.hovered_node
            self.hovered_node = None

            return self.current_node.data
        else:
            self.scrolling = True
            self.scroll_initial_y = mouse_pos[1] - self.pos[1]

        return None

    def _mouse_up(self, mouse_pos: Point, button: int):
        if button == 1:
            self.scrolling = False

    def _load_sprites(self):
        self.map_sprite = pygame.image.load("assests/map_bg.png").convert()

        # só pra deixar mais claras as coordenadas abaixo
        f = lambda x, y: (x * 48, y * 48, 48, 48)

        ss = pygame.image.load("assests/map_icons.png").convert()
        self.node_sprites = [
            _get_sprite(f(3,0), ss), # nó de batalha inacessível
            _get_sprite(f(3,1), ss), # nó de história inacessível
            _get_sprite((128, 96, 64, 64), ss), # nó de boss inacessível
            _get_sprite(f(2,0), ss), # nó ... já visitado
            _get_sprite(f(2,1), ss),
            _get_sprite((0,96,64,64), ss),
            _get_sprite(f(0,0), ss), # nó ... acessível
            _get_sprite(f(0,1), ss),
            _get_sprite((0,96,64,64), ss),
            _get_sprite(f(1,0), ss), # nó ... sendo selecionado pelo mouse
            _get_sprite(f(1,1), ss),
            _get_sprite((64,96,64,64), ss),
        ]

    def _add_children(self, node: MapNode):
        self.nodes.update(node.children)
        for child in node.children:
            self._add_children(child)

    def _render_edges(self, origin: MapNode):
        for child in origin.children:
            if (child.was_visited or child.is_navigable) and origin.was_visited:
                pygame.draw.line(self, (82, 61, 53), origin.pos, child.pos, 3)
            else:
                pygame.draw.line(self, (189, 106, 98), origin.pos, child.pos, 3)

            self._render_edges(child)

    def _render_node(self, node: MapNode):
        sprite_id = 0

        sprite_id += node.type.value
        sprite_id += 3 * node.was_visited
        sprite_id += (6 * node.is_navigable)
        sprite_id += 3 * (node.is_navigable and node == self.hovered_node)

        sprite = self.node_sprites[sprite_id]
        w, h = sprite.get_size()
        self.blit(sprite, (node.pos[0] - (w >> 1), node.pos[1] - (h >> 1)))

    def _node_radius(self, node: MapNode):
        return 30 if node.type == MapNodeType.BOSS else 20


# ------------------------------------


node = MapNode((230, 300), MapNodeType.STORY, 1)

odyssey_map = MapNode((100, 450), MapNodeType.BATTLE, 2).to(
    MapNode((170, 360), MapNodeType.STORY, 3).to(
        MapNode((150, 260), MapNodeType.BATTLE, 4),
        node.to(
            MapNode((180, 190), MapNodeType.BATTLE, 5).to(
                MapNode((220, 70), MapNodeType.BOSS, 6)
            )
        )
    ),
    MapNode((210, 390), MapNodeType.BATTLE, 7).to(
        MapNode((260, 340), MapNodeType.STORY, 8).to(
            node
        )
    )
)
