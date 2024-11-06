""" Módulo responsável pelas mecânicas do mapa do jogo """


import pygame
from map_node import MapNode, MapNodeType, Point
import math
import random


SCROLL_SPEED = 7
MARGIN = 20


class MapScreen(pygame.Surface):
    def __init__(self, target: pygame.Surface, root: MapNode):
        self._load_sprites()
        pygame.Surface.__init__(self, self.map_sprite.get_size(), pygame.SRCALPHA)
        self.pos = pygame.math.Vector2(target.get_size())
        self.pos -= self.get_size()
        self.pos /= 2

        self.target = target
        
        self.root = root
        self.nodes = set([root])
        self._add_children(root)

        self.hovered_node = None
        self.current_node = root
        self.choosen_node = None
        root.activate()

        self.scrolling = False
        self.scroll_initial_y = 0

        self.scroll_interval = (self.pos.y * 2 - MARGIN, MARGIN)
        self._scroll_to(root)

        for node in self.nodes:
            self._bake_trail(node)

    def handle_event(self, ev: pygame.event.Event):
        if ev.type == pygame.MOUSEMOTION:
            self._mouse_motion(ev.dict["pos"])

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_down(ev.dict["pos"], ev.dict["button"])

        elif ev.type == pygame.MOUSEBUTTONUP:
            self._mouse_up(ev.dict["pos"], ev.dict["button"])

        elif ev.type == pygame.MOUSEWHEEL:
            self.hovered_node = None
            self.pos.y = pygame.math.clamp(
                self.pos.y + ev.dict["y"] * SCROLL_SPEED,
                self.scroll_interval[0],
                self.scroll_interval[1],
            )

    def get(self):
        node = self.choosen_node
        self.choosen_node = None
        if node != None:
            self._scroll_to(node)
            return node.data

    def render(self):
        self.blit(self.map_sprite, (0,0))

        for node in self.nodes:
            self._render_node(node)

        self.target.blit(self, self.pos)

    def _scroll_to(self, node: MapNode):
        self.pos.y = pygame.math.clamp(
            (self.target.get_height() * 3/4) - node.pos.y,
            self.scroll_interval[0],
            self.scroll_interval[1],
        )

    def _mouse_motion(self, mouse_pos: Point):
        if self.scrolling:
            self.pos.y = pygame.math.clamp(
                mouse_pos[1] - self.scroll_initial_y,
                self.scroll_interval[0],
                self.scroll_interval[1],
            )

        for node in self.nodes:
            if not node.is_navigable: continue
            
            diff = (node.pos - mouse_pos + self.pos).length()

            if (diff < self._node_radius(node)):
                self.hovered_node = node
                return

        self.hovered_node = None

    def _mouse_down(self, mouse_pos: Point, button: int):
        if button != 1: return
        
        if self.hovered_node != None:
            self.current_node.navigate_to(self.hovered_node)
            self._bake_trail(self.hovered_node)
            self._bake_trail(self.current_node)

            self.current_node = self.hovered_node
            self.choosen_node = self.hovered_node
            self.hovered_node = None

            return self.current_node.data
        else:
            self.scrolling = True
            self.scroll_initial_y = mouse_pos[1] - self.pos.y
            
            # # DEBUG: adiciona nó novo no clique
            # n = MapNode(-self.pos + mouse_pos, MapNodeType.STORY, None)
            # self.current_node.to(n)
            # self.current_node.navigate_to(n)
            # self._bake_trail(n)
            # self._bake_trail(self.current_node)
            # self.current_node = n
            # self.nodes.add(n)

        return None

    def _mouse_up(self, mouse_pos: Point, button: int):
        if button == 1:
            self.scrolling = False

    def _load_sprites(self):
        self.map_sprite = pygame.image.load("assests/map_bg.png").convert_alpha()

        ss = pygame.image.load("assests/map_icons.png").convert_alpha()
        self.node_sprites = [
            ss.subsurface((142, 0,  48, 48)), # nó de batalha inacessível
            ss.subsurface((142, 48, 48, 48)), # nó de história inacessível
            ss.subsurface((128, 96, 64, 64)), # nó de boss inacessível
            ss.subsurface((96,  0,  48, 48)), # nó ... já visitado
            ss.subsurface((96,  48, 48, 48)),
            ss.subsurface((0,   96, 64, 64)),
            ss.subsurface((0,   0,  48, 48)), # nó ... acessível
            ss.subsurface((0,   48, 48, 48)),
            ss.subsurface((0,   96, 64, 64)),
            ss.subsurface((48,  0,  48, 48)), # nó ... sendo selecionado
            ss.subsurface((48,  48, 48, 48)),
            ss.subsurface((64,  96, 64, 64)),
        ]

        self.trail_marks_sprite = pygame.image.load("assests/map_trail_marks.png").convert_alpha()

    def _add_children(self, node: MapNode):
        self.nodes.update(node.children)
        for child in node.children:
            self._add_children(child)

    def _bake_trail(self, origin: MapNode):
        for child in origin.children:
            diff_raw = child.pos - origin.pos
            diff_normal = diff_raw.normalize()

            start = origin.pos + diff_normal * self._node_radius(origin)
            end = child.pos - diff_normal * self._node_radius(child)

            diff = end - start

            distance = diff.length()
            angle_idx = math.floor(.5 - math.atan2(diff.y, diff.x) * 12 / math.pi)

            num_marks = math.floor(distance / 16)
            inc = diff / num_marks if num_marks != 0 else pygame.math.Vector2(0, 0)

            for i in range(num_marks + 1):
                x = (int(origin.pos.x) + i) % 4
                x += 4 * (child.is_navigable or child.was_visited)
                y = angle_idx % 6

                sprite = self.trail_marks_sprite.subsurface((x << 4, y << 4, 16, 16))

                if (angle_idx % 12) >= 6:
                    sprite = pygame.transform.rotate(sprite, 90)

                p = start + inc * i if num_marks > 0 else (start + end) / 2
                s = pygame.math.Vector2(sprite.get_size())
                self.map_sprite.blit(sprite, p - s / 2)

    def _render_node(self, node: MapNode):
        sprite_id = node.was_visited + \
                    (node.is_navigable << 1) + \
                    (node == self.hovered_node)

        sprite_id = len(MapNodeType) * sprite_id + node.type.value

        sprite = self.node_sprites[sprite_id]
        w, h = sprite.get_size()
        self.blit(sprite, node.pos - (w >> 1, h >> 1))

    def _node_radius(self, node: MapNode):
        return 32 if node.type == MapNodeType.BOSS else 20


# ------------------------------------


node = MapNode((230, 300), MapNodeType.STORY, 1)

odyssey_map = MapNode((100, 450), MapNodeType.STORY, 2).to(
    MapNode((170, 360), MapNodeType.STORY, 3).to(
        MapNode((150, 260), MapNodeType.BATTLE, 4),
        node.to(
            MapNode((180, 190), MapNodeType.BATTLE, 5).to(
                MapNode((200, 100), MapNodeType.BOSS, 6)
            )
        )
    ),
    MapNode((210, 390), MapNodeType.BATTLE, 7).to(
        MapNode((270, 340), MapNodeType.STORY, 8).to(
            node
        )
    )
)
