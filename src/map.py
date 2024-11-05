""" Módulo responsável pelas mecânicas do mapa do jogo """


from pygame import Surface, draw, display, math
from map_node import MapNode, MapNodeType, Point


MAP_WIDTH = 400
MAP_HEIGHT = 600
SCROLL_SPEED = 2
MARGIN = 20

COLOR_MAP = (200, 200, 150)


class MapView(Surface): # TODO: implicações de herdar Surface
    def __init__(self, target: Surface, root: MapNode):
        self.size = (MAP_WIDTH, MAP_HEIGHT)
        self.pos = (
            (target.get_width() - self.size[0]) >> 1,
            (target.get_height() - self.size[1]) >> 1
        )

        Surface.__init__(self, (MAP_WIDTH, MAP_HEIGHT))
        self.target = target
        
        self.root = root
        self.nodes = set([root])
        self.hovered_node = None
        self._add_children(root)

        self.current_node = root
        root.visit()

        self.scrolling = False
        self.scroll_initial_y = 0

        self.scroll_interval = (target.get_height() - MAP_HEIGHT - MARGIN, MARGIN)
        self.focus_on(root)

    def mouse_motion(self, mouse_pos: Point):
        if self.scrolling:
            self.pos = (
                self.pos[0],
                math.clamp(
                    mouse_pos[1] - self.scroll_initial_y,
                    self.scroll_interval[0],
                    self.scroll_interval[1],
                )
            )

        for node in self.nodes:
            diff = (node.pos[0] - mouse_pos[0] + self.pos[0]) ** 2 + \
                   (node.pos[1] - mouse_pos[1] + self.pos[1]) ** 2

            if (diff < 400) and node.is_available:
                node.is_hovered = True
                self.hovered_node = node
                return

        # Aqui o mouse não está sobre nenhum nó
        
        if self.hovered_node != None:
            self.hovered_node.is_hovered = False

        self.hovered_node = None

    def mouse_down(self, mouse_pos: Point):
        if self.hovered_node != None and self.hovered_node.is_available:
            self.current_node.is_active = False
            self.current_node.is_available = False

            for child in self.current_node.children:
                child.is_available = False

            self.hovered_node.visit()
            self.current_node = self.hovered_node

            return self.current_node.data
        else:
            self.scrolling = True
            self.scroll_initial_y = mouse_pos[1] - self.pos[1]

        return None

    def mouse_up(self, mouse_pos: Point):
        self.scrolling = False
        
    def render(self):
        rect = self.get_bounding_rect()
        draw.rect(self, COLOR_MAP, rect)

        self._render_edges(self.root)

        for node in self.nodes:
            node.render(self)

        self.target.blit(self, (self.pos[0], self.pos[1]))

    def focus_on(self, node: MapNode):
        self.pos = (
            self.pos[0],
            math.clamp(
                (self.target.get_height() * 3/4) - node.pos[1],
                self.scroll_interval[0],
                self.scroll_interval[1],
            )
        )

    def _add_children(self, node: MapNode):
        self.nodes.update(node.children)
        for child in node.children:
            self._add_children(child)

    def _render_edges(self, origin: MapNode):
        for child in origin.children:
            if (child.was_visited or child.is_available) and origin.was_visited:
                draw.line(self, (100, 100, 60), origin.pos, child.pos, 4)
            else:
                draw.line(self, (150, 150, 110), origin.pos, child.pos, 4)

            self._render_edges(child)


# ------------------------------------


node = MapNode((230, 400), MapNodeType.STORY, None)

odyssey_map = MapNode((200, 540), MapNodeType.BATTLE, None).to(
    MapNode((170, 460), MapNodeType.STORY, None).to(
        MapNode((150, 360), MapNodeType.BATTLE, None),
        node.to(
            MapNode((180, 290), MapNodeType.BATTLE, None).to(
                MapNode((220, 170), MapNodeType.BOSS, None)
            )
        )
    ),
    MapNode((210, 490), MapNodeType.BATTLE, None).to(
        MapNode((260, 440), MapNodeType.STORY, None).to(
            node
        )
    )
)
