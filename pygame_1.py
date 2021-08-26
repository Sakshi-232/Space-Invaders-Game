import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

# Adding Title
pygame.display.set_caption("Space Invadors")

# Adding icon
icon = pygame.image.load("spaceship_img.png")
pygame.display.set_icon(icon)

# Adding background image
background = pygame.image.load("space_background_1.png")

# Adding Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Adding player
player_img = pygame.image.load("spaceship (3).png")
PlayerX = 380
PlayerY = 480
PlayerX_change = 0

# Adding enemy

enemy_img = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_enemies = 7

for i in range(num_enemies):
    enemy_img.append(pygame.image.load("ufo.png"))
    EnemyX.append(random.randint(0, 730))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(0.2)
    EnemyY_change.append(40)

# Adding Bullet
bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8  # To move at the speed of 10
bullet_state = "ready"

# score

score_val = 0
font = pygame.font.Font("freesansbold.ttf", 20)

textX = 10
textY = 10

game_over_font = pygame.font.Font("freesansbold.ttf", 1260)


def game_over_display():
    game_over = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullets(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 15, y + 20))


def iscollision(EnemyX, EnemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(EnemyX - bulletX, 2)) + (math.pow(EnemyY - bulletY, 2)))
    if distance <= 30:
        return True
    else:
        return False


running = True
while running:

    screen.fill((0, 0, 0))
    # PlayerY -= 0.1   # To check the moment left,right, yop or bottom

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # For the movement of spaceship by key strokes

        if event.type == pygame.KEYDOWN:
            # print("keystroke has been pressed")
            if event.key == pygame.K_LEFT:
                # print("Left arrow key is pressed")
                PlayerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                # print("Right arrow key pressed")
                PlayerX_change = 0.3
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                if bullet_state == "ready":
                    bulletX = PlayerX
                    fire_bullets(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke is released")
                PlayerX_change = 0

    # creating boundaries for spaceship
    PlayerX += PlayerX_change

    if PlayerX < 0:
        PlayerX = 0
    elif PlayerX >= 730:
        PlayerX = 730

    # creating boundaries for enemy
    for i in range(num_enemies):
        if EnemyY[i] > 440:
            for j in range(num_enemies):
                EnemyY[i] = 2000
                game_over_display()
                break
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 0.2
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 730:
            EnemyX_change[i] = -0.2
            EnemyY[i] += EnemyY_change[i]

        collision = iscollision(EnemyX[i], EnemyY[i], bulletX, bulletY)
        if collision:
            collide_sound = mixer.Sound("explosion.wav")
            collide_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            # print(score_val)
            EnemyX[i] = random.randint(0, 730)
            EnemyY[i] = random.randint(50, 150)

        enemy(EnemyX[i], EnemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullets(bulletX, bulletY)
        bulletY -= bulletY_change

    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()
