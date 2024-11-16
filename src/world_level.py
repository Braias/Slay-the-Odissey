from pathlib import Path
import pygame
from entities import Enemy,Ulisses
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
            if instantiated_enemy.is_alive:
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

    def execute_enemy_combat_loop(self,target:Ulisses):
        """Metodo responsavel pelo ataque automatico de inimigos no jogo

        Args:
            target (Ulisses): alvo prinicpal de todo inimigo smepre sera o protagonista
        """
        for each_enemy in self.instantiated_enemies:
            # No inicio de cada rodada usamos o shuffle and allcoate 
            # Isso limpa a mao antiga do inimigo e aleatoriamente aloca um anova
            each_enemy.deck.shuffle_and_allocate() 
            # Enquanto o Inimigo tiver energia e Nao tiver exausto seu deck inteiro lutamos
            while each_enemy.current_energy > 0 and len(each_enemy.deck.hand) > 0 and each_enemy.is_alive:
                # Selecionamos smepre a primeira carta do baralho
                each_enemy.deck.selected_card = each_enemy.deck.hand[0]
                if each_enemy.deck.selected_card._type == 'attack':
                    each_enemy.deck.selected_card.apply_card(each_enemy,target)
                elif each_enemy.deck.selected_card._type == 'defense':
                    each_enemy.deck.selected_card.apply_card(each_enemy,each_enemy)
                # Caso o inimgo nao tenha energia para jogar a carta atual ainda queremos 
                # olhar proximas cartas, assim descartamos a carta atual e prosseguimos
                if each_enemy.deck.selected_card in each_enemy.deck.hand:
                    each_enemy.deck.discard_card(each_enemy.deck.selected_card)


    def player_combat_loop(self,ulisses:Ulisses,mouse_pos:tuple):
        if ulisses.is_alive:
            if ulisses.deck.selected_card:
                if ulisses.rect.collidepoint(mouse_pos):
                    ulisses.deck.selected_card.apply_card(ulisses,ulisses)
                for enemy in self.instantiated_enemies:
                    if enemy.rect.collidepoint(mouse_pos) and enemy.is_alive:
                        ulisses.deck.selected_card.apply_card(ulisses,enemy) 
            for each_card in ulisses.deck.hand:
                if each_card.rect.collidepoint(mouse_pos):
                    if each_card == ulisses.deck.selected_card:
                        ulisses.deck.selected_card = None
                    else:
                        ulisses.deck.selected_card = each_card  

    def end_player_turn(self,ulisses:Ulisses):
        self.is_player_turn = False
        ulisses.current_energy = ulisses.max_energy
        for each_enemy in self.instantiated_enemies:
            each_enemy.current_defense = 0
        ulisses.deck.shuffle_and_allocate()
        self.execute_enemy_combat_loop(ulisses)
        self.end_enemies_turn(ulisses)

    def end_enemies_turn(self,ulisses:Ulisses):
        self.is_player_turn = True  
        ulisses.current_defense = 0 
        for each_enemy in self.instantiated_enemies:
            each_enemy.current_energy = each_enemy.max_energy
        
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