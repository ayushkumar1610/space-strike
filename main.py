import pygame
import random

# initilizing pygame
pygame.init()

# creating a screen
screen = pygame.display.set_mode((800,600))
background = pygame.image.load("background.png")
score = 0

# Icon and caption
pygame.display.set_caption("Space Strike") 
icon = pygame.image.load("favicon.png") 
pygame.display.set_icon(icon)
destroyIcon = pygame.image.load("destroy.png")

# player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 490
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyChange = []
num_enemy = 5
for i in range(num_enemy):
    enemyImg.append(pygame.image.load("enemy.png")) 
    enemyX.append(random.randint(35,750))
    enemyY.append(random.randint(45,150))
    enemyChange.append(0)

# bullet
bulletImg = pygame.image.load("bullet.png") 
bulletX = 0
bulletY = 490
bulletXChange = 0
bulletYChange = 0
bulletState = "ready"


def player(x, y):
    # blit means draw.
    screen.blit(playerImg,(x, y)) 

def enemy(x, y, e):
    screen.blit(enemyImg[e],(x, y)) 

def bulletFire(x, y):
    global bulletState
    bulletState = "fire"    # we can use any global variable but to change it, should be global
    screen.blit(bulletImg, (x + 20, y + 9))

def collisionEnemy(e):
    global enemyX
    global enemyY 
    enemyX[e] = random.randint(0,780)
    enemyY[e] = random.randint(27,35)


# Game loop
running = True
while running:
    
    # screen color/background
    # screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

    # event loop
    for event in pygame.event.get():

        # terminating window
        if event.type == pygame.QUIT:
            running = False

        # ======= Positioning player ========
        # checking keystroke pressed is left or right
        # KEYDOWN --> pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_LEFT:
                playerX_change -= 5
            # generate bullet on space
            if event.key == pygame.K_SPACE:
                bulletX = playerX
                bulletFire(bulletX,bulletY)
        # KEYUP --> released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0


    # coordinates to be passed
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_enemy):
        # enemy position
        if enemyChange[i] == 0:
            enemyX[i] += 2
        else:
            enemyX[i] -= 2
        if enemyX[i] >= 767:
            enemyChange[i] = 1
            enemyY[i] += random.randint(17,43) 
        if enemyX[i] <= 0:
            enemyChange[i] = 0
            enemyY[i] += random.randint(20,41)
        
        # bullet fire
        if bulletState == "fire":
            # drawing bullet
            bulletFire(bulletX, bulletY)
            bulletY -= 2.5
        if bulletY <= 0:    
            bulletY = 490
            bulletState = "ready"

        # distance for collision
        distFire = (abs( (enemyX[i]-bulletX)**2 + (enemyY[i]-bulletY)**2 ))**(1/2)
        if distFire <= 25:
            
            destroyTime = 0
            while destroyTime <= 55:
                screen.blit(destroyIcon, (enemyX[i], enemyY[i]))
                screen.blit(destroyIcon, (enemyX[i], enemyY[i]))
                screen.blit(destroyIcon, (enemyX[i], enemyY[i]))
                destroyTime += 1
            score += 1
            collisionEnemy(i)
            bulletY = 490
            bulletState = "ready"
            
        # drawing player
        player(playerX, playerY)

        # drawing enemy
        enemy(enemyX[i], enemyY[i], i)

    # always update display
    pygame.display.update()

print(score)