from pygame import Surface, draw, math
from enum import Enum
from typing import Self
from screen import Screen


Point = tuple[int, int]


class MapNodeType(Enum):
    FIREPLACE = 0
    STORY = 1
    BATTLE = 2
    BOSS = 3


class MapNode:
    """ Representa um único nó no mapa do jogo.
        
        Atributos:
            pos (tuple[int, int]): A posição do nó no mapa.
            type (MapNodeType): O tipo do nó, que define qual sprite será
                utilizado para renderizá-lo.
            is_navigable (bool): Define se atualmente é possível navegar até
                esse nó a partir do nó ativo.
            children (list[MapNode]): Os nós aos quais o atual se conecta, sem
                considerar os caminhos que chegam nele.
            screen (Screen): A tela que o jogo deve exibir quando o nó atual
                for selecionado pelo jogador.
            was_visited (bool): Indica se o jogador já passou pelo nó.
            is_active (bool): Indica se o jogador está no nó atual.
    """


    def __init__(self, pos: Point, type: MapNodeType, screen: Screen):
        """ Construtor da classe. """
        self.pos = math.Vector2(pos)
        self.children = []
        self.type = type
        self.screen = screen
        self.was_visited = False
        self.is_navigable = False
        self.is_active = False


    def add_children(self, *args: list[Self]):
        """ Na prática, cria arestas direcionadas indo do nó atual a todos
            passados em `args`. Gera um ValueError caso já exista uma aresta
            indo àquele nó.
            
            Parâmetros:
                args (list[Self]): A lista de nós para os quais devem ser
                    criados caminhos.
        """
        if any([v in self.children for v in args]):
            raise ValueError("Arestas paralelas não são permitidas")

        self.children += args


    def navigate_to(self, child: Self):
        """ Atualiza as propriedades dos nós para refletir a ação do jogador ter            
            "navegado" para `child`. Ou seja, `child` se torna o novo nó ativo e
            o nó atual tem seu estado resetado.

            Parâmetros:
                child (MapNode): o nó para o qual o jogador está navegando.
        """
        if child not in self.children:
            raise ValueError("Nó sendo visitado não é filho do anterior")

        child.activate()

        # Reseta o estado "ativo" do nó atual, mas mantendo `was_visited`
        self.is_active = False
        for c in self.children:
            c.is_navigable = False


    def activate(self):
        """ Torna o nó ativo, AKA, o nó em que o jogador está, e atualiza o
            grafo de acordo.
        """
        self.was_visited = True
        self.is_active = True
        for c in self.children:
            c.is_navigable = True
