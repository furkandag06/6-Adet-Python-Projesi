import pygame
import sys
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = {
    '1': (255, 0, 0), #Kırmızı
    '2': (0, 255, 0), #Yeşil
    '3': (0, 0, 255), #Mavi
    '4': (255, 255, 0), #Sarı
    '5': (0, 255, 255), #Turkuaz
    '6': (255, 0, 255), #Lila
    '7': (128, 128, 128), #Gri
}

# Top ve raket ayarları
ball_size = 20
ball_speed_x = 5
ball_speed_y = 5
paddle_width, paddle_height = 10, 100
paddle_speed = 10
hitbox_extension = 12  # Raketlerin genişletilmiş hitbox'ı
SCORE_LIMIT = 7

# Top ve raketlerin başlangıç konumları
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x = random.choice([-5, 5])
ball_speed_y = random.choice([-5, 5])
ball_color = WHITE
paddle1_x, paddle1_y = 30, HEIGHT // 2 - paddle_height // 2
paddle2_x, paddle2_y = WIDTH - 40, HEIGHT // 2 - paddle_height // 2

# Skorlar
score1, score2 = 0, 0

# Yazı fontu
font = pygame.font.Font(None, 74)  # Varsayılan fontu kullanabiliriz, özel bir font dosyası da kullanılabilir

# Mod seçimi
mode = None
paddle_color = WHITE  # Varsayılan raket rengi

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def show_winner(winner_text):
    screen.fill(BLACK)
    draw_text(winner_text, font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)  # Kazanan mesajını 3 saniye göstermek için bekle

def draw_color_palette():
    color_width, color_height = 100, 50
    spacing = 10
    start_x = WIDTH // 2 - (color_width * len(COLORS) + spacing * (len(COLORS) - 1)) // 2
    start_y = HEIGHT // 2 - color_height // 2
    for index, (color_name, color_value) in enumerate(COLORS.items()):
        pygame.draw.rect(screen, color_value, (start_x + index * (color_width + spacing), start_y, color_width, color_height))
        draw_text(color_name, font, BLACK, screen, start_x + index * (color_width + spacing) + color_width // 2, start_y + color_height // 2)

def select_color(color_type):
    global paddle_color, ball_color
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                color_width, color_height = 100, 50
                spacing = 10
                start_x = WIDTH // 2 - (color_width * len(COLORS) + spacing * (len(COLORS) - 1)) // 2
                start_y = HEIGHT // 2 - color_height // 2
                for index, (color_name, color_value) in enumerate(COLORS.items()):
                    rect = pygame.Rect(start_x + index * (color_width + spacing), start_y, color_width, color_height)
                    if rect.collidepoint(mouse_x, mouse_y):
                        if color_type == 'paddle':
                            paddle_color = color_value
                        elif color_type == 'ball':
                            ball_color = color_value
                        return

        screen.fill(BLACK)
        draw_color_palette()
        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Ana menü fonksiyonu
def main_menu():
    global mode
    button_width, button_height = 300, 50
    button_spacing = 20
    start_x = WIDTH // 2
    start_y = HEIGHT // 2 - (button_height + button_spacing)  # İlk butonun y koordinatı

    while mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_x - button_width // 2 < mouse_x < start_x + button_width // 2:
                    if start_y < mouse_y < start_y + button_height:  # 'Tek Kişilik' butonu
                        mode = 'single'
                    elif start_y + button_height + button_spacing < mouse_y < start_y + 2 * button_height + button_spacing:  # 'İki Kişilik' butonu
                        mode = 'multi'
                    elif start_y + 2 * (button_height + button_spacing) < mouse_y < start_y + 3 * button_height + 2 * button_spacing:  # 'Renk Seçimi' butonu
                        select_color('paddle')
                    elif start_y + 3 * (button_height + button_spacing) < mouse_y < start_y + 4 * button_height + 3 * button_spacing:  # 'Top Rengi Değiştir' butonu
                        select_color('ball')
                    elif start_y + 4 * (button_height + button_spacing) < mouse_y < start_y + 5 * button_height + 4 * button_spacing:  # 'Çıkış' butonu
                        pygame.quit()
                        sys.exit()

        screen.fill(BLACK)
        draw_text('Pong Oyunu', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 200)

        # 'Tek Kişilik' butonu
        pygame.draw.rect(screen, WHITE, (start_x - button_width // 2, start_y, button_width, button_height), 2, border_radius=10)
        draw_text('Tek Kisilik', font, WHITE, screen, start_x, start_y + button_height // 2)

        # 'İki Kişilik' butonu
        pygame.draw.rect(screen, WHITE, (start_x - button_width // 2, start_y + button_height + button_spacing, button_width, button_height), 2, border_radius=10)
        draw_text('İki Kisilik', font, WHITE, screen, start_x, start_y + button_height + button_spacing + button_height // 2)

        # 'Renk Seçimi' butonu
        pygame.draw.rect(screen, WHITE, (start_x - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height), 2, border_radius=10)
        draw_text('Renk Degis', font, WHITE, screen, start_x, start_y + 2 * (button_height + button_spacing) + button_height // 2)
        
        # 'Top Rengi Değiştir' butonu
        pygame.draw.rect(screen, WHITE, (start_x - button_width // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height), 2, border_radius=10)
        draw_text('Top Rengi', font, WHITE, screen, start_x, start_y + 3 * (button_height + button_spacing) + button_height // 2)
        
        # 'Çıkış' butonu
        pygame.draw.rect(screen, WHITE, (start_x - button_width // 2, start_y + 4 * (button_height + button_spacing), button_width, button_height), 2, border_radius=10)
        draw_text('Çıkış', font, WHITE, screen, start_x, start_y + 4 * (button_height + button_spacing) + button_height // 2)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Ana menüyü başlat
main_menu()

# Raketleri çizme fonksiyonu
def draw_paddle(x, y, width, height, surface, color):
    pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height))

def bot_ai():
    global paddle2_y

    bot_reaction_chance = 0.75
    bot_speed = 5  # Botun hareket hızı
    bot_error_margin = 10

    if random.random() < bot_reaction_chance:
        paddle2_center = paddle2_y + paddle_height / 2
        target_y = ball_y - paddle_height / 2

        # Hedef konuma ulaşmak için yumuşak hareket
        if abs(paddle2_center - ball_y) > bot_error_margin:
            if paddle2_center < ball_y:
                paddle2_y += min(bot_speed, ball_y - paddle2_center)
            else:
                paddle2_y -= min(bot_speed, paddle2_center - ball_y)

    # Raket sınırları
    if paddle2_y < 0:
        paddle2_y = 0
    if paddle2_y > HEIGHT - paddle_height:
        paddle2_y = HEIGHT - paddle_height
        
# Oyunun ana döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Klavye girdileri
    keys = pygame.key.get_pressed()
    if mode == 'multi':
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s] and paddle1_y < HEIGHT - paddle_height:
            paddle1_y += paddle_speed
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - paddle_height:
            paddle2_y += paddle_speed
    elif mode == 'single':
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s] and paddle1_y < HEIGHT - paddle_height:
            paddle1_y += paddle_speed

        # Bot hareketi
        bot_ai()

    # Topun hareketi
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Topun duvarlara çarpması
    if ball_y <= 0 or ball_y >= HEIGHT - ball_size:
        ball_speed_y = -ball_speed_y

    # Topun raketlere çarpması
    if (ball_x <= paddle1_x + paddle_width + hitbox_extension and
            paddle1_y - hitbox_extension < ball_y + ball_size and
            paddle1_y + paddle_height + hitbox_extension > ball_y):
        ball_speed_x = -ball_speed_x
    if (ball_x + ball_size >= paddle2_x - hitbox_extension and
            paddle2_y - hitbox_extension < ball_y + ball_size and
            paddle2_y + paddle_height + hitbox_extension > ball_y):
        ball_speed_x = -ball_speed_x

    # Skorları güncelleme
    if ball_x < 0:
        score2 += 1
        if score2 >= SCORE_LIMIT:
            show_winner("Oyuncu 2 Kazandı!")
            score1, score2 = 0, 0
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = random.choice([-5, 5])
        ball_speed_y = random.choice([-5, 5])
    if ball_x > WIDTH:
        score1 += 1
        if score1 >= SCORE_LIMIT:
            show_winner("Oyuncu 1 Kazandı!")
            score1, score2 = 0, 0
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = random.choice([-5, 5])
        ball_speed_y = random.choice([-5, 5])

    # Ekranı temizle
    screen.fill(BLACK)

    # Topu çiz
    pygame.draw.ellipse(screen, ball_color, pygame.Rect(ball_x, ball_y, ball_size, ball_size))

    # Raketleri çiz
    draw_paddle(paddle1_x, paddle1_y, paddle_width, paddle_height, screen, paddle_color)
    draw_paddle(paddle2_x, paddle2_y, paddle_width, paddle_height, screen, paddle_color)

    # Skorları çiz
    draw_text(str(score1), font, WHITE, screen, WIDTH // 4, 50)
    draw_text(str(score2), font, WHITE, screen, WIDTH * 3 // 4, 50)

    # Ekranı güncelle
    pygame.display.flip()
    pygame.time.Clock().tick(60)
