import utils.transport
import utils.session
import pgzrun
import random
from pygame import Rect
from math import sqrt

# Tamanho da janela do jogo
WIDTH = 800
HEIGHT = 600

# Definição das cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Estados do jogo
MENU = "menu"
GAME = "game"
EXIT = "exit"
WIN = "win"
LOSE = "lose"  # Novo estado para quando o jogador perde

#estado inicial do jogo
game_state = MENU

# Definição dos botões do menu 
buttons = {
    "start": Rect(50, 150, 150, 30),
    "sound": Rect(50, 200, 150, 30),
    "exit": Rect(50, 250, 150, 30)
}

game_buttons = {
    "exit": Rect(WIDTH - 150, HEIGHT - 30, 150, 30)
}

#alterna entre som ativado e desativado
def play_sound(sound_obj):
    if sound_on:
        sound_obj.play()

# Jogo inicia com som ativado
sound_on = True

# Carregar a música de fundo
music.play("background.mp3")

# Carregar o som de colisão ao fazer ponto
collision_sound_circle = sounds.load("pontonojogo.mp3")

# Carregar o som de colisão quando colidir com o inimigo
collision_sound_enemy = sounds.load("colisaoinimigo.mp3")

# Carregar a imagem de fundo
background_image = Actor('background.png')

# Variáveis de largura e altura da imagem para centralizar imagem de fundo
bg_width = background_image.width - 70
bg_height = background_image.height
x = (WIDTH - bg_width) // 2
y = (HEIGHT - bg_height) // 2

# Carregar a imagem do sprite do personagem
character = Actor('game_sheet.png')  

heroe_width = 31  # ajustar a largura do sprite do herói
heroe_height = 30  # ajustar a altura do sprite do herói

enemy_width = 70 #ajustar a largura do inimigo
enemy_height = 140 #ajustar a altura do inimigo

heroe_speed = 5  # Velocidade do herói

# Posição inicial do herói 
heroe_x = x + bg_width // 2
heroe_y = y + bg_height // 2

# Posição inicial do inimigo
enemy_x = x + 80 + bg_width // 4
enemy_y = y + bg_height // 4

# Posição inicial do círculo
circle_x = random.randint(x, x + bg_width)
circle_y = random.randint(y, y + bg_height)
circle_radius = 15  # Raio do círculo

# Variável de pontuação do herói
heroe_score = 0  # Inicializa a pontuação do herói em zero

# Função para atualizar a posição do inimigo
def update_enemy_position():
    global enemy_x, enemy_y
    enemy_x = random.randint(x, x + bg_width - enemy_width)
    enemy_y = random.randint(y, y + bg_height - enemy_height)

# Agendar a atualização da posição do inimigo a cada 8 segundos
clock.schedule_interval(update_enemy_position, 8.0)

# Mudança da posição do círculo
def update_circle_position():
    global circle_x, circle_y
    circle_x = random.randint(x, x + bg_width)
    circle_y = random.randint(y, y + bg_height)

# Agendar a atualização da posição do círculo a cada 10 segundos
clock.schedule_interval(update_circle_position, 10.0)

# Detecção da colisão com o círculo
def check_collision():
    global heroe_score
    distance = sqrt((heroe_x - circle_x)**2 + (heroe_y - circle_y)**2)
    if distance < heroe_width // 2 + circle_radius:
        heroe_score += 1
        play_sound(collision_sound_circle)
        update_circle_position()

# Verificar colisão entre o herói e o inimigo 
def check_enemy_collision():
    
    global game_state
    scale_factor = 2
    
    cut_top = 105

    # Retângulo do herói, usando as dimensões desenhadas:
    hero_rect = Rect(
        heroe_x - heroe_width // 2,
        heroe_y - heroe_height // 2,
        heroe_width + scale_factor,
        heroe_height + scale_factor
    )

    # Retângulo do inimigo, usando as dimensões desenhadas:
    enemy_rect = Rect(
        enemy_x - enemy_width // 2,
        enemy_y - enemy_height // 2,
        enemy_width - 40 + scale_factor,
        enemy_height - cut_top + scale_factor
    )

    # Debug: imprima ou desenhe os retângulos se necessário
    # print("Hero rect:", hero_rect)
    # print("Enemy rect:", enemy_rect)

    if hero_rect.colliderect(enemy_rect):
        play_sound(collision_sound_enemy)
        game_state = LOSE



# Atualizações da tela do jogo
def update():    
    global heroe_x, heroe_y, game_state
    if game_state == GAME:
        if keyboard.left:
            heroe_x -= heroe_speed
        if keyboard.right:
            heroe_x += heroe_speed
        if keyboard.up:
            heroe_y -= heroe_speed
        if keyboard.down:
            heroe_y += heroe_speed

        # Garantir que o herói não saia da área da imagem de fundo, ajustando os limites
        heroe_x = max(x + 38, min(x + bg_width - heroe_width - 10, heroe_x))  # Ajuste para permitir mais movimento à esquerda e direita
        heroe_y = max(y + 13, min(y + bg_height - heroe_height + 12, heroe_y))  # Ajuste para permitir mais movimento na parte superior
        
        # Verificar colisão do herói com o círculo
        check_collision()

        # Verificar colisão do herói com o inimigo
        check_enemy_collision()

        # Verificar se o herói ganhou o jogo
        if heroe_score >= 3:
            game_state = WIN

# Fim do jogo, jogador venceu
def draw_win():
    screen.fill(BLACK)  # Preencher a tela com preto
    screen.draw.text("Parabéns, você ganhou!!!", center=(WIDTH // 2, HEIGHT // 2), color=WHITE, fontsize=50)

# Tela de derrota
def draw_lose():
    screen.fill(BLACK)  # Preencher a tela com preto
    screen.draw.text("Você perdeu o jogo!", center=(WIDTH // 2, HEIGHT // 2), color=WHITE, fontsize=50)

# Exibição de tela de acordo com estado do jogo
def draw():
    screen.clear()
    screen.blit(background_image.image, (x, y))  # Desenha a imagem de fundo centralizada
    if game_state == MENU:
        draw_menu()
    elif game_state == GAME:
        draw_game()
    elif game_state == WIN:
        draw_win()
    elif game_state == LOSE:
        draw_lose()

#criação do menu
def draw_menu():
    screen.draw.text("Menu Principal", topleft=(50, 120), color=WHITE, fontsize=25)  # Texto do menu alinhado à esquerda e acima dos botões
    screen.draw.filled_rect(buttons["start"], WHITE)
    screen.draw.filled_rect(buttons["sound"], WHITE)
    screen.draw.filled_rect(buttons["exit"], WHITE)
    screen.draw.text("Começar o jogo", center=buttons["start"].center, color=BLACK, fontsize=20)
    screen.draw.text("Música e sons: {}".format("Ligados" if sound_on else "Desligados"), center=buttons["sound"].center, color=BLACK, fontsize=15)
    screen.draw.text("Saída", center=buttons["exit"].center, color=BLACK, fontsize=20)

    # Instruções do jogo
    instructions = [
        "Mova o herói com as setas de navegação",
        "e colecione 3 itens na tela para vencer o jogo.",
        "Caso o inimigo colida com você, você perde o jogo."
    ]
    for i, line in enumerate(instructions):
        screen.draw.text(line, center=(WIDTH // 2 + 25, 100 + i * 30), color=WHITE, fontsize=26)

# Desenho do botão de saída, jogador e círculo vermelho na tela
def draw_game():
    screen.draw.filled_rect(game_buttons["exit"], WHITE)
    screen.draw.text("Saída", center=game_buttons["exit"].center, color=BLACK, fontsize=20)

    # Desenha o círculo
    screen.draw.filled_circle((circle_x, circle_y), circle_radius, (255, 0, 0))  # Cor do círculo (vermelho)

    #criação da imagem do herói e do inimigo
    heroe_image = character._surf
    enemy_image = character._surf  

    # Inserção da imagem do herói
    scale_factor = 2  
    for x in range(heroe_width + scale_factor):
        for y in range(heroe_height + scale_factor):
            src_x = x // scale_factor
            src_y = y // scale_factor
            
            # Garantir que os índices estejam dentro dos limites do retângulo recortado
            if 0 <= src_x < heroe_image.get_width() and 0 <= src_y < heroe_image.get_height():
                color = heroe_image.get_at((src_x, src_y))
                # Ignorar pixels pretos ou transparentes
                if color != BLACK and color != (0, 0, 0, 0):  
                    screen.surface.set_at((heroe_x - heroe_width // 2 + x, heroe_y - heroe_height // 2 + y), color)

    # Inserção da imagem do inimigo
    scale_factor = 2  
    cut_top = 105  # Quantidade de pixels a serem cortados da parte superior

    for x in range(enemy_width - 40 + scale_factor):
        for y in range(cut_top, enemy_height + scale_factor):  # Começa a partir de `cut_top` para cortar a parte superior
            src_x = x // scale_factor
            src_y = y // scale_factor
            
            # Garantir que os índices estejam dentro dos limites do retângulo recortado
            if 0 <= src_x < enemy_image.get_width() and 0 <= src_y < enemy_image.get_height():
                color = enemy_image.get_at((src_x, src_y))
                # Ignorar pixels pretos ou transparentes
                if color != BLACK and color != (0, 0, 0, 0):  
                    screen.surface.set_at((enemy_x - enemy_width // 2 + x, enemy_y - enemy_height // 2 + y - cut_top), color)

    # Desenhar a pontuação do herói
    screen.draw.text("Pontuação: {}".format(heroe_score), topleft=(WIDTH - 250, HEIGHT - 25), color=WHITE, fontsize=20)

# Ações de clique com o mouse
def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == MENU:
        if buttons["start"].collidepoint(pos):
            game_state = GAME
        elif buttons["sound"].collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                music.play("background")
            else:
                music.stop()
        elif buttons["exit"].collidepoint(pos):
            exit_game()
    elif game_state == GAME:
        if game_buttons["exit"].collidepoint(pos):
            exit_game()

#sair do jogo
def exit_game():
    raise SystemExit("O jogo foi fechado pelo usuário.")

#executar o jogo
pgzrun.go()