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
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.BOXSIZE, self.BOXSIZE)
        self.x = _x
        self.y = _y
    def drawTile(self, DISPLAYSURF):
        self.TILESURF.blit(self.image, (0,0))
        self.TILESURF.set_colorkey((255, 255, 255))
        DISPLAYSURF.blit(self.TILESURF, (self.left, self.top))
class Player(Sprite):
    def __init__(self, _BOXSIZE, _left, _top, _image):
        pygame.sprite.Sprite.__init__(self)
        self.BOXSIZE = _BOXSIZE
        self.left = _left
        self.top = _top
        self.TILESURF = pygame.Surface((self.BOXSIZE, self.BOXSIZE))
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.BOXSIZE, self.BOXSIZE)
    def movePlayer(self, x, y):
        self.rect.x = self.rect.x + x
        self.rect.y = self.rect.y + y
class main():
    DISPLAYWIDTH = 16
    DISPLAYHEIGHT = 12
    BOARDWIDTH = 71
    BOARDHEIGHT = 71
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


    #Board Config
    minXLength = 3
    maxXlength = 8
    minYLength = 3
    maxYlength = 8
    borderWidth = 12
    roomNumberMin = 10
    roomNumberMax = 20
    hallWayRandomMove = 1
    minHallwayLength = 4
    chanceOfDoubleHallway = 3
    roomGap = 2

    #SpriteGroups
    playerSprite = pygame.sprite
    playerGroup = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()

    #Images
    Floor = pygame.image.load("images/TestFloor.png")
    Wall = pygame.image.load("images/TestWall.png")
    hallway = pygame.image.load("images/PlayerTest2.png")

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

            self.move()
            #Updating board
            if self.playable == True:
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
                tempPlayer = Player(self.TILESIZE, int(self.DISPLAYWIDTH/ 2) * self.TILESIZE, int(self.DISPLAYHEIGHT/2) * self.TILESIZE, self.hallway)
                self.playerGroup.add(tempPlayer)
                self.playerSprite = tempPlayer
                self.playerSprite.rect.update(self.tileList[pointy][pointx].left, self.tileList[pointy][pointx].top, self.TILESIZE, self.TILESIZE)
                print(self.playerSprite.rect)
                self.playerX = self.tileList[pointy][pointx].x
                self.playerY = self.tileList[pointy][pointx].y
                break
    def drawBoard(self):
        pygame.sprite.Group.draw(self.backgroundGroup, self.boardSurface)
        pygame.sprite.Group.draw(self.playerGroup, self.boardSurface)
        self.DISPLAYSURF.blit(self.boardSurface, (int(self.DISPLAYWIDTH/ 2) * self.TILESIZE - (self.playerX*self.TILESIZE), int(self.DISPLAYHEIGHT/2) * self.TILESIZE - (self.playerY*self.TILESIZE)))

    def restart(self):
        self.createdBoard = False
        self.tileList = []
        self.centerArray = []
        self.centerArrayNumber = 0
        self.playerGroup = pygame.sprite.Group()
        self.backgroundGroup = pygame.sprite.Group()
        self.playerX = 0
        self.playerY = 0
        self.player = ""
        self.playable = False
    def move(self):
        wentUp = False
        wentDown = False
        wentRight = False
        wentLeft = False
        if self.canGoUp == True:
            self.playerY -= self.speed
            self.playerSprite.movePlayer(0, -self.speed * self.TILESIZE)
            wentUp = True
        if self.canGoLeft == True:
            self.playerX -= self.speed
            self.playerSprite.movePlayer(-self.speed * self.TILESIZE, 0)
            wentLeft = True
        if self.canGoDown == True:
            self.playerY += self.speed
            self.playerSprite.movePlayer(0, self.speed * self.TILESIZE)
            wentDown = True
        if self.canGoRight == True:
            self.playerX += self.speed
            self.playerSprite.movePlayer(self.speed * self.TILESIZE, 0)
            wentRight = True

        spriteGroup = spritecollide(self.playerSprite, self.backgroundGroup, False)
        for x in range(len(spriteGroup)):
            if spriteGroup[x].isWall == True:
                if wentUp == True:
                    self.playerSprite.movePlayer(0, self.speed * self.TILESIZE)
                    self.playerY += self.speed
                if wentDown == True:
                    self.playerSprite.movePlayer(0, -self.speed * self.TILESIZE)
                    self.playerY -= self.speed
                if wentLeft == True:
                    self.playerSprite.movePlayer(self.speed * self.TILESIZE, 0)
                    self.playerX += self.speed
                if wentRight == True:
                    self.playerSprite.movePlayer(-self.speed * self.TILESIZE, 0)
                    self.playerX -= self.speed
                break





MainObject = main()
MainObject.main()
