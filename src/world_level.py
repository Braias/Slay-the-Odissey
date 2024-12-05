from pathlib import Path
import pygame
from entities import Enemy,Ulisses,AnimationState
import random
from screen import Screen
import json

game_dir = Path(__file__).parent.parent
cards_json_path = game_dir / "assets" / "cards.json"

# Carregando json de configuracoes para construir cartas
with open(file=cards_json_path,mode='r') as card_config:
    default_card_configurations = json.load(card_config)

class CombatLevel(Screen):
    """
    Classe para gerenciar um nível de combate em um jogo.

    CombatLevel configura o cenário em cada estágio que involve combate entre Ulisses e inimigos
    
    Atributos:
        screen (pygame.display): Tela onde o nível será desenhado
        background_img (pygame.Surface): Imagem de fundo do nível
        game_state (int): Estado atual do nível, representando o estágio do combate
        stages (tuple): Conjunto de estágios contendo os nomes dos inimigos para cada estágio
        staged_enemies (list): Lista de nomes de inimigos para o estágio atual
        instantiated_enemies (list): Lista de instâncias de inimigos criados para o estágio atual
    """
    def __init__(self,screen:pygame.display,background_name:str,staged_enemies:list, ulisses:Ulisses, next_screen: Screen):
        """Método inicializa objetos da classe CombatLevel

        Parâmetros:
            screen (pygame.display): Tela onde o nível será desenhado
            background_name (str): Nome da imagem de fundo que esta armazenado em assets
            stages (tuple): tupla de listas contendo os tipos de inimigo do estágio (ex:stages=(['Fairy','Fairy']) -- estágio com duas fadas inimigas)
        """
        try:
            game_dir = Path(__file__).parent.parent
            background_img_path = game_dir / "assets" / f"{background_name}.png"
            self.background_img = pygame.image.load(background_img_path)
            
            self.ulisses = ulisses
            self.game_state = 0
            self.screen = screen
            self.staged_enemies = staged_enemies
            self.instantiated_enemies = []
            self.is_player_turn = True
            self.next_screen = next_screen
        except FileNotFoundError as error:
            print(f"{error}: background asset not found in 'assets")

    def draw(self):
        """Método responsável por desenhar todo cenario e inimigos do estágio
        """
        self.screen.blit(self.background_img,((self.screen.get_width() - self.background_img.get_width()) >> 1,-40))
        self.instantiate_enemies()
        self.draw_enemies()
        self.ulisses.draw_entity(self.screen)
        if self.is_player_turn:
            self.ulisses.deck.draw_hand_on_screen(self.screen)

    def draw_enemies(self):
        """Método responsável por desenhar inimigos na tela do jogador 
        """
        for instantiated_enemy in self.instantiated_enemies:
            instantiated_enemy.draw_entity(screen=self.screen)

    def instantiate_enemies(self):
        """Método responsável por instanciar todos inimigos do estágio caso não existam
        """
        num_staged_enemies = len(self.staged_enemies)
        num_instantiated_enemies = len(self.instantiated_enemies)
        if num_staged_enemies != num_instantiated_enemies:
            for enemy_index,staged_enemy in enumerate(self.staged_enemies):
                self.instantiated_enemies.append(Enemy(name=staged_enemy))
                self.instantiated_enemies[enemy_index].x_pos -= 75 * enemy_index
                self.instantiated_enemies[enemy_index].origin_x -= 75 * enemy_index
    
    def execute_enemy_combat_loop(self,):
        for each_enemy in self.instantiated_enemies:
            has_played = self.execute_enemy_turn(each_enemy)
            if has_played:
                break
            else:
                self.end_enemies_turn()

    def execute_enemy_turn(self,enemy:Enemy) -> bool:
        target = self.ulisses
        enemy_turn_played = False
        if enemy.check_is_alive() and enemy.current_energy > 0 and len(enemy.deck.hand) > 0:
            #Selecionamos smepre a primeira carta do baralho
            enemy.deck.selected_card = enemy.deck.hand[0]
            if enemy.deck.selected_card._type == 'attack': enemy.deck.selected_card.apply_card(enemy,target)
            elif enemy.deck.selected_card._type == 'defense':
                enemy.deck.selected_card.apply_card(enemy,enemy)
            # Caso o inimgo nao tenha energia para jogar a carta atual ainda queremos 
            # olhar proximas cartas, assim descartamos a carta atual e prosseguimos
            if enemy.deck.selected_card in enemy.deck.hand:
                enemy.deck.discard_card(enemy.deck.selected_card)
            enemy_turn_played = True
        return enemy_turn_played

    def player_combat_loop(self,mouse_pos:tuple):
        if self.ulisses.check_is_alive():
            if self.ulisses.deck.selected_card:
                if self.ulisses.rect.collidepoint(mouse_pos):
                    self.ulisses.deck.selected_card.apply_card(self.ulisses,self.ulisses)
                for enemy in self.instantiated_enemies:
                    if enemy.rect.collidepoint(mouse_pos) and enemy.check_is_alive():
                        self.ulisses.deck.selected_card.apply_card(self.ulisses,enemy) 
            for each_card in self.ulisses.deck.hand:
                if each_card.rect.collidepoint(mouse_pos):
                    if each_card == self.ulisses.deck.selected_card:
                        self.ulisses.deck.selected_card = None
                    else:
                        self.ulisses.deck.selected_card = each_card  

    def end_player_turn(self,):
        for each_enemy in self.instantiated_enemies:
            each_enemy.current_defense = 0
            each_enemy.deck.shuffle_and_allocate()
            each_enemy.apply_offensive_effects()
            each_enemy.apply_defensive_effects()
        self.ulisses.current_energy = self.ulisses.max_energy
        self.ulisses.deck.shuffle_and_allocate()
        self.ulisses.clear_multipliers()
        self.is_player_turn = False


    def end_enemies_turn(self,):
        self.ulisses.current_defense = 0 
        self.ulisses.apply_offensive_effects()
        self.ulisses.apply_defensive_effects()
        for each_enemy in self.instantiated_enemies:
            each_enemy.current_energy = each_enemy.max_energy
        self.is_player_turn = True  

    def check_enemy_animating(self) -> bool:
        for each_enemy in self.instantiated_enemies:
            if each_enemy.animation_state != AnimationState.REST:
                return True
        return False
    
    def handle_event(self,event:pygame.event.Event,):
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = event.dict["pos"]
            if self.is_player_turn:
                self.player_combat_loop(current_mouse_pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.end_player_turn()
            elif event.key == pygame.K_a:
                self.ulisses.attack_animate()

    def run_animations(self,):
        if self.ulisses.animation_state == AnimationState.ATTACK or self.ulisses.animation_state == AnimationState.RETREAT:
            self.ulisses.attack_animate(invert_direction=False)
        elif self.ulisses.animation_state == AnimationState.SHAKE:
            self.ulisses.hit_animate()
        for each_enemy in self.instantiated_enemies:
            if each_enemy.animation_state == AnimationState.ATTACK or each_enemy.animation_state == AnimationState.RETREAT:
                each_enemy.attack_animate(invert_direction=True)
            elif each_enemy.animation_state == AnimationState.SHAKE:
                each_enemy.hit_animate()

    def check_win(self):
        enemy_is_dead = []
        for each_enemy in self.instantiated_enemies:
            enemy_is_dead.append(not each_enemy.check_is_alive())
        return all(enemy_is_dead)
    
    def onenter(self):
        self.ulisses.deck.shuffle_and_allocate()
        self.ulisses.damage_multiplier = 1
        self.ulisses.absorption_multiplier = 1
        self.ulisses.current_defense = 0
        self.ulisses.current_energy = self.ulisses.max_energy
        
    def update(self):
        all_entities = [self.ulisses] + self.instantiated_enemies
        for each_entity in all_entities:
            if not each_entity.check_is_alive():
                each_entity.death_animate()
        if not self.is_player_turn and not self.check_enemy_animating():
            self.execute_enemy_combat_loop()
        self.run_animations()
        if self.check_win():
            return self.next_screen

class RewardScreen(Screen):
    def __init__(self,surface:pygame.surface,ulisses:Ulisses,next_screen:Screen):
        self.ulisses = ulisses 
        self.next_screen = next_screen
        self.surface = surface
        self.reward_name = "---DEFAULT----"
        self.reward = None
        self.screen_ended = False


    def randomize_reward(self):
        reward_cards = list(default_card_configurations['cards'].keys())
        reward_id = random.choice(reward_cards)
        self.reward_name = reward_id.replace("_"," ")
        return reward_id
    
    def onenter(self):
        try:
            self.reward = self.ulisses.deck.add_single_card(self.randomize_reward())
        except FileNotFoundError as error:
            print(f"{error}: Assest for rewarded card unavailable")
        finally:
            surface_size = pygame.Vector2(self.surface.get_size())
            font = pygame.font.SysFont("Times New Roman", 16)
            self.text_surface = font.render(f"""Você Ganhou {self.reward_name} -- 'E' para voltar ao mapa""", False, (255,255,255))
            self.text_pos = (surface_size + (-self.text_surface.get_width(), 100)) / 2

    def draw(self):
        if self.reward:
            self.reward.rect.center = self.surface.get_rect().center
            self.surface.blit(self.reward.sprite,self.reward.rect)
            self.surface.blit(self.text_surface, dest=self.text_pos)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.screen_ended = True

    def update(self):
        if self.screen_ended:
            return self.next_screen
