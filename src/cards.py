from abc import ABC, abstractmethod
import pygame
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

        img = pygame.image.load(f'./assets/{name}.png')
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
        ValueError
            Se o custo é maior que a energia disponível pelo usuário, impede o uso da carta.
        """
        try:
            if owner.current_energy < self._cost:
                raise ValueError
        except:
            if owner.__class__.__name__ == "Enemy":
                # lógica para a ação de jogar dos inimigos (passar pra próxima carta caso não tenha energia)
                pass
            else:
                # lógica para ação do jogador (não conseguir selecionar a carta se não tiver energia e passar para resseleção)
                pass                           

    @property
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

    @property        
    def check_target(target, owner):
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Levanta
        ------
        KeyError
            Na Carta Ataque, impede o usuário de utilizar um ataque em si mesmo.
        """
        try:
            if target == owner:
                raise KeyError  # esse card não pode ser aplicado em si mesmo
            #TODO criar classe de erros específicos de aplicação de cartas
        except:
            pass

    def apply_card(self,owner,target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, diminui o HP do alvo escolhido. 
        """
        if target.defense - self._damage < 0:
            target.defense = 0
            # Subtrai a diferença entre o dano e a defesa da vida atual do alvo
            target.current_life -= (self._damage - target.defense)
        else:
           target.defense -= self._damage
        super().apply_card(owner,target)
    

class DefenseCard(Card):
    def __init__(self, name, description, cost, defense: int, type="defense"):
        super().__init__(name, description, cost, type)
        self._defense = defense
     
    @property      
    def check_target(target, owner):
        """
        Checa a aplicabilidade da carta no alvo escolhido.

        Levanta
        ------
        KeyError
            Na Carta Defesa, impede o usuário de utilizar defesa em um inimigo.
        """
        try:
            if target != owner:
                raise KeyError  # esse card só pode ser aplicado em si mesmo
            #TODO criar classe de erros específicos de aplicação de cartas
        except:
            pass

    def apply_card(self,owner,target):
        """
        Aplica as funcionalidades da carta no alvo escolhido e cobra o custo da carta. Aqui, aumenta a defesa do usuário. 
        """
        target.defense += self._defense
        super().apply_card(owner,target)
