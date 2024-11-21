from pathlib import Path
import pygame
from entities import Enemy,Ulisses,AnimationState
import time
class CombatLevel:
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
    def __init__(self,screen:pygame.display,background_name:str,staged_enemies:list):
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
            
            self.game_state = 0
            self.screen = screen
            self.staged_enemies = staged_enemies
            self.instantiated_enemies = []
            self.is_player_turn = True
        except FileNotFoundError as error:
            print(f"{error}: background assest not found in 'assets")

    def draw_level(self,ulisses:Ulisses):
        """Método responsável por desenhar todo cenario e inimigos do estágio
        """
        self.screen.blit(self.background_img,(0,0))
        pygame.draw.rect(self.screen,color='brown',rect=pygame.Rect(0, 540,800,160))
        self.instantiate_enemies()
        self.draw_enemies()
        ulisses.draw_entity(self.screen)
        if self.is_player_turn:
            ulisses.deck.draw_hand_on_screen(self.screen)

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
                self.instantiated_enemies[enemy_index].x_pos -= 150*enemy_index
                self.instantiated_enemies[enemy_index].origin_x -= 150*enemy_index
    
    def execute_enemy_combat_loop(self,ulisses:Ulisses):
        for each_enemy in self.instantiated_enemies:
            has_played = self.execute_enemy_turn(each_enemy,ulisses)
            if has_played:
                break
            else:
                self.end_enemies_turn(ulisses)

    def execute_enemy_turn(self,enemy:Enemy,target:Ulisses) -> bool:
        enemy_turn_played = False
        if enemy.check_is_alive() and enemy.current_energy > 0 and len(enemy.deck.hand) > 0:
            #Selecionamos smepre a primeira carta do baralho
            enemy.deck.selected_card = enemy.deck.hand[0]
            if enemy.deck.selected_card._type == 'attack':
                enemy.deck.selected_card.apply_card(enemy,target)
            elif enemy.deck.selected_card._type == 'defense':
                enemy.deck.selected_card.apply_card(enemy,enemy)
            # Caso o inimgo nao tenha energia para jogar a carta atual ainda queremos 
            # olhar proximas cartas, assim descartamos a carta atual e prosseguimos
            if enemy.deck.selected_card in enemy.deck.hand:
                enemy.deck.discard_card(enemy.deck.selected_card)
            enemy_turn_played = True
        return enemy_turn_played

    def player_combat_loop(self,ulisses:Ulisses,mouse_pos:tuple):
        if ulisses.check_is_alive():
            if ulisses.deck.selected_card:
                if ulisses.rect.collidepoint(mouse_pos):
                    ulisses.deck.selected_card.apply_card(ulisses,ulisses)
                for enemy in self.instantiated_enemies:
                    if enemy.rect.collidepoint(mouse_pos) and enemy.check_is_alive():
                        ulisses.deck.selected_card.apply_card(ulisses,enemy) 
            for each_card in ulisses.deck.hand:
                if each_card.rect.collidepoint(mouse_pos):
                    if each_card == ulisses.deck.selected_card:
                        ulisses.deck.selected_card = None
                    else:
                        ulisses.deck.selected_card = each_card  

    def end_player_turn(self,ulisses:Ulisses):
        for each_enemy in self.instantiated_enemies:
            each_enemy.current_defense = 0
            each_enemy.deck.shuffle_and_allocate()
            each_enemy.apply_offensive_effects()
            each_enemy.apply_defensive_effects()
        ulisses.current_energy = ulisses.max_energy
        ulisses.deck.shuffle_and_allocate()
        ulisses.clear_multipliers()
        self.is_player_turn = False


    def end_enemies_turn(self,ulisses:Ulisses):
        ulisses.current_defense = 0 
        ulisses.apply_offensive_effects()
        ulisses.apply_defensive_effects()
        for each_enemy in self.instantiated_enemies:
            each_enemy.current_energy = each_enemy.max_energy
        self.is_player_turn = True  

    def check_enemy_animating(self) -> bool:
        for each_enemy in self.instantiated_enemies:
            if each_enemy.animation_state != AnimationState.REST:
                return True
        return False
    
    def handle_event(self,event:pygame.event.Event,ulisses:Ulisses):
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_mouse_pos = pygame.mouse.get_pos()
            if self.is_player_turn:
                self.player_combat_loop(ulisses,current_mouse_pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.end_player_turn(ulisses)
            elif event.key == pygame.K_a:
                ulisses.attack_animate()

    def run_animations(self,ulisses:Ulisses):
        if ulisses.animation_state == AnimationState.ATTACK or ulisses.animation_state == AnimationState.RETREAT:
            ulisses.attack_animate(invert_direction=False)
        elif ulisses.animation_state == AnimationState.SHAKE:
            ulisses.hit_animate()
        for each_enemy in self.instantiated_enemies:
            if each_enemy.animation_state == AnimationState.ATTACK or each_enemy.animation_state == AnimationState.RETREAT:
                each_enemy.attack_animate(invert_direction=True)
            elif each_enemy.animation_state == AnimationState.SHAKE:
                each_enemy.hit_animate()

    def update(self,ulisses:Ulisses):
        all_entities = [ulisses] + self.instantiated_enemies
        for each_entity in all_entities:
            if not each_entity.check_is_alive():
                each_entity.death_animate()
        if not self.is_player_turn and not self.check_enemy_animating():
            self.execute_enemy_combat_loop(ulisses)
        self.run_animations(ulisses)

