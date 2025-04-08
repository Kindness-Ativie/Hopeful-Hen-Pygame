import pygame
from random import randrange

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1125
screen_height = 750

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hopeful Hen')

# player
player = pygame.image.load('assets/images/hen.png')
pygame.display.set_icon(player)  # sets game icon to player
player_left = pygame.transform.flip(player, True, False)
screen.blit(player, (600, 700))
player_rect = player.get_rect()
player_rect.x = screen_width / 2  # starting x
player_rect.y = screen_height - 50  # starting y
player_speed = 7
# background
bg = 'assets/images/purple_camp.jpg'
bg_2 = 'assets/images/starry_night.jpg'


# classes
class Enemy:
    def __init__(self, image, height, speed):
        self.image = image
        self.speed = speed
        self.pos = image.get_rect().move(0, height)
        # self.rect = (self.pos, self.image.get_width(), self.image.get_height())

    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right > screen_width - 20:
            self.pos.left = 0

    def collide(self, player_r):
        if player_r.colliderect(self.pos):
            return True


class Coin:
    def __init__(self, image, edge):
        self.image = image
        self.x_pos = randrange(0 + edge, screen_width - edge)
        self.y_pos = randrange(0 + edge, screen_height - edge)
        self.rect = (self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height())

    def update(self):
        screen.blit(self.image, (self.x_pos, self.y_pos))

    def collide(self, player_r):
        if player_r.colliderect(self.rect):
            return True


# enemy
enemy_img = pygame.image.load('assets/images/ghost.png')
enemies = []
total_enemies = 10
for num in range(total_enemies):
    opponent = Enemy(enemy_img, num * 90, randrange(7, 15))
    enemies.append(opponent)


# animations
lightning_bolt = pygame.image.load('assets/images/thunder.png')


# ----------------------- FUNCTIONS -------------------------
# scales and blits your bg! Enter true if it's already scaled!
def static_background(image_path, scaled=False):
    screen_surface = pygame.image.load(image_path)
    if scaled is False:
        scaled_surface = pygame.transform.scale(screen_surface, (screen_width, screen_height))
        screen.blit(scaled_surface, (0, 0))
    else:
        screen.blit(screen_surface, (0, 0))


# uses top left vs center
def text_on_screen(text: str, font_path, font_size, color, surface, x_pos, y_pos):
    display_font = pygame.font.Font(font_path, font_size)
    text_render = display_font.render(text, 1, color)
    text_rect = text_render.get_rect()
    text_rect.topleft = (x_pos, y_pos)
    surface.blit(text_render, text_rect)


# uses center
def text_on_screen_center(text: str, font_path, font_size, color, surface, x_pos, y_pos):
    display_font = pygame.font.Font(font_path, font_size)
    text_render = display_font.render(text, 1, color)
    text_rect = text_render.get_rect(center=(x_pos, y_pos))
    surface.blit(text_render, text_rect)


def text_on_screen_center_return(text: str, font_path, font_size, color, surface, x_pos, y_pos):
    display_font = pygame.font.Font(font_path, font_size)
    text_render = display_font.render(text, 1, color)
    text_rect = text_render.get_rect(center=(x_pos, y_pos))
    surface.blit(text_render, text_rect)

    return text_rect


def icon_on_screen(image_path, x_pos, y_pos, x_y_scale=None):
    loaded_image = pygame.image.load(image_path)
    if x_y_scale is None:
        icon_rect = loaded_image.get_rect(center=(x_pos, y_pos))
        screen.blit(loaded_image, icon_rect)
    else:
        scaled_image = pygame.transform.scale(loaded_image, x_y_scale)
        icon_rect = scaled_image.get_rect(center=(x_pos, y_pos))
        screen.blit(scaled_image, icon_rect)


# useful testing functions
def test_click_coor():
    # use with event.type == pygame.MOUSEBUTTONDOWN for click:
    x, y = pygame.mouse.get_pos()
    print(f'(x, y) = ({x}, {y})')

# def animation(image, x_pos, y_pos, speed):
#     screen.blit(image, (x_pos, y_pos))
#     image_rect = image.get_rect()
#     image_rect.move(0, speed)


# ----------------- GAME LOOPS ---------------------
# Game play
def game_running_screen():
    # score
    score = 0
    total_coins_collected = 0
    level = 1

    # coins
    coin_img = pygame.image.load('assets/images/coin.png')
    coins = []
    coin_goal = 10
    for _ in range(coin_goal):
        my_coin = Coin(coin_img, 50)
        coins.append(my_coin)

    game_running = True
    while game_running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        static_background(bg)
        text_on_screen(f'Score: {score}/{coin_goal}', 'assets/fonts/LLPIXEL3.ttf', 30, 'white', screen, 6, 6)
        text_on_screen(f'Level {level}', 'assets/fonts/LLPIXEL3.ttf', 30, 'white', screen, screen_width / 2 - 50, 6)
        text_on_screen(f'Total coins: {total_coins_collected}', 'assets/fonts/LLPIXEL3.ttf', 30, 'white', screen, screen_width / 2 + 200, 6)

        for alien in enemies:
            alien.move()
            screen.blit(alien.image, alien.pos)
            if alien.collide(player_rect):
                game_running = False
                game_over_screen()
                pygame.quit()

        for coin in coins:
            coin.update()
            if coin.collide(player_rect):
                coins.remove(coin)
                score += 1
                total_coins_collected += 1

                if score == coin_goal:
                    level += 1
                    score = 0
                    coin_goal += 10
                    for _ in range(coin_goal):
                        new_coin = Coin(coin_img, 50)
                        coins.append(new_coin)

                # animation(lightning_bolt, coin.x_pos, coin.y_pos, 10)
                # screen.blit(coin.image, (575, 700))

        # collect_coin()
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_LEFT]:
            player_rect.x -= player_speed
            # player = pygame.transform.flip(player, True, False)
        if key_press[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if key_press[pygame.K_SPACE]:
            player_rect.y -= player_speed * 2

        player_rect.y += player_speed * 0.8
        if player_rect.y > screen_height - 100:
            player_rect.y = screen_height - 100
        screen.blit(player, player_rect)

        pygame.display.flip()

    pygame.quit()


# ------------------------ GAME OVER / RESTART LOOP ---------------
def game_over_screen():
    display_font = pygame.font.Font('assets/fonts/LLPIXEL3.ttf', 80)
    text_render = display_font.render('RESTART?', 1, 'white')
    text_rect = text_render.get_rect(center=(550, 400))

    game_over = True
    while game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                mouse_rect = (mouse[0], mouse[1], 5, 5)
                if text_rect.colliderect(mouse_rect):
                    game_running_screen()
                    pygame.quit()

        static_background(bg)
        text_on_screen_center('GAME OVER', 'assets/fonts/LLPIXEL3.ttf', 60, 'white', screen, 550, 325)
        screen.blit(text_render, text_rect)


        # text_on_screen_center(f'Score: {temp_score}', 'assets/fonts/LLPIXEL3.ttf', 30, 'white', screen, 550, 375)
        # text_on_screen('TRY AGAIN?', 'assets/fonts/LLPIXEL3.ttf', 60, 'white', screen, 550, 400)

        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_SPACE]:
            game_running_screen()

        pygame.display.flip()


# ------------------- TUTORIAL SCREEN --------------------------
def tutorial_screen():
    # button
    start_button = pygame.image.load('assets/images/start-button.png')
    start_button_rect = start_button.get_rect()
    start_button_rect.x = screen_width / 2 - 100
    start_button_rect.y = 70
    game_over = True
    while game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                mouse_rect = (mouse[0], mouse[1], 5, 5)
                if start_button_rect.colliderect(mouse_rect):
                    game_running_screen()


        static_background(bg)
        screen.blit(player, (screen_width / 2, screen_height - 100))
        text_on_screen_center('INSTRUCTIONS', 'assets/fonts/LLPIXEL3.ttf', 80, 'white', screen, 550, 50)
        screen.blit(start_button, start_button_rect)
        text_1 = 'Our poor hen dreams of flying'
        text_2 = 'It needs coins to buy fancy wings'
        text_3 = 'But, there\'s some pesky ghosts lurking'
        text_on_screen_center(text_1, 'assets/fonts/Storyboo.TTF', 40, 'white', screen, 550, 350)
        icon_on_screen('assets/images/coin.png', 560, 320)
        icon_on_screen('assets/images/coin.png', 580, 320)
        icon_on_screen('assets/images/coin.png', 600, 320)
        text_on_screen_center(text_2, 'assets/fonts/Storyboo.TTF', 40, 'white', screen, 550, 400)
        icon_on_screen('assets/images/ghost.png', 59, 496)
        icon_on_screen('assets/images/ghost.png', 109, 500)
        icon_on_screen('assets/images/ghost.png', 981, 499)
        icon_on_screen('assets/images/ghost.png', 1042, 502)
        text_on_screen_center(text_3, 'assets/fonts/Storyboo.TTF', 40, 'white', screen, 550, 450)
        text_on_screen('<--    -->', 'assets/fonts/LLPIXEL3.ttf', 40, 'white', screen, 50, screen_height - 50)
        text_on_screen('SPACE = UP', 'assets/fonts/LLPIXEL3.ttf', 40, 'white', screen, 840, screen_height - 50)


        pygame.display.flip()


# --------------------- SCREEN CALLS --------------------------
# game_running_screen()
tutorial_screen()
pygame.quit()
