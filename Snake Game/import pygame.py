import pygame
import time
import random

# Pygame'i başlat
pygame.init()

# Ekran boyutları
width, height = 600, 400
panel_height = 50  # Skor ve can göstergesi için üstte bir panel
game_height = height - panel_height  # Oyun alanı yüksekliği
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Geliştirilmiş Yılan Oyunu')

# Renkler
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
gray = (192, 192, 192)

# Yılanın başlangıç boyutu ve hız
snake_block = 10
snake_speed = 15

# Yiyecek boyutu
food_size = 10

# Can sayısı
initial_lives = 3

# Puanı ve canları gösterme fonksiyonu
def your_score(score):
    font_style = pygame.font.SysFont(None, 35)
    value = font_style.render("Your Score: " + str(score), True, black)
    screen.blit(value, [0, 0])

def your_lives(lives):
    font_style = pygame.font.SysFont(None, 35)
    value = font_style.render("Lives: " + str(lives), True, black)
    screen.blit(value, [width - 150, 0])

# Yılanı çizme fonksiyonu
def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# Yiyecek oluşturma fonksiyonu
def create_food():
    return [round(random.randrange(0, width - food_size) / 10.0) * 10.0,
            round(random.randrange(panel_height, game_height - food_size) / 10.0) * 10.0]

# Butonları çizme fonksiyonu
def draw_button(text, color, button_rect):
    pygame.draw.rect(screen, color, button_rect)
    font = pygame.font.SysFont(None, 35)
    text_surf = font.render(text, True, white)
    screen.blit(text_surf, (button_rect.x + 10, button_rect.y + 10))

# Oyunu duraklatma ekranı
def pause_game():
    paused = True
    while paused:
        screen.fill(blue)
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render("Paused", True, red)
        screen.blit(mesg, [width / 3, height / 3])

        resume_button = pygame.Rect(width / 4, height / 2, 120, 50)
        quit_button = pygame.Rect(width / 2 + 10, height / 2, 120, 50)

        draw_button('Resume', green, resume_button)
        draw_button('Quit', red, quit_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if resume_button.collidepoint(pos):
                    paused = False
                if quit_button.collidepoint(pos):
                    pygame.quit()
                    quit()

# Oyun döngüsü
def gameLoop():
    game_over = False
    game_close = False

    # Başlangıç pozisyonu ve değişkenler
    x1 = width / 2
    y1 = panel_height + (game_height - panel_height) / 2
    x1_change = 0
    y1_change = 0

    # Başlangıç yılanı
    snake_List = [[x1, y1]]
    Length_of_snake = 1

    # Yiyecek ve skor
    foodx, foody = create_food()
    score = 0
    lives = initial_lives

    clock = pygame.time.Clock()

    while not game_over:
        while game_close == True:
            screen.fill(blue)
            font_style = pygame.font.SysFont(None, 50)
            mesg = font_style.render("You Lost!", True, red)
            screen.blit(mesg, [width / 6, height / 6])
            your_score(score)
            your_lives(lives)

            # Butonları tanımla
            new_game_button = pygame.Rect(width / 4, height / 2, 120, 50)
            close_button = pygame.Rect(width / 2 + 10, height / 2, 120, 50)

            draw_button('New Game', green, new_game_button)
            draw_button('Close', red, close_button)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if new_game_button.collidepoint(pos):
                        gameLoop()
                    if close_button.collidepoint(pos):
                        game_over = True
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:  # 'p' tuşuna basarak oyunu duraklat
                    pause_game()

        x1 += x1_change
        y1 += y1_change

        # Ekran kenarlarından geçiş
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - snake_block
        if y1 >= height:
            y1 = panel_height
        elif y1 < panel_height:
            y1 = game_height - snake_block

        screen.fill(blue)
        pygame.draw.rect(screen, gray, [0, 0, width, panel_height])  # Üst panel
        pygame.draw.rect(screen, green, [foodx, foody, food_size, food_size])

        # Yılanın yeni başını ekleyin
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        # Eğer yılan uzunluğu aşılırsa, eski elemanları sil
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Kendine çarpma
        if snake_Head in snake_List[:-1]:
            lives -= 1
            if lives <= 0:
                game_close = True
            else:
                # Oyunu yeniden başlat, ama yılan boyutunu koru
                x1 = width / 2
                y1 = panel_height + (game_height - panel_height) / 2
                x1_change = 0
                y1_change = 0
                snake_List = []
                # Yılanı boyutunda yeniden oluştur
                for _ in range(Length_of_snake):
                    snake_List.append([x1, y1])
                foodx, foody = create_food()
                time.sleep(1)  # Biraz bekle

        our_snake(snake_block, snake_List)
        your_score(score)
        your_lives(lives)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody = create_food()
            Length_of_snake += 1
            score += 10

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
