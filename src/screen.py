from abc import abstractmethod, ABC
from typing import Self, Optional
from pygame.event import Event


class Screen(ABC):
    """
    Representa uma tela do jogo, como um menu principal ou uma tela de combate.
    Durante o jogo, apenas uma tela será exibida de cada vez e seus métodos
    serão chamados automaticamente pelo loop principal.
    """

    @abstractmethod
    def handle_event(self, event: Event):
        ...

    @abstractmethod
    def update(self) -> Optional[Self]:
        ...

    @abstractmethod
    def draw(self):
        ...

    def onenter(self):
        pass
