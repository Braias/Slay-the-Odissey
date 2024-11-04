from abc import ABC, abstractmethod
import entities

class Card(ABC):
    """
    Classe para todas as cartas a serem utilizadas nas batalhas do jogo.

    Parâmetros
    ----------
    ABC :
        Classe Mãe de Card. Define a existência de classes abstratas na Mãe, permitindo a criação de conteúdo específico para classe Filho.
    """
    def __init__(self, name: str, 
                 description: str, 
                 cost: int,
                 type: str,
                 card_user: entities.Entity, 
                 target: entities.Entity,
                 effect = None,):
        """
        Inicializa a classe Card.

        Parâmetros
        ----------
        name : str
            Título específico da carta.
        description : str
            Descrição da carta, seus efeitos e funcionalidades.
        cost : int
            Custo energético da carta perante ao seu uso.
        type : str
            Tipo da Carta dentre os definidos: "Attack", "Defense", etc.
        card_user : entities.Entity
            Usuário da Carta em questão.
        target : entities.Entity
            Entidade nas quais serão aplicadas os efeitos e funcionalidades da carta.
        effect : str, optional
            Consequência secundária do uso da carta, default None.
        """
        self._name = name
        self._description = description
        self._cost = cost
        self._type = type
        self._effect = effect
        self._card_user = card_user
        self._target = target
    
    def check_energy(self):
        """
        Checagem da possibilidade do uso da carta, baseado na disponibilidade de energia no usuário da carta e no custo energético desta.  

        Levanta
        ------
        ValueError
            Se o custo é maior que a energia disponível pelo usuário, impede o uso da carta.
        """
        try:
            if self._card_user.energy < self._cost:
                raise ValueError
        except:
            if self._card_user.__class__ == entities.Enemy:
                # lógica para a ação de jogar dos inimigos (passar pra próxima carta caso não tenha energia)
                pass
            else:
                # lógica para ação do jogador (não conseguir selecionar a carta se não tiver energia e passar para resseleção)
                pass                           

    @property
    @abstractmethod
    def apply_card(): ...

    @abstractmethod
    def check_target(): ...

class AttackCard(Card):
    """
    Classe Filha de Card, referente às cartas de Ataque, que diminuem HP do alvo.

    Parâmetros
    ----------
    Card
        Classe Mãe de AttackCard.
    """
    def __init__(self, 
                 name, 
                 description, 
                 cost, 
                 target, 
                 card_user, 
                 effect, 
                 damage: int, 
                 type="attack"):
        """
        Inicia a classe AttackCard.

        Parâmetros
        ----------
        name : str
            Título específico da carta.
        description : str
            Descrição da carta, seus efeitos e funcionalidades.
        cost : int
            Custo energético da carta perante ao seu uso.
        card_user : entities.Entity
            Usuário da Carta em questão.
        target : entities.Entity
            Entidade nas quais serão aplicadas os efeitos e funcionalidades da carta.
        effect : str, optional
            Consequência secundária do uso da carta, default None.
        damage : int
            Valor de dimuição do HP do alvo.
        type : str, optional
            Tipo da Carta dentre os definidos: "Attack", "Defense", etc, por default "attack"
        """
        super().__init__(name, description, cost, target, card_user, type, effect)
        self._damage = damage

    @property        
    def apply_card(self):
        self._card_user.energy -= self._cost
        self._target.current_life -= self._damage
    
    def check_target(self):
        try:
            if self._target == self._card_user:
                raise KeyError  # esse card não pode ser aplicado em si mesmo
            #TODO criar classe de erros específicos de aplicação de cartas
        except:
            pass

class DefenseCard(Card):
    def __init__(self, name, description, cost, target, card_user, defense: int, type="defense", effect=None):
        super().__init__(name, description, cost, target, card_user, type, effect)
        self._defense = defense
     
    @property        
    def apply_card(self):
        self._card_user.energy -= self._cost
        self._target.defense += self._defense

    def check_target(self):
        try:
            if self._target != self._card_user:
                raise KeyError  # esse card só pode ser aplicado em si mesmo
            #TODO criar classe de erros específicos de aplicação de cartas
        except:
            pass
