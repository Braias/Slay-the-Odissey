from abc import abstractmethod, ABC
from typing import Self, Optional
from pygame.event import Event


class Screen(ABC):
    """ Representa uma tela do jogo, como um menu principal ou uma tela de
        combate. Durante o jogo, apenas uma tela será exibida de cada vez e
        seus métodos serão chamados automaticamente pelo loop principal.
    """


    @abstractmethod
    def handle_event(self, event: Event):
        """ Método que lida com todos os eventos do jogo. A função é chamada
            uma vez para cada evento ocorrido enquanto a tela estiver visível,
            até o início da transição de troca de telas. Eventos ocorridos
            durante a transição de entrada serão adiados para o primeiro frame
            após seu fim.
        """
        ...


    @abstractmethod
    def update(self) -> Optional[Self]:
        """ Método chamado uma vez a cada frame (enquanto a tela estiver
            visível e não esteja ocorrendo uma transição) e responsável pelas
            atualizações gerais da tela, não incluindo renderização.
            Implementações deste método devem retornar dele a próxima tela a
            ser exibida ou `None` caso não seja o momento de trocar de tela; o
            loop principal do jogo lida com a transição e faz essa troca
            automaticamente.
        """
        ...


    @abstractmethod
    def draw(self):
        """ Método chamado uma vez a cada frame (enquanto a tela estiver
            visível, incluindo durante as transições) e responsável pela
            renderização da tela.
        """
        ...


    def onenter(self):
        """ Método chamado toda vez que o jogo transicionar para a tela,
            exatamente na metade da animação da transição, quando a tela estiver
            totalmente preta.
        """
        pass
