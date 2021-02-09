import pygame, sys
from pygame.locals import *
pygame.init()
import random

class tile:
    def __init__(self, _BOXSIZE, _left, _top, _image):
        self.BOXSIZE = _BOXSIZE
        self.left = _left
        self.top = _top
        self.TILESURF = pygame.Surface((self.BOXSIZE, self.BOXSIZE))
        self.isFloor = False
        self.isWall = False
        self.image = _image
    def drawTile(self, DISPLAYSURF):
        self.TILESURF.blit(self.image, (0,0))
        self.TILESURF.set_colorkey((255, 255, 255))
        DISPLAYSURF.blit(self.TILESURF, (self.left, self.top))

class main():
    BOARDWIDTH = 60
    BOARDHEIGHT = 60
    TILESIZE = 10
    displayWidth = 0
    displayHeight = 0
    fpsClock = pygame.time.Clock()
    score = 0
    highScore = 0
    tileList = []
    centerArray = []
    centerArrayNumber = 0
    DISPLAYSURF = pygame.display.set_mode((600,600))
    pygame.display.set_caption("RougeLike")

    #ratio
    ratioNumberHeight = 1
    ratioNumberWidth = 1
    height = 0
    width = 0

    #Boolean Values
    playable = True
    createdBoard = False
    restarted = False
    player1Lost = False

    #Board Config
    minXLength = 3
    maxXlength = 15
    minYLength = 3
    maxYlength = 15
    borderWidth = 3
    roomNumberMin = 5
    roomNumberMax = 20
    hallWayRandomMove = 10
    minHallwayLength = 3


    #Images
    Floor = pygame.image.load("images/TestFloor.png")
    Wall = pygame.image.load("images/TestWall.png")

    def main(self):
        while True:
            # Creating board
            while self.createdBoard == False:
                self.createBoard()
                self.drawBoard()
                self.createdBoard = True
            # Moving character
            if self.playable == True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                                print("Left")
                            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                                print("Right")
                            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                                print("Up")
                            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                                print("Down")
            #Updating board
            if self.playable == True:
                pygame.display.update()
            self.fpsClock.tick(30)
    def createBoard(self):
        self.tileList = [[0] * self.BOARDWIDTH for x in range(self.BOARDHEIGHT)]
        tempTop = 0 - self.TILESIZE
        for y in range(self.BOARDHEIGHT):
            tempTop += self.TILESIZE
            tempLeft = 0 - self.TILESIZE
            for x in range(self.BOARDWIDTH):
                tempLeft += self.TILESIZE
                self.tileList[y][x] = tile(30, tempLeft, tempTop, self.Wall)
                self.tileList[y][x].isWall = True
        while True:
            roomAmount = (random.random()* self.roomNumberMax) + 1
            if roomAmount >= self.roomNumberMin and roomAmount <= self.roomNumberMax:
                break
        tempNumber = 0
        while roomAmount > 0:
            xStart = int((random.random()* (self.BOARDWIDTH - self.maxXlength - self.borderWidth))) + self.borderWidth
            yStart = int((random.random()* (self.BOARDHEIGHT - self.maxYlength - self.borderWidth))) + self.borderWidth
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
                        if self.tileList[y][x].isFloor or self.tileList[y - 1][x].isFloor or self.tileList[y + 1][x].isFloor or self.tileList[y][x - 1].isFloor or self.tileList[y][x + 1].isFloor:
                            tempCheck = True
                            tempNumber += 1
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
                            if xLength == 0:
                                self.centerArray.append((y, x, self.centerArrayNumber, [-1]))
                                self.centerArrayNumber += 1
                    roomAmount -= 1
                if tempNumber == 3:
                    roomAmount -= 1
                    tempNumber = 0
        print(self.centerArrayNumber)
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
                    for x in range(len(axisOne[3])):
                        if axisTwo[2] == axisOne[3][x]:
                            breakout = False
                else:
                    breakout = False
                if breakout == True:
                    axisOne[3].append(axisTwo[2])
                    print(axisOne[3])
                    break
            (currentY, currentX, currentRoomNumber, currentArray) = axisOne
            (finalY, finalX, finalRoomNumber, finalArray) = axisTwo
            tempHallWayLength = 0
            self.hallWayRandomMove = 10
            while True:
                if tempHallWayLength == 0:
                    direction = int(random.random() * 4) + 1
                    tempHallWayLength = self.minHallwayLength
                if direction == 1 and currentY > self.borderWidth + 1 and (currentY > finalY or self.hallWayRandomMove > 0):
                    currentY -= 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                elif direction == 2 and currentX < self.BOARDWIDTH - self.borderWidth - 1 and (currentX < finalX or self.hallWayRandomMove > 0):
                    currentX += 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                elif direction == 3 and currentY < self.BOARDHEIGHT - self.borderWidth - 1 and (currentY < finalY or self.hallWayRandomMove > 0):
                    currentY += 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                elif direction == 4 and currentX > self.borderWidth + 1 and (currentX > finalX or self.hallWayRandomMove > 0):
                    currentX -= 1
                    tempHallWayLength -= 1
                    self.hallWayRandomMove -= 1
                else:
                    tempHallWayLength = 0
                self.tileList[currentY][currentX].image = self.Floor
                self.tileList[currentY][currentX].isWall = False
                self.tileList[currentY][currentX].isFloor = True
                if currentY == finalY and currentX == finalX:
                    break
    def drawBoard(self):
        for y in range(self.BOARDHEIGHT):
            for x in range(self.BOARDWIDTH):
                self.tileList[y][x].drawTile(self.DISPLAYSURF)



MainObject = main()
MainObject.main()
