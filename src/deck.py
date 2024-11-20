import random
from pathlib import Path
import cards
import json
import pygame


game_dir = Path(__file__).parent.parent
cards_json_path = game_dir / "assets" / "cards.json"

# Carregando json de configuracoes para construir cartas
with open(file=cards_json_path,mode='r') as card_config:
    default_card_configurations = json.load(card_config)

class Deck:
    """
    Classe que estrutura baralhos de toda entidade

    Atributos
    ---------
        hand : list
            Coleção de cartas atualmente disponiveis para serem jogadas no round de combate
        draw_pile : list
            Coleção de cartas disponiveis para serem usados em próximos rounds de comabte 
        discrad_pile : list
            Coleção de cartas usadas durante os rounds de comabte - podem ser feitas disponiveis 
            caso o draw_pile ficar pequeno o suficiente
        exhaust_pile : list
            Coleção de cartas que estao indisponiveis pelo nivel de jogo
        owner : Entity
            variavel da classe Entidade que indica de quem pertence o baralho - usado 
            para checar a aplicação de cartas
    """
    def __init__(self,draw_pile_ids=[]):
        self.hand = []
        self.draw_pile= self.build_draw_pile(draw_pile_ids)
        self.discard_pile = []
        self.exhaust_pile =[]
        self.owner = None
        self.selected_card = None

    def __str__(self):
        """Metodo responsavel pela representacao em string do deck

        Retorna:
            str: lista ed nomes de cartas na mao atual e descarte
        """
        hand_names = []
        discard_pile_names = []
        for each_card in self.hand:
            hand_names.append(each_card._name)
        for each_card in self.discard_pile:
            discard_pile_names.append(each_card._name)
        return f"hand:{hand_names}\ndiscard pile:{discard_pile_names}"
    
    def shuffle_and_allocate(self):
        """Metodo responsavel pelo embaralhamento do 'draw_pile' e alocacao da mao 
        atual do jogador no inicio de cada round d combate
        """
        # limpar mao atual e mover para pilha de descarte
        self.discard_card(*self.hand)    
        self.selected_card = None
        # Checamos quantas cartas estão disponíveis
        cards_to_draw = len(self.draw_pile) 
        # Caso não temos cartas suficentes para formar uma mão adcionamos do deck de descarte
        if cards_to_draw < 5: 
            self.draw_pile+=self.discard_pile
            self.discard_pile = []
        # Embaralhamos o deck e removemos as primeiras 5 cartas
        random.shuffle(self.draw_pile)
        next_hand = self.draw_pile[:5]
        del(self.draw_pile[:5])
        # posicionamos as cartas no display e consturimos nossa mao
        for card_index,card in enumerate(next_hand):
            card.x_pos = 100+150*card_index
        self.hand = next_hand
    
    def build_draw_pile(self,draw_pile_ids:list):
        """Metodo responsavel por consultar arquivo de configuracao e instanciar
        novas cartas no 'draw_pile'

        Args:
            draw_pile_ids (list): lista de nomes de cartas a serem instanciadas

        Retorna:
            list: lista de objetos do tipo Card - baralho disponivel do jogador
        """
        draw_pile = []
        # iteramos sobre cada identificador de cada carta no baralho 
        # para depois busacar no arquivo de configuracao
        for card_id in draw_pile_ids: 
            card_info = default_card_configurations['cards'][card_id]
            card_type = card_info['type']
            if card_type == 'attack':
                draw_pile.append(cards.AttackCard(card_id,
                                                  card_info['cost'],card_info['damage'],
                                                  card_type))
            elif card_type == 'defense':
                draw_pile.append(cards.DefenseCard(card_id,
                                                   card_info['cost'],card_info['defense'],
                                                   card_type))
            elif card_type == "effect":
                draw_pile.append(cards.EffectCard(card_id, card_info['cost'],card_info['poison'], card_type))
        return draw_pile
    
    def draw_hand_on_screen(self,screen:pygame.display):
        """metodo atualiza centro de cartas na mao do jogador e desenha na tela 

        Args:
            screen (pygame.display): janela atual de jogo
        """
        for card in self.hand:
            if card == self.selected_card:
                card.rect.center=(card.x_pos,card.y_pos-30)
            else:
                card.rect.center=(card.x_pos,card.y_pos)
            screen.blit(card.sprite,card.rect)

    def set_owner(self,owner):
        """Define owner de baralho do jogador
        
        Args:
            owner (Entity): variavel da classe Entidade que indica de quem pertence o baralho
        """
        self.owner = owner

    def discard_card(self,*args:cards.Card):
        """Metodo remove carta de mao atual do jogador e adciona a pilha de descarte
        """
        for each_card in args:
            self.hand.remove(each_card)
            self.discard_pile.append(each_card)
