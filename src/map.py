""" Módulo responsável pelas mecânicas do mapa do jogo """


from pygame import Surface, draw, display, math, image
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
        root.begin()

        self.scrolling = False
        self.scroll_initial_y = 0

        self.scroll_interval = (target.get_height() - MAP_HEIGHT - MARGIN, MARGIN)
        self.focus_on(root)

        self.spritesheet = image.load("assests/map_icons.png")

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
            if not node.is_navigable: continue
            
            diff = (node.pos[0] - mouse_pos[0] + self.pos[0]) ** 2 + \
                   (node.pos[1] - mouse_pos[1] + self.pos[1]) ** 2

            if (diff < 400):
                self.hovered_node = node
                return

        # Aqui o mouse não está sobre nenhum nó
        
        self.hovered_node = None

    def mouse_down(self, mouse_pos: Point):
        if self.hovered_node != None and self.hovered_node.is_navigable:
            self.current_node.navigate_to(self.hovered_node)
            self.current_node = self.hovered_node
            self.hovered_node = None

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
            self._render_node(node)

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
            if (child.was_visited or child.is_navigable) and origin.was_visited:
                draw.line(self, (100, 100, 60), origin.pos, child.pos, 4)
            else:
                draw.line(self, (150, 150, 110), origin.pos, child.pos, 4)

            self._render_edges(child)

    def _render_node(self, node: MapNode):
        color = (100, 100, 100)
        if node.was_visited or node.is_navigable:
            color = (0, 0, 0)

        size = 10 if node.is_navigable else 6

        if node.type == MapNodeType.BATTLE:
            draw.circle(self, color, node.pos, size)
        elif node.type == MapNodeType.STORY:
            draw.rect(self, color, (
                node.pos[0] - size, node.pos[1] - size,
                size << 1, size << 1
            ))
        elif node.type == MapNodeType.BOSS:
            draw.circle(self, color, node.pos, size * 3)

        if node == self.hovered_node: # overlay
            draw.circle(self, (140, 140, 100), node.pos, size + 16, width = 4)
        


# ------------------------------------


node = MapNode((230, 400), MapNodeType.STORY, 1)

odyssey_map = MapNode((200, 540), MapNodeType.BATTLE, 2).to(
    MapNode((170, 460), MapNodeType.STORY, 3).to(
        MapNode((150, 360), MapNodeType.BATTLE, 4),
        node.to(
            MapNode((180, 290), MapNodeType.BATTLE, 5).to(
                MapNode((220, 170), MapNodeType.BOSS, 6)
            )
        )
    ),
    MapNode((210, 490), MapNodeType.BATTLE, 7).to(
        MapNode((260, 440), MapNodeType.STORY, 8).to(
            node
        )
    )
)
