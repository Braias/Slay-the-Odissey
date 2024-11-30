from abc import ABC, abstractmethod
from pathlib import Path
import pygame

class InsufficientEnergyError(Exception):
    def __init__(self, message="A energia atual não é suficiente para essa carta"):
        super().__init__(message)

class WrongTargetError(Exception):
    def __init__(self, message="A carta escolhida não pode ser aplicada no alvo selecionado"):
        super().__init__(message)

class Card(ABC):
    """
    Classe para todas as cartas a serem utilizadas nas batalhas do jogo

    Atributos
    ----------
    name : str
        Título específico da carta.
    description : str
        Descrição da carta, seus efeitos e funcionalidades.
    cost : int
        Custo energético da carta perante ao seu uso.
    type : str
        Tipo da Carta dentre os definidos: "Attack", "Defense", etc.
    """
    
    def __init__(self, name: str, description: str, cost: int, type: str):
        self._name = name
        self._description = description 
        self._cost = cost 
        self._type = type 
        
        game_dir = Path(__file__).parent.parent
        img_path = game_dir / "assets" / f"{name}.png"
        img = pygame.image.load(img_path)
        
        self.sprite = pygame.transform.scale(img,(150,150))
        self.rect = self.sprite.get_rect()
        self.x_pos = 100
        self.y_pos = 620
        self.rect.center = (self.x_pos,self.y_pos)
    
    @abstractmethod
    def check_target(owner, target): ...

    @abstractmethod
    def apply_card(self, owner, target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta.
        """ 
        owner.current_energy -= self._cost

class AttackCard(Card):
    """
    Classe Filha de Card, referente às cartas de Ataque, que diminuem HP do alvo.

    Atributos
    ----------
    name : str
        Título específico da carta.
    description : str
        Descrição da carta, seus efeitos e funcionalidades.
    cost : int
        Custo energético da carta perante ao seu uso.
    damage : int
        Valor de dimuição do HP do alvo.
    type : str, optional
        Tipo da Carta dentre os definidos: "Attack", "Defense", etc, por default "attack"
    """
    def __init__(self, name, description, cost, damage: int, type="attack"):
        super().__init__(name, description, cost, type)
        self._damage = damage

    def check_target(self, owner, target) -> bool:
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Parametros
        ----------

        """
        # esse card não pode ser aplicado em si mesmo
        if target == owner:
                return False
        else:
            return True

    def apply_card(self, owner, target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, diminui o HP do alvo escolhido. 
        """
        if self.check_target(owner,target):
            if target.defense - self._damage < 0:
                # Subtrai a diferença entre o dano e a defesa da vida atual do alvo
                target.current_life -= (self._damage - target.defense)
            else:
                target.defense -= self._damage
            super().apply_card(owner,target)
    

class DefenseCard(Card):
    def __init__(self, name, description, cost, defense: int, type="defense"):
        super().__init__(name, description, cost, type)
        self._defense = defense
     
    def check_target(self, target, owner) -> bool:
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Parametros 
        ----------

        """
        if target != owner:
            # esse card só pode ser aplicado em si mesmo
            return False
        else:
            return True

    def apply_card(self,owner,target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, aumenta a defesa do usuário. 
        """
        if self.check_target(owner,target):
            target.defense += self._defense
            super().apply_card(owner,target)
