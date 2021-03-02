import pygame, sys
from pygame.locals import *
from pygame.sprite import *
pygame.init()
import random

class centerInfo():
    def __init__(self, _currentY, _currentX, _currentRoomNumber, _currentArray):
        self.currentY = _currentY
        self.currentX = _currentX
        self.roomNumber = _currentRoomNumber
        self.array = _currentArray
class tile(Sprite):
    def __init__(self, _BOXSIZE, _left, _top, _image, _x, _y):
        pygame.sprite.Sprite.__init__(self)
        Sprite.__init__(self)
        self.BOXSIZE = _BOXSIZE
        self.left = _left
        self.top = _top
        self.TILESURF = pygame.Surface((self.BOXSIZE, self.BOXSIZE))
        self.isFloor = False
        self.isWall = False
        self.isRoom = False
        self.isEnemy = False
        self.isPlayer = False
        self.isConnected = False
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.BOXSIZE, self.BOXSIZE)
        self.x = _x
        self.y = _y
    def drawTile(self, DISPLAYSURF):
        self.TILESURF.blit(self.image, (0,0))
        self.TILESURF.set_colorkey((255, 255, 255))
        DISPLAYSURF.blit(self.TILESURF, (self.left, self.top))
class Enemy(Sprite):
    def __init__(self, _BOXSIZE, _left, _top, _image, _moveTime, _damage, _critDamage, _waitAttack, _health):
        pygame.sprite.Sprite.__init__(self)
        self.BOXSIZE = _BOXSIZE
        self.left = _left
        self.top = _top
        self.TILESURF = pygame.Surface((self.BOXSIZE, self.BOXSIZE))
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.BOXSIZE, self.BOXSIZE)
        self.speed = .2
        self.following = False
        self.canGoVerticle = True
        self.canGoHorizontal = True
        self.randomMovementX = 0
        self.randomMovementY = 0
        self.randomlyMovingX = False
        self.randomlyMovingY = False
        self.leavingCorner = False
        self.cornerMovementY = 0
        self.cornerMovementX = 0
        self.movingDirection = ""
        self.milliseconds = 0
        self.waitAttackTime = _waitAttack
        self.moveTime = _moveTime
        self.damage = _damage
        self.critDamage = _critDamage
        self.fpsClock = pygame.time.Clock()
        self.health = _health
        self.hurt = False
    def moveTowardsPlayer(self, player, backgroundGroup, distanceToPlayer, maxFollowDistance):
        self.milliseconds += self.fpsClock.tick_busy_loop(60)
        if self.milliseconds > self.moveTime:
            self.milliseconds = 0
            if self.moveTime != 60:
                self.moveTime = 60
            dirvect = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            if self.following == True and abs(dirvect.x) >= maxFollowDistance * self.BOXSIZE + 1 or abs(dirvect.y) >= maxFollowDistance * self.BOXSIZE + 1:
                    self.following = False
            if (dirvect.x != 0 or dirvect.y != 0) and (self.following == True or abs(dirvect.x) <= distanceToPlayer*self.BOXSIZE + 1 and abs(dirvect.y) <= distanceToPlayer*self.BOXSIZE + 1):
                if self.following == False:
                    self.following = True
                if self.canGoVerticle == False and self.canGoHorizontal == False and self.leavingCorner == False:
                    self.randomlyMovingX = False
                    self.randomlyMovingY = False
                    self.leavingCorner = True
                    tempCheck = int(random.random() * 2) + 1
                    if tempCheck == 1:
                        self.movingDirection = "HOR"
                    else:
                        self.movingDirection = "VER"
                elif abs(dirvect.x) < self.BOXSIZE and abs(dirvect.x) > 0 and self.leavingCorner == False:
                    self.randomlyMovingX = True
                elif abs(dirvect.y) < self.BOXSIZE and abs(dirvect.y) > 0 and self.leavingCorner == False:
                    self.randomlyMovingY = True
                if dirvect.y < 0:
                    dirvect.y = -1
                elif dirvect.y > 0:
                    dirvect.y = 1
                else:
                    dirvect.y = 0
                if dirvect.x < 0:
                    dirvect.x = -1
                elif dirvect.x > 0:
                    dirvect.x = 1
                else:
                    dirvect.x = 0
                dirvect.y *= self.speed*self.BOXSIZE
                dirvect.x *= self.speed * self.BOXSIZE
                if pygame.sprite.collide_rect(self, player):
                    dirvect.y *= -1
                    dirvect.x *= -1
                    tempCheck = int((random.random()*4) + 1)
                    if tempCheck > 1:
                        player.health -= self.damage
                    else:
                        player.health -= self.critDamage
                    self.moveTime = self.waitAttackTime
                if self.leavingCorner == True:
                    if self.cornerMovementY == 0 and self.cornerMovementX == 0:
                        if self.movingDirection == "HOR":
                            self.cornerMovementX = dirvect.x * -1
                        else:
                            self.cornerMovementY = dirvect.y * -1
                    if self.movingDirection == "HOR":
                        dirvect.x = self.cornerMovementX
                    else:
                        dirvect.y = self.cornerMovementY
                elif self.randomlyMovingX == True:
                    if self.randomMovementX == 0:
                        self.randomMovementX = dirvect.x
                    dirvect.x = self.randomMovementX
                elif self.randomlyMovingY == True:
                    if self.randomMovementY == 0:
                        self.randomMovementY = dirvect.y
                    dirvect.y = self.randomMovementY
                self.rect.y += dirvect.y
                spriteGroup = spritecollide(self, backgroundGroup, False)
                for x in range(len(spriteGroup)):
                    if spriteGroup[x].isWall == True:
                        self.rect.y += dirvect.y * -1
                        self.canGoVerticle = False
                        if self.movingDirection == "VER":
                            self.leavingCorner = False
                            self.cornerMovementY = 0
                            self.movingDirection = ""
                        break
                    elif x == len(spriteGroup) - 1:
                        if self.movingDirection == "HOR":
                            self.leavingCorner = False
                            self.cornerMovementX = 0
                            self.movingDirection = ""
                        self.randomlyMovingX = False
                        self.randomMovementX = 0
                        self.canGoVerticle = True
                spriteGroup = spritecollide(self, self.groups()[0], False)
                for x in range(len(spriteGroup)):
                    if spriteGroup != None and self.moveTime != 800:
                        if spriteGroup[x] != self:
                            self.rect.y += dirvect.y * -1
                            self.canGoVerticle = False
                            self.leavingCorner = False
                            break
                self.rect.x += dirvect.x
                spriteGroup = spritecollide(self, backgroundGroup, False)
                for x in range(len(spriteGroup)):
                    if spriteGroup[x].isWall == True:
                        self.rect.x += dirvect.x * -1
                        self.canGoHorizontal = False
                        if self.movingDirection == "HOR":
                            self.leavingCorner = False
                            self.cornerMovementX = 0
                            self.movingDirection = ""
                        break
                    elif x == len(spriteGroup) - 1:
                        if self.movingDirection == "VER":
                            self.leavingCorner = False
                            self.cornerMovementY = 0
                            self.movingDirection = ""
                        self.randomlyMovingY = False
                        self.randomMovementY = 0
                        self.canGoHorizontal = True
                spriteGroup = spritecollide(self, self.groups()[0], False)
                for x in range(len(spriteGroup)):
                    if spriteGroup != None and self.moveTime != 800:
                        if spriteGroup[x] != self:
                            self.rect.x += dirvect.x * -1
                            self.canGoHorizontal = False
                            self.leavingCorner = False
                            break
class Weapon(Sprite):
    def __init__(self, _left, _top, _image):
        pygame.sprite.Sprite.__init__(self)
        self.left = _left
        self.top = _top
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.rect.width, self.rect.height)
        self.count = 0
        self.xMove = 0
        self.yMove =0
class Player(Sprite):
    def __init__(self, _BOXSIZE, _left, _top, _image, _DisplaySurf):
        pygame.sprite.Sprite.__init__(self)
        self.DisplaySurf = _DisplaySurf
        self.BOXSIZE = _BOXSIZE
        self.left = _left
        self.top = _top
        self.image = _image
        self.permanentImage = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.BOXSIZE, self.BOXSIZE)
        self.direction = ""
        self.mousex = 0
        self.mousey = 0
        self.health = 999
        self.goingUp = False
        self.goingDown = False
        self.goingLeft = False
        self.goingRight = False
        self.sword = Weapon(self.rect.x, self.rect.y, pygame.image.load("images/Sword.png"))
        self.permanentSwordRect = self.sword.rect
        self.permanentSwordX = self.sword.rect.x
        self.permanentSwordY = self.sword.rect.y
        self.permanentSwordWidth = self.sword.rect.width
        self.permanentSwordHeight = self.sword.rect.height
        self.permanentSwordImage = self.sword.image
        self.WeaponGroup = pygame.sprite.Group()
        self.WeaponGroup.add(self.sword)
        self.attacking = False
        self.attackCount = 0
        self.swordDamage = 15
        self.harmedGroup = ""
        self.laserCount = 0
        self.laserGroup = pygame.sprite.Group()
        self.maxLaserDistance = 9
        self.laser = pygame.image.load("images/laser.png")
        self.laserX = self.rect.x
        self.laserY = self.rect.y
        self.laserDamage = 30
        self.harmedCount = 15
    def movePlayer(self, x, y):
        self.rect.x = self.rect.x + x
        self.rect.y = self.rect.y + y
        self.permanentSwordX = self.permanentSwordX + x
        self.permanentSwordY = self.permanentSwordY + y
        self.sword.rect.x = self.sword.rect.x + x
        self.sword.rect.y = self.sword.rect.y + y
    def attackLaser(self):
        if self.harmedCount >= 5:
            self.harmedCount -= 5
            laser = Weapon(self.laserX, self.laserY, self.laser)
            if self.direction == "UP":
                laser.yMove = -20
                laser.xMove = 0
            elif self.direction == "DOWN":
                laser.yMove = 20
                laser.xMove = 0
            elif self.direction == "LEFT":
                laser.yMove = 0
                laser.xMove = -20
            elif self.direction == "RIGHT":
                laser.yMove = 0
                laser.xMove = 20
            self.laserGroup.add(laser)
    def movingLaser(self, enemyGroup, backgroundGroup):
        spriteList = self.laserGroup.sprites()
        for x in range(len(spriteList)):
            spriteList[x].rect.x += spriteList[x].xMove
            spriteList[x].rect.y += spriteList[x].yMove
            spriteList[x].count += 1
            if spriteList[x].count > self.maxLaserDistance:
                spriteList[x].kill()
            spriteGroup = spritecollide(spriteList[x], enemyGroup, False)
            for y in range(len(spriteGroup)):
                spriteGroup[y].health -= self.laserDamage
                if spriteGroup[y].health <= 0:
                    spriteGroup[y].kill()
                spriteList[x].kill()
            spriteGroup = spritecollide(spriteList[x], backgroundGroup, False)
            for y in range(len(spriteGroup)):
                if spriteGroup[y].isWall == True:
                    spriteList[x].kill()
    def attackSword(self, enemyGroup, backgroundGroup):
        spriteGroup = spritecollide(self.sword, backgroundGroup, False)
        for y in range(len(spriteGroup)):
            if spriteGroup[y].isWall == True:
                self.attacking = False
        if self.attacking == True:
            if self.direction == "UP" or self.direction == "DOWN":
                if self.direction == "UP":
                    number = 7
                else:
                    number = -7
                self.attackCount +=7
                if self.attackCount <= 14:
                    self.sword.rect.y -= number
                else:
                    self.sword.rect.y += number
                if self.attackCount == 28:
                    self.attacking = False
                    self.attackCount = 0
            elif self.direction == "LEFT" or self.direction == "RIGHT":
                if self.direction == "LEFT":
                    number = 7
                else:
                    number = -7
                self.attackCount += 7
                if self.attackCount <= 14:
                    self.sword.rect.x -= number
                else:
                    self.sword.rect.x += number
                if self.attackCount == 28:
                    self.attacking = False
                    self.attackCount = 0
            spriteGroup = spritecollide(self.sword, enemyGroup, False)
            for x in range(len(spriteGroup)):
                self.harmedGroup = spriteGroup
                if spriteGroup[x].hurt == False:
                    self.harmedCount += 1
                    spriteGroup[x].health -= self.swordDamage
                    spriteGroup[x].hurt = True
                if spriteGroup[x].health <= 0:
                    spriteGroup[x].kill()
            if self.attacking == False:
                for x in range(len(self.harmedGroup)):
                    self.harmedGroup[x].hurt = False
            pygame.sprite.Group.draw(self.WeaponGroup, self.DisplaySurf)
            pygame.display.update()
    def findAttackDirection(self):
        dirvect = pygame.math.Vector2(self.mousex - self.DisplaySurf.get_width()/2, self.mousey -  self.DisplaySurf.get_height()/2)
        if dirvect.x < 0 and dirvect.y < 0:
            if abs(dirvect.x) > abs(dirvect.y):
                self.direction = "LEFT"
            else:
                self.direction = "UP"
        elif dirvect.x > 0 and dirvect.y < 0:
            if abs(dirvect.x) > abs(dirvect.y):
                self.direction = "RIGHT"
            else:
                self.direction = "UP"
        elif dirvect.x < 0 and dirvect.y > 0:
            if abs(dirvect.x) > abs(dirvect.y):
                self.direction = "LEFT"
            else:
                self.direction = "DOWN"
        elif dirvect.x > 0 and dirvect.y > 0:
            if abs(dirvect.x) > abs(dirvect.y):
                self.direction = "RIGHT"
            else:
                self.direction = "DOWN"
        self.redrawPlayer()
    def redrawPlayer(self):
        if self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.permanentImage, 180)
            self.sword.image = pygame.transform.rotate(self.permanentSwordImage, 180)
            self.sword.rect.x = self.permanentSwordX - self.BOXSIZE + 36
            self.sword.rect.y = self.permanentSwordY + self.BOXSIZE - 23
            self.sword.rect.width = self.permanentSwordWidth
            self.sword.rect.height = self.permanentSwordHeight
            (tempX, tempY) = self.rect.bottomright
            self.laserX = tempX - 11
            self.laserY = tempY - 21
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.permanentImage, 90)
            self.sword.image = pygame.transform.rotate(self.permanentSwordImage, 90)
            self.sword.rect.x = self.permanentSwordX - self.BOXSIZE + 17
            self.sword.rect.y = self.permanentSwordY + 6
            self.sword.rect.width = self.permanentSwordHeight
            self.sword.rect.height = self.permanentSwordWidth
            (tempX, tempY) = self.rect.bottomleft
            self.laserX = tempX + 17
            self.laserY = tempY - 11
        elif self.direction == "RIGHT":
            self.image = pygame.transform.rotate(self.permanentImage, -90)
            self.sword.image = pygame.transform.rotate(self.permanentSwordImage, -90)
            self.sword.rect.x = self.permanentSwordX + self.BOXSIZE - 23
            self.sword.rect.y = self.permanentSwordY + self.BOXSIZE - 9
            self.sword.rect.width = self.permanentSwordHeight
            self.sword.rect.height = self.permanentSwordWidth
            (tempX, tempY) = self.rect.topright
            self.laserX = tempX - 21
            self.laserY = tempY + 7
        elif self.direction == "UP":
            self.image = self.permanentImage
            self.sword.image = self.permanentSwordImage
            self.sword.rect.x = self.permanentSwordX + 21
            self.sword.rect.y = self.permanentSwordY - 13
            self.sword.rect.width = self.permanentSwordWidth
            self.sword.rect.height = self.permanentSwordHeight
            (tempX, tempY) = self.rect.topleft
            self.laserX = tempX + 7
            self.laserY = tempY + 17


class main():
    DISPLAYWIDTH = 15
    DISPLAYHEIGHT = 15
    BOARDWIDTH = 57
    BOARDHEIGHT = 57
    TILESIZE = 30
    fpsClock = pygame.time.Clock()
    milliseconds = 0
    score = 0
    highScore = 0
    boardSprites = ""
    tileList = []
    centerArray = []
    centerArrayNumber = 0
    DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH * TILESIZE, DISPLAYHEIGHT * TILESIZE))
    boardSurface = pygame.Surface((BOARDWIDTH * TILESIZE, BOARDHEIGHT * TILESIZE))
    pygame.display.set_caption("RougeLike")
    canGoUp = False
    canGoDown = False
    canGoRight = False
    canGoLeft = False
    speed = .5
    #boolean
    createdBoard = False
    playable = False
    canSprint = True
    sprinting = False

    #player
    player = ""
    playerX = 0
    playerY = 0
    healthObj = pygame.font.Font('freesansbold.ttf', 20)

    #Board Config
    minXLength = 3
    maxXlength = 8
    minYLength = 3
    maxYlength = 8
    borderWidth = int(DISPLAYWIDTH/2)
    roomNumberMin = 10
    roomNumberMax = 15
    hallWayRandomMove = 1
    minHallwayLength = 4
    chanceOfDoubleHallway = 0
    roomGap = 2

    #Enemy Config
    maxFollowDistance = 10
    minNumberOfEnemies = 8
    maxNumberOfEnemies = 10
    minEnemyDamage = 20
    maxEnemyDamage = 40
    minEnemyHealth = 40
    maxEnemyHealth = 80

    #SpriteGroups
    playerSprite = pygame.sprite
    playerGroup = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()

    #Images
    Floor = pygame.image.load("images/Floor.png")
    Wall = pygame.image.load("images/TestWall.png")
    Enemy = pygame.image.load("images/Enemy1.png")
    Player = pygame.image.load("images/player.png")
    Laser = pygame.image.load("images/laser.png")

    def main(self):
        while True:
            # Creating board
            while self.createdBoard == False:
                self.createBoard()
                self.drawBoard()
                self.createdBoard = True
                self.playable = True
            # Moving character
            if self.playable == True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEMOTION:
                        self.playerSprite.mousex, self.playerSprite.mousey = pygame.mouse.get_pos()
                    elif event.type == MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed(3) == (True, False, False):
                            self.playerSprite.attacking = True
                        if pygame.mouse.get_pressed(3) == (False, False, True) and self.playerSprite.attacking == False:
                            self.playerSprite.attackLaser()
                    elif event.type == KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                self.restart()
                            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                                self.canGoLeft = True
                            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                                self.canGoRight = True
                            if event.key == pygame.K_w or event.key == pygame.K_UP:
                                self.canGoUp = True
                            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                                self.canGoDown = True
                            if event.key == pygame.K_LSHIFT and self.canSprint == True:
                                self.milliseconds = 0
                                self.sprinting = True
                                self.speed = 1
                    elif event.type == KEYUP:
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.canGoLeft = False
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.canGoRight = False
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            self.canGoUp = False
                        if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            self.canGoDown = False
                        if event.key == pygame.K_LSHIFT:
                            self.sprinting = False
                            self.speed = .5
            if self.playerSprite.health <= 0:
                self.restart()
            self.move()
            #Updating board
            if self.playable == True:
                self.playerSprite.attackSword(self.enemyGroup, self.backgroundGroup)
                if self.playerSprite.attacking == False:
                    self.playerSprite.findAttackDirection()
                self.playerSprite.movingLaser(self.enemyGroup, self.backgroundGroup)
                self.drawBoard()
                pygame.display.update()
            self.fpsClock.tick(30)
            self.milliseconds += self.fpsClock.tick_busy_loop(60)
    def createBoard(self):
        originalRandom = self.hallWayRandomMove
        self.tileList = [[0] * self.BOARDWIDTH for x in range(self.BOARDHEIGHT)]
        tempTop = 0 - self.TILESIZE
        for y in range(self.BOARDHEIGHT):
            tempTop += self.TILESIZE
            tempLeft = 0 - self.TILESIZE
            for x in range(self.BOARDWIDTH):
                tempLeft += self.TILESIZE
                self.tileList[y][x] = tile(self.TILESIZE, tempLeft, tempTop, self.Wall, x, y)
                self.tileList[y][x].isWall = True
        while True:
            roomAmount = int ((random.random()* self.roomNumberMax) + 1)
            if roomAmount >= self.roomNumberMin and roomAmount <= self.roomNumberMax:
                break
        tempNumber = 0
        while roomAmount > 0:
            while True:
                xStart = int((random.random()* (self.BOARDWIDTH - self.maxXlength - self.borderWidth)))
                if xStart > self.borderWidth + 1 and xStart < self.BOARDWIDTH - self.borderWidth - 1:
                    break
            while True:
                yStart = int((random.random()* (self.BOARDHEIGHT - self.maxYlength - self.borderWidth)))
                if yStart > self.borderWidth + 1 and yStart < self.BOARDHEIGHT - self.borderWidth - 1:
                    break
            while True:
                xEnd = int ((random.random()* (self.maxXlength) + 1))
                if xEnd >= self.minXLength and xEnd <= self.maxXlength:
                    xEnd = xStart + xEnd
                    break
            while True:
                yEnd = int (random.random()* (self.maxYlength) + 1)
                if yEnd >= self.minYLength and yEnd <= self.maxYlength:
                    yEnd = yStart + yEnd
                    break
            tempCheck = False
            if self.tileList[yStart][xStart].isFloor != True:
                for y in range (yStart, yEnd):
                    for x in range (xStart, xEnd):
                        if self.tileList[y][x].isFloor or self.tileList[y - self.roomGap][x].isFloor or self.tileList[y + self.roomGap][x].isFloor or self.tileList[y][x - self.roomGap].isFloor or self.tileList[y][x + self.roomGap].isFloor:
                            tempCheck = True
                            tempNumber += 1
                            break
                    if tempCheck == True:
                        break
                if tempCheck == False:
                    yLegnth = int ((yEnd - yStart) * .5) + 1
                    xLength = int ((xEnd - xStart) * .5) + 1
                    for y in range(yStart, yEnd):
                        yLegnth -= 1
                        for x in range(xStart, xEnd):
                            if yLegnth == 0:
                                xLength -= 1
                            self.tileList[y][x].image = self.Floor
                            self.tileList[y][x].isWall = False
                            self.tileList[y][x].isFloor = True
                            self.tileList[y][x].isRoom = True
                            if xLength == 0:
                                self.centerArray.append(centerInfo(y, x, self.centerArrayNumber, [-1]))
                                self.centerArrayNumber += 1
                    roomAmount -= 1
                if tempNumber == 3:
                    roomAmount -= 1
                    tempNumber = 0
        tempNumber = 1
        while self.centerArrayNumber > 0:
            axisOne = self.centerArray[len(self.centerArray) - tempNumber]
            tempNumber += 1
            self.centerArrayNumber -= 1
            while True:
                breakout = True
                point = int(random.random() * len(self.centerArray))
                if self.centerArray[point] != axisOne:
                    axisTwo = self.centerArray[point]
                    for x in range(len(axisOne.array)):
                        if axisTwo.roomNumber == axisOne.array[x]:
                            breakout = False
                else:
                    breakout = False
                if breakout == True:
                    axisOne.array.append(axisTwo.roomNumber)
                    break
            currentY = axisOne.currentY
            currentX = axisOne.currentX
            finalY = axisTwo.currentY
            finalX = axisTwo.currentX
            tempHallWayLength = 0
            self.hallWayRandomMove = originalRandom
            tempTest = int(random.random() * 10 + 1)
            tempDirection = "none"
            while True:
                if tempHallWayLength == 0:
                    direction = int(random.random() * 4 + 1)
                    tempHallWayLength = self.minHallwayLength
                if direction == 1 and currentY > self.borderWidth + 1 and (currentY > finalY or self.hallWayRandomMove > 0):
                    currentY -= 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                    tempDirection = "verticle"
                elif direction == 2 and currentX < self.BOARDWIDTH - self.borderWidth - 1 and (currentX < finalX or self.hallWayRandomMove > 0):
                    currentX += 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                    tempDirection = "horizontal"
                elif direction == 3 and currentY < self.BOARDHEIGHT - self.borderWidth - 1 and (currentY < finalY or self.hallWayRandomMove > 0):
                    currentY += 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                    tempDirection = "verticle"
                elif direction == 4 and currentX > self.borderWidth + 1 and (currentX > finalX or self.hallWayRandomMove > 0):
                    currentX -= 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                    tempDirection = "horizontal"
                else:
                    tempHallWayLength = 0
                self.tileList[currentY][currentX].image = self.Floor
                self.tileList[currentY][currentX].isWall = False
                self.tileList[currentY][currentX].isFloor = True
                if self.chanceOfDoubleHallway >= tempTest:
                    if tempDirection == "verticle":
                        if currentX == self.borderWidth:
                            addNumber = 1
                        else:
                            addNumber = -1
                        self.tileList[currentY][currentX + addNumber].image = self.Floor
                        self.tileList[currentY][currentX + addNumber].isWall = False
                        self.tileList[currentY][currentX + addNumber].isFloor = True
                    else:
                        if currentY == self.borderWidth:
                            addNumber = 1
                        else:
                            addNumber = -1
                        self.tileList[currentY + addNumber][currentX].image = self.Floor
                        self.tileList[currentY + addNumber][currentX].isWall = False
                        self.tileList[currentY + addNumber][currentX].isFloor = True
                if currentY == finalY and currentX == finalX:
                    break
        for y in range(self.BOARDHEIGHT):
            for x in range(self.BOARDWIDTH):
                self.backgroundGroup.add(self.tileList[y][x])
        while True:
            pointx = int(random.random()*self.BOARDWIDTH)
            pointy = int(random.random()*self.BOARDHEIGHT)
            if self.tileList[pointy][pointx].isRoom == True:
                self.tileList[pointy][pointx].isPlayer = True
                tempPlayer = Player(self.TILESIZE, self.tileList[pointy][pointx].left, self.tileList[pointy][pointx].top, self.Player, self.DISPLAYSURF)
                self.playerGroup.add(tempPlayer)
                self.playerSprite = tempPlayer
                #self.playerSprite.rect.update(self.tileList[pointy][pointx].left, self.tileList[pointy][pointx].top, self.TILESIZE, self.TILESIZE)
                self.playerX = self.tileList[pointy][pointx].x
                self.playerY = self.tileList[pointy][pointx].y
                for y in range(pointy - self.borderWidth, pointy + self.borderWidth):
                    for x in range(pointx - self.borderWidth, pointx + self.borderWidth):
                        self.tileList[y][x].isPlayer = True
                break
        while True:
            numberOfEnemies = int(random.random()*10) + 1
            if numberOfEnemies >= self.minNumberOfEnemies and numberOfEnemies <= self.maxNumberOfEnemies:
                break
        while numberOfEnemies > 0:
            pointx = int(random.random()*self.BOARDWIDTH)
            pointy = int(random.random()*self.BOARDHEIGHT)
            if self.tileList[pointy][pointx].isRoom == True and self.tileList[pointy][pointx].isPlayer == False and self.tileList[pointy][pointx].isEnemy == False:
                while True:
                    tempHealth = int(random.random() * self.maxEnemyHealth) + 1
                    if tempHealth >= self.minEnemyHealth and tempHealth <= self.maxEnemyHealth:
                        break
                while True:
                    tempDamage = int(random.random() * self.maxEnemyDamage) + 1
                    if tempDamage >= self.minEnemyDamage and tempDamage <= self.maxEnemyDamage:
                        break
                tempEnemy= Enemy(self.TILESIZE, self.tileList[pointy][pointx].left, self.tileList[pointy][pointx].top, self.Enemy, 60, tempDamage, tempDamage*2, 800, tempHealth)
                self.enemyGroup.add(tempEnemy)
                numberOfEnemies -= 1
    def drawBoard(self):
        pygame.sprite.Group.draw(self.backgroundGroup, self.boardSurface)
        pygame.sprite.Group.draw(self.playerSprite.WeaponGroup, self.boardSurface)
        pygame.sprite.Group.draw(self.playerGroup, self.boardSurface)
        pygame.sprite.Group.draw(self.enemyGroup, self.boardSurface)
        pygame.sprite.Group.draw(self.playerSprite.laserGroup, self.boardSurface)
        self.DISPLAYSURF.blit(self.boardSurface, (int(self.DISPLAYWIDTH/ 2) * self.TILESIZE - (self.playerX*self.TILESIZE), int(self.DISPLAYHEIGHT/2) * self.TILESIZE - (self.playerY*self.TILESIZE)))
        clockSurfaceObj = self.healthObj.render("Health: " + str(self.playerSprite.health), True, (255, 255, 255))
        self.DISPLAYSURF.blit(clockSurfaceObj, (330, 15))
        clockSurfaceObj = self.healthObj.render("Shots Left: " + str(int(self.playerSprite.harmedCount/5)), True, (255, 255, 255))
        self.DISPLAYSURF.blit(clockSurfaceObj, (318, 38))
    def restart(self):
        self.createdBoard = False
        self.tileList = []
        self.centerArray = []
        self.centerArrayNumber = 0
        self.playerGroup = pygame.sprite.Group()
        self.backgroundGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.playerX = 0
        self.playerY = 0
        self.player = ""
        self.playable = False
    def move(self):
        enemySprites = self.enemyGroup.sprites()
        for x in range(len(enemySprites)):
            enemySprites[x].moveTowardsPlayer(self.playerSprite, self.backgroundGroup, self.borderWidth, self.maxFollowDistance)
        if self.milliseconds > 80 and self.sprinting == True:
            self.speed = .5
            self.canSprint = False
            self.milliseconds = 0
            self.sprinting = False
        if self.milliseconds > 300 and self.canSprint == False:
            self.canSprint = True
        if self.canGoUp == True or self.canGoDown == True:
            if self.canGoUp == True and self.canGoDown == False:
                self.playerY -= self.speed
                self.playerSprite.movePlayer(0, -self.speed * self.TILESIZE)
            if self.canGoDown == True and self.canGoUp == False :
                self.playerY += self.speed
                self.playerSprite.movePlayer(0, self.speed * self.TILESIZE)
            spriteGroup = spritecollide(self.playerSprite, self.enemyGroup, False)
            for x in range(len(spriteGroup)):
                if spriteGroup != None:
                    if self.canGoUp == True:
                        self.playerSprite.movePlayer(0, self.speed * self.TILESIZE)
                        self.playerY += self.speed
                    if self.canGoDown == True:
                        self.playerSprite.movePlayer(0, -self.speed * self.TILESIZE)
                        self.playerY -= self.speed
                    break
            spriteGroup = spritecollide(self.playerSprite, self.backgroundGroup, False)
            for x in range(len(spriteGroup)):
                if spriteGroup[x].isWall == True:
                    if self.canGoUp == True:
                        self.playerSprite.movePlayer(0, self.speed * self.TILESIZE)
                        self.playerY += self.speed
                    if self.canGoDown == True:
                        self.playerSprite.movePlayer(0, -self.speed * self.TILESIZE)
                        self.playerY -= self.speed
                    break
        if self.canGoLeft == True or self.canGoRight == True:
            if self.canGoLeft == True and self.canGoRight == False:
                self.playerX -= self.speed
                self.playerSprite.movePlayer(-self.speed * self.TILESIZE, 0)
            if self.canGoRight == True and self.canGoLeft == False:
                self.playerX += self.speed
                self.playerSprite.movePlayer(self.speed * self.TILESIZE, 0)
            spriteGroup = spritecollide(self.playerSprite, self.enemyGroup, False)
            for x in range(len(spriteGroup)):
                if spriteGroup != None:
                    if self.canGoLeft == True:
                        self.playerSprite.movePlayer(self.speed * self.TILESIZE, 0)
                        self.playerX += self.speed
                    if self.canGoRight == True:
                        self.playerSprite.movePlayer(-self.speed * self.TILESIZE, 0)
                        self.playerX -= self.speed
                    break
            spriteGroup = spritecollide(self.playerSprite, self.backgroundGroup, False)
            for x in range(len(spriteGroup)):
                if spriteGroup[x].isWall == True:
                    if self.canGoLeft == True:
                        self.playerSprite.movePlayer(self.speed * self.TILESIZE, 0)
                        self.playerX += self.speed
                    if self.canGoRight == True:
                        self.playerSprite.movePlayer(-self.speed * self.TILESIZE, 0)
                        self.playerX -= self.speed
                    break






MainObject = main()
MainObject.main()
