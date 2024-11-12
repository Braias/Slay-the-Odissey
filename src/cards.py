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
    
    def check_energy(self, owner):
        """
        Checagem da possibilidade do uso da carta, baseado na disponibilidade de energia no usuário da carta e no custo energético desta.  

        Levanta
        ------
        InsufficientEnergyError
            Se o custo é maior que a energia disponível pelo usuário, impede o uso da carta.
        """
        try:
            if owner.current_energy < self._cost:
                raise InsufficientEnergyError
        except:
            if owner.__class__.__name__ == "Enemy":
                # TODO lógica para a ação de jogar dos inimigos (passar pra próxima carta caso não tenha energia)
                print("Ei, inimigo")
            else:
                # TODO lógica para ação do jogador (não conseguir selecionar a carta se não tiver energia e passar para resseleção)
                print("Ei, Ulisses")                           

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

    def check_target(self, owner, target):
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Levanta
        ------
        WrongTargetError
            Na Carta Ataque, impede o usuário de utilizar um ataque em si mesmo.
        """
        try:
            if target == owner:
                raise WrongTargetError  # esse card não pode ser aplicado em si mesmo
        except:
            # TODO tratamento certo pra esse erro
            print("Essa carta não pode ser aplicada em si mesmo")

    def apply_card(self, owner, target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, diminui o HP do alvo escolhido. 
        """
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
     
    def check_target(self, target, owner):
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Levanta
        ------
        WrongTargetError
            Na Carta Defesa, impede o usuário de utilizar defesa em um inimigo.
        """
        try:
            if target != owner:
                raise WrongTargetError  # esse card só pode ser aplicado em si mesmo
        except:
            # TODO tratamento certo pra esse erro
            print("Essa carta não pode ser aplicada em um inimigo")

    def apply_card(self,owner,target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, aumenta a defesa do usuário. 
        """
        target.defense += self._defense
        super().apply_card(owner,target)
