import pygame
import math
import random

# u need to initialize pygame
pygame.init()

# creating the screen and displaying resolution AND the background
screen = pygame.display.set_mode((1366, 768))
level_1 = pygame.image.load('background1.jpg')

# game title and icon
pygame.display.set_caption("The Empire Strikes Back Again!")
icon = pygame.image.load('millennium-falcon.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('gracz2.png')
playerX = 683
playerY = 580
playerX_move = 0

# tie fighters
tie_fighterImg = []
tie_fighterX = []
tie_fighterY = []
tie_fighterX_move = []
tie_fighterY_move = []
tie_num = 2

for i in range(tie_num):
    tie_fighterImg.append(pygame.image.load('tie_fighter.png'))
    tie_fighterX.append(random.randint(64, 1302))
    tie_fighterY.append(-71)
    tie_fighterX_move.append(0)
    tie_fighterY_move.append(0.3)

# player laser shot
# read - bullet is not fired
# fire - bullet is fired
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 580
laserX_move = 0
laserY_move = 3
laser_state = "ready"

# adding score
score_vaule = 0
font = pygame.font.Font('starfont.ttf', 32)
scoreX = 10
scoreY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_vaule), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))  # it draws player image


def tie_fighter(x, y, i):
    screen.blit(tie_fighterImg[i], (x, y))  # it draws tie fighter


def laser_shoot(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollison(tie_fighterX, tie_fighterY, laserX, laserY):
    distance = math.sqrt((math.pow(tie_fighterX - laserX, 2)) + (math.pow(tie_fighterY - laserY, 2)))
    if distance < 30:
        return True
    else:
        return False


# game loop - game is running always
running = True
while running:
    # this is RGB code - Red,Gree,Blue that will display from 0 to 255
    # you can check RGB to color converter
    screen.fill((0, 0, 0))
    # here is background image:
    screen.blit(level_1, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right of left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_move = -2
            if event.key == pygame.K_RIGHT:
                playerX_move = 2
            # shooting
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laserX = playerX
                    laser_shoot(playerX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0

    # this will change the position of player
    playerX += playerX_move

    # getting some boundaries
    if playerX <= -64:
        playerX = 1366
    elif playerX >= 1430:
        playerX = -63

    # how the enemy moves in this game
    for i in range(tie_num):
        tie_fighterY[i] += tie_fighterY_move[i]
        if tie_fighterY[i] <= -70:
            tie_fighterY_move[i] = 0.5
        elif tie_fighterY[i] >= 780:
            tie_fighterY_move[i] = 0

        # collison laser - tie
        collision = isCollison(tie_fighterX[i], tie_fighterY[i], laserX, laserY)
        if collision:
            laserY = 580
            laser_state = "ready"
            score_vaule += 10
            tie_fighterX[i] = random.randint(64, 1302)
            tie_fighterY[i] = -71

        tie_fighter(tie_fighterX[i], tie_fighterY[i], i)

    # that was tricky - tried to add some additional movements for ties
    for i in range(tie_num):
        if tie_fighterY[i] >= 100 and tie_fighterY[i] <= 100.6:
            tie_fighterX_move[i] = random.choice([-64, 64])
            tie_fighterX[i] += tie_fighterX_move[i]

        if tie_fighterY[i] >= 400 and tie_fighterY[i] <= 400.6:
            tie_fighterX_move[i] = random.choice([-64, 64])
            tie_fighterX[i] += tie_fighterX_move[i]
    # the enemies cannot go out the boundaries
    for i in range(tie_num):
        if tie_fighterX[i] <= 64:
            tie_fighterX[i] = 63
        if tie_fighterX[i] >= 1300:
            tie_fighterX[i] = 1299

    # laser movement
    if laserY <= 0:
        laserY = 580
        laser_state = "ready"
    if laser_state == "fire":
        laser_shoot(laserX, laserY)
        laserY -= laserY_move

    # player must be drawn after setting the screen colors!
    player(playerX, playerY)
    show_score(scoreX, scoreY)
    pygame.display.update()
