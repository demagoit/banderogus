import pygame
from pygame.constants import QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT
import random
from os import listdir

# initiate game
pygame.init()
# initiate clock for game speed
FPS = pygame.time.Clock()
font = pygame.font.SysFont('Verdana', 20)

# set screen size
screen = width, height = 880, 660
WHITE = 255, 255, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0

# set the game scene
main_surface = pygame.display.set_mode(screen)
bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgx = 0
bgx2 = bg.get_width()
bg_speed = 3

# set hero character
# player = pygame.Surface((20, 20))
# player.fill(WHITE)
IMG_PATH = 'goose'


# scale player images
def scale_player_imgs(ratio=1.0):
    player_imgs = []
    for file in listdir(IMG_PATH):
        img = pygame.image.load(IMG_PATH + "/" + file).convert_alpha()
        player_imgs.append(pygame.transform.scale_by(img, ratio))
    return player_imgs


ratio = 0.5
player_imgs = scale_player_imgs(ratio)
img_index = 0
player = player_imgs[img_index]
player_rect = player.get_rect()
player_speed = 5
# create handler for player animation event
CHANGE_IMG = pygame.USEREVENT + 1
# set player animation evoke timer
pygame.time.set_timer(CHANGE_IMG, 125)


# set enemy character
def create_enemy():
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (100, 35))
    enemy_rect = pygame.Rect(width, random.randint(enemy.get_height(), height - enemy.get_height()),
                             *enemy.get_size())
    enemy_speed = random.randint(1, 5)
    return [enemy, enemy_rect, enemy_speed]


# create handler for enemy creation event
CREATE_ENEMY = pygame.USEREVENT + 2
# set enemy evoke timer
pygame.time.set_timer(CREATE_ENEMY, 1500)
# create active enemies list
enemies = []


# set bonus character
def create_bonuses():
    # bonus = pygame.Surface((20, 20))
    # bonus.fill(GREEN)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (90, 150))
    bonus_rect = pygame.Rect(random.randint(bonus.get_width(), width - bonus.get_width()),
                             -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(1, 5)
    return [bonus, bonus_rect, bonus_speed]


# create handler for bonus creation event (+3 - to appear apart from enemy)
CREATE_BONUS = pygame.USEREVENT + 3
# set bonus evoke timer
pygame.time.set_timer(CREATE_BONUS, 2000)
# create active bonuses list
bonuses = []

is_working = True
score = 0

while is_working:
    # set game speed Frames Per Second
    FPS.tick(60)

    for event in pygame.event.get():
        # event to stop the game
        if event.type == QUIT:
            is_working = False
        # event to evoke new enemy
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        # event to evoke new bonus
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonuses())
        # event fo player animation
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index >= len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    # capture pressed keys
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_DOWN] and player_rect.bottom <= height:
        player_rect = player_rect.move(0, player_speed)
    if pressed_keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(0, -player_speed)
    if pressed_keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(-player_speed, 0)
    if pressed_keys[K_RIGHT] and player_rect.right <= width:
        player_rect = player_rect.move(player_speed, 0)

    # paint moving game background
    # main_surface.fill(BLACK)
    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))
    if bgx2 < 0:
        bgx = 0
        bgx2 = bg.get_width()
    else:
        bgx -= bg_speed
        bgx2 -= bg_speed
    # place hero character on screen
    main_surface.blit(player, player_rect)

    # place score counter on screen
    main_surface.blit(font.render(str(score), True, GREEN), (width - 100, 0))

    for enemy in enemies:
        # place enemy on screen
        main_surface.blit(enemy[0], enemy[1])
        # move enemy on screen
        enemy[1] = enemy[1].move(-enemy[2], 0)
        # release memory from escaped enemy
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            # re-shape hero character after enemy hit
            # player.fill([random.randint(1, 254), random.randint(1, 254), random.randint(1, 254)])
            ratio = ratio / 1.3
            player_imgs = scale_player_imgs(ratio)
            player = player_imgs[img_index]
            player_rect = pygame.Rect(player_rect.left, player_rect.top, *player.get_size())
            score -= 3
            if score <= 0:
                is_working = False

    for bonus in bonuses:
        # place bonus on screen
        main_surface.blit(bonus[0], bonus[1])
        # move bonus on screen
        bonus[1] = bonus[1].move(0, bonus[2])
        # release memory from escaped bonus
        if bonus[1].top > height:
            bonuses.pop(bonuses.index(bonus))
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            # re-shape hero character after bonus hit
            # player.fill(WHITE)
            ratio = ratio * 1.1
            player_imgs = scale_player_imgs(ratio)
            player = player_imgs[img_index]
            player_rect = pygame.Rect(player_rect.left, player_rect.top, *player.get_size())
            score += 1
    # render game scene
    pygame.display.flip()
