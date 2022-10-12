import pygame
import random
import math
from pygame import mixer

pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.mp3')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('ship.png')
playerX = 378
playerX_change = 0
playerY = 480

# Invader
invaderImg = []
invaderX = []
invaderY = []
invaderX_change = []
invaderY_change = []

no_of_invaders = 4

for i in range(no_of_invaders):
    invaderImg.append(pygame.image.load('invader.png'))
    invaderX.append(random.randint(20, 730))
    invaderX_change.append(1.5)
    invaderY_change.append(40)
    invaderY.append(random.randint(50, 200))

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2.5
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 60)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (220, 250))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means draw


def invader(x, y):
    screen.blit(invaderImg[i], (x, y))  # blit means draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y - 15))


def isCollision(invaderX, invaderY, bulletX, bulletY):
    distance = math.sqrt(
        math.pow(invaderX - bulletX, 2) + math.pow(invaderY - bulletY, 2))
    if distance < 27:
        return True
    return False


# Game loop
running = True
while running:
    screen.fill((30, 30, 30))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_SPACE:
                if (bullet_state == "ready"):
                    bullet_sound = mixer.Sound('Shoot.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of ship
    playerX += playerX_change
    if (playerX >= 750):
        playerX = 750
    elif (playerX <= 20):
        playerX = 20

    # Enemy movement

    for i in range(no_of_invaders):
        # game over
        if (invaderY[i] > 420):
            for j in range(no_of_invaders):
                invaderY[j] = 2000
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            game_over_text()
            break
        invaderX[i] += invaderX_change[i]
        if (invaderX[i] >= 730):
            invaderX_change[i] = -1.5
            invaderY[i] += invaderY_change[i]
        elif (invaderX[i] <= 20):
            invaderX_change[i] = 1.5
            invaderY[i] += invaderY_change[i]

        # collison
        collision = isCollision(invaderX[i], invaderY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('invaderkilled.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            invaderX[i] = random.randint(21, 650)
            invaderY[i] = random.randint(50, 200)

        invader(invaderX[i], invaderY[i])

    # bullet movement
    if (bullet_state == "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if (bulletY <= 0):
        bulletY = 480
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
