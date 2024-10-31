import pygame, sys, asyncio
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
        self.isConnected = False
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
        self.isPortal = False
        self.isHealthPack = False
        self.isDamageBuff = False
        self.isDamager = False
        self.isButton = False
        self.isCharge = False
        self.isChanged = False
        self.clickAmount = 0
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.update(self.left, self.top, self.BOXSIZE, self.BOXSIZE)
        self.x = _x
        self.y = _y
        self.isBossStart = False
        self.fpsClock = pygame.time.Clock()
        self.milliseconds = 0
        self.permanentImage = pygame.image.load("images/charge.png")
        self.SparkImage = pygame.image.load("images/spark.png")
        self.laserImage = ""

    def drawTile(self, DISPLAYSURF):
        self.TILESURF.blit(self.image, (0,0))
        self.TILESURF.set_colorkey((255, 255, 255))
        DISPLAYSURF.blit(self.TILESURF, (self.left, self.top))
    def runningSparks(self, enemyGroup, player):
        self.image = self.SparkImage
        spriteGroup = spritecollide(self, enemyGroup, False)
        for x in range(len(spriteGroup)):
            spriteGroup[x].health -= 5
            if spriteGroup[x].health <= 0:
                spriteGroup[x].kill()
        if pygame.sprite.collide_rect(self, player) == True:
            player.health -= 10
    def runningLaser(self, enemyGroup):
        self.image = self.laserImage
        spriteGroup = spritecollide(self, enemyGroup, False)
        for x in range(len(spriteGroup)):
            spriteGroup[x].health -= 1000
            if spriteGroup[x].health <= 0:
                spriteGroup[x].kill()
class Enemy(Sprite):
    def __init__(self, _BOXSIZE, _left, _top, _image, _moveTime, _damage, _critDamage, _waitAttack, _health, _isBoss):
        pygame.sprite.Sprite.__init__(self)
        self.BOXSIZE = _BOXSIZE
        self.left = _left
        self.top = _top
        self.TILESURF = pygame.Surface((self.BOXSIZE, self.BOXSIZE))
        self.image = _image
        self.permanentImage =  _image
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
        self.isBoss = _isBoss
        self.changeCrazy = False
        if self.isBoss == True:
            self.rect.update(self.rect.left - self.BOXSIZE/2, self.rect.top - self.BOXSIZE/2, self.BOXSIZE, self.BOXSIZE)
            self.speed = .1
            self.isStunned = False
            self.isCrazy = False
            self.randomlyMoving = False
            self.rotationCount = 0
        self.originalPositionX = self.rect.centerx
        self.originalPositionY = self.rect.centery
        self.charging = False
        self.repositioning = False
        self.repositionDirvectX = -1
        self.repositionDirvectY = -1
        self.keepGoing = 0
    def moveTowardsPlayer(self, player, backgroundGroup, distanceToPlayer, maxFollowDistance, enemyGroup):
        self.milliseconds += self.fpsClock.tick_busy_loop(60)
        if self.milliseconds > self.moveTime:
            self.milliseconds = 0
            if self.moveTime != 60:
                self.moveTime = 60
            dirvect = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            self.changeimage(dirvect)
            if self.following == True and abs(dirvect.x) >= maxFollowDistance * self.BOXSIZE + 1 or abs(dirvect.y) >= maxFollowDistance * self.BOXSIZE + 1:
                    self.following = False
            if (dirvect.x != 0 or dirvect.y != 0) and (self.following == True or abs(dirvect.x) <= distanceToPlayer*self.BOXSIZE + 1 and abs(dirvect.y) <= distanceToPlayer*self.BOXSIZE + 1):
                if self.following == False:
                    self.following = True
                if self.canGoVerticle == False and self.canGoHorizontal == False and self.leavingCorner == False:
                    self.randomlyMovingX = False
                    self.randomlyMovingY = False
                    self.leavingCorner = True
                    tempCheck = int(random.random() * 2 + 1)
                    if tempCheck == 1:
                        self.movingDirection = "HOR"
                        tempCheck = int(random.random() * 2 + 1)
                        if tempCheck == 1:
                            self.cornerMovementX = self.speed*self.BOXSIZE * -1
                        else:
                            self.cornerMovementX = self.speed * self.BOXSIZE
                    else:
                        self.movingDirection = "VER"
                        tempCheck = int(random.random() * 2 + 1)
                        if tempCheck == 1:
                            self.cornerMovementY = self.speed * self.BOXSIZE * -1
                        else:
                            self.cornerMovementY = self.speed * self.BOXSIZE
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
                            self.canGoVerticle = False
                            self.canGoHorizontal = False
                            self.movingDirection = ""
                            return
                        elif dirvect.x == 0 and self.movingDirection == "":
                            self.canGoHorizontal = False
                            self.cornerMovementX = 0
                            self.leavingCorner = False
                        break
                    elif x == len(spriteGroup) - 1:
                        if self.movingDirection == "HOR":
                            self.leavingCorner = False
                            self.cornerMovementX = 0
                            self.movingDirection = ""
                        self.randomlyMovingX = False
                        self.randomMovementX = 0
                        self.canGoVerticle = True
                spriteGroup = spritecollide(self, enemyGroup, False)
                for x in range(len(spriteGroup)):
                    if spriteGroup != None and self.moveTime != 800:
                        if spriteGroup[x] != self:
                            self.rect.y += dirvect.y * -1
                            self.canGoVerticle = False
                            break
                self.rect.x += dirvect.x
                spriteGroup = spritecollide(self, backgroundGroup, False)
                for x in range(len(spriteGroup)):
                    if spriteGroup[x].isWall == True:
                        self.rect.x += dirvect.x * -1
                        self.canGoHorizontal = False
                        if self.movingDirection == "HOR":
                            self.leavingCorner = False
                            self.canGoVerticle = False
                            self.canGoHorizontal = False
                            self.movingDirection = ""
                            return
                        elif dirvect.y == 0 and self.movingDirection == "":
                            self.canGoVerticle = False
                            self.cornerMovementY = 0
                            self.leavingCorner = False
                        break
                    elif x == len(spriteGroup) - 1:
                        if self.movingDirection == "VER":
                            self.leavingCorner = False
                            self.cornerMovementY = 0
                            self.movingDirection = ""
                        self.randomlyMovingY = False
                        self.randomMovementY = 0
                        self.canGoHorizontal = True
                spriteGroup = spritecollide(self, enemyGroup, False)
                for x in range(len(spriteGroup)):
                    if spriteGroup != None and self.moveTime != 800:
                        if spriteGroup[x] != self:
                            self.rect.x += dirvect.x * -1
                            self.canGoHorizontal = False
                            break
    def bossMoveTowardsPlayer(self, player, backgroundGroup, distanceToPlayer):
        self.milliseconds += self.fpsClock.tick_busy_loop(60)
        if self.milliseconds > self.moveTime:
            self.milliseconds = 0
            if self.moveTime != 60:
                self.moveTime = 60
            if self.repositioning == True:
                self.isStunned = False
                dirvect = pygame.math.Vector2(self.originalPositionX - self.rect.centerx, self.originalPositionY - self.rect.centery)
                if abs(dirvect.x) == 0 and abs(dirvect.y) == 0 or self.keepGoing > 0:
                    if pygame.sprite.collide_rect(self, player) or self.keepGoing > 0:
                        if self.keepGoing == 0:
                            player.health -= self.damage
                        self.keepGoing += 1
                        self.rect.x += 1 * self.BOXSIZE * self.speed
                        self.rect.y += 1 * self.BOXSIZE * self.speed
                        if self.keepGoing >= 10:
                            self.keepGoing = 0
                        return
                    else:
                        self.repositioning = False
                        self.charging = False
                        if self.isCrazy == True:
                            self.isCrazy = False
                            self.randomlyMoving = True
                        return
                else:
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
                    dirvect.y *= self.speed * self.BOXSIZE
                    dirvect.x *= self.speed * self.BOXSIZE
            else:
                dirvect = pygame.math.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
            if self.randomlyMoving == True:
                self.rotateimage()
            elif self.charging == False and self.repositioning == False:
                self.changeimage(dirvect)
            if ((dirvect.x != 0 or dirvect.y != 0) and (abs(dirvect.x) <= distanceToPlayer * self.BOXSIZE + 1 and abs(dirvect.y) <= distanceToPlayer * self.BOXSIZE + 1)) or self.charging == True or self.repositioning == True or self.randomlyMoving == True:
                if self.randomlyMoving == True and self.isCrazy == False:
                    while True:
                        tempCheck = int(random.random() * 3 + 1)
                        if tempCheck == 1:
                            self.randomMovementX = .5 * self.BOXSIZE
                            break
                        elif tempCheck == 2:
                            self.randomMovementX = .5 * self.BOXSIZE * -1
                            break
                        else:
                            self.randomMovementX = 0
                            break
                    while True:
                        tempCheck = int(random.random() * 3 + 1)
                        if tempCheck == 1:
                            self.randomMovementY = .5 * self.BOXSIZE
                            break
                        elif tempCheck == 2:
                            self.randomMovementY = .5 * self.BOXSIZE * -1
                            break
                        elif tempCheck == 3 and self.randomMovementX != 0:
                            self.randomMovementY = 0
                            break
                    self.isCrazy = True
                elif self.charging == False and self.repositioning == False and self.randomlyMoving == False:
                    if self.movingDirection == "UP" or self.movingDirection == "DOWN":
                        if dirvect.x < -15:
                            dirvect.x = -1
                        elif dirvect.x > 15:
                            dirvect.x = 1
                        else:
                            dirvect.x = 0
                            self.charging = True
                        dirvect.y = 0
                    else:
                        if dirvect.y < -15:
                            dirvect.y = -1
                        elif dirvect.y > 15:
                            dirvect.y = 1
                        else:
                            dirvect.y = 0
                            self.charging = True
                        dirvect.x = 0
                    dirvect.y *= .1 * self.BOXSIZE
                    dirvect.x *= .1 * self.BOXSIZE
                    if self.charging == True:
                        if self.movingDirection == "UP":
                            self.randomMovementX = 0
                            self.randomMovementY = -1 * self.BOXSIZE * .5
                        elif self.movingDirection == "DOWN":
                            self.randomMovementX = 0
                            self.randomMovementY = 1 * self.BOXSIZE * .5
                        elif self.movingDirection == "RIGHT":
                            self.randomMovementX = 1 * self.BOXSIZE * .5
                            self.randomMovementY = 0
                        elif self.movingDirection == "LEFT":
                            self.randomMovementX = -1 * self.BOXSIZE * .5
                            self.randomMovementY = 0
                if self.charging == True or self.randomlyMoving == True:
                    dirvect.y = self.randomMovementY
                    dirvect.x = self.randomMovementX
                self.rect.y += dirvect.y
                spriteGroup = spritecollide(self, backgroundGroup, False)
                for x in range(len(spriteGroup)):
                    if spriteGroup[x].isWall == True:

                        self.rect.y += dirvect.y * -1
                        if self.randomlyMoving == False and self.repositioning == False:
                            self.isStunned = True
                            personGroup = spritecollide(player, backgroundGroup, False)
                            tempCheck = False
                            for x in range(len(personGroup)):
                                if personGroup[x].isRoom == False:
                                    self.isStunned = False
                                    tempCheck = True
                            if tempCheck == False:
                                self.moveTime = 2000
                            self.repositioning = True
                            self.charging = False
                        else:
                            if self.changeCrazy == True:
                                self.rotationCount += 1
                                self.isCrazy = False
                                self.changeCrazy = False
                            else:
                                self.changeCrazy = True
                        if self.rotationCount >= 10:
                            self.rotationCount = 0
                            self.randomlyMoving = False
                            self.repositioning = True
                        break
                self.rect.x += dirvect.x
                spriteGroup = spritecollide(self, backgroundGroup, False)
                for x in range(len(spriteGroup)):
                    if spriteGroup[x].isWall == True:
                        self.rect.x += dirvect.x * -1
                        if self.randomlyMoving == False and self.repositioning == False:
                            self.isStunned = True
                            personGroup = spritecollide(player, backgroundGroup, False)
                            tempCheck = False
                            for x in range(len(personGroup)):
                                if personGroup[x].isRoom == False:
                                    self.isStunned = False
                                    tempCheck = True
                            if tempCheck == False:
                                self.moveTime = 2000
                            self.repositioning = True
                            self.charging = False
                        else:
                            if self.changeCrazy == True:
                                self.rotationCount += 1
                                self.isCrazy = False
                                self.changeCrazy = False
                            else:
                                self.changeCrazy = True
                        if self.rotationCount >= 10:
                            self.rotationCount = 0
                            self.randomlyMoving = False
                            self.repositioning = True
                        break
                if pygame.sprite.collide_rect(self, player):
                    if self.charging == True or self.randomlyMoving == True:
                        player.health -= self.damage
                        self.moveTime = self.waitAttackTime
                        self.charging = False
                        self.repositioning = True
                        self.randomlyMoving = False
                        self.isCrazy = False
                spriteGroup = spritecollide(self, self.groups()[0], False)
                for x in range(len(spriteGroup)):
                    if spriteGroup != None:
                        if spriteGroup[x] != self:
                            spriteGroup[x].kill()
    def changeimage(self, vector):
        if vector.x <= 0 and vector.y <= 0:
            if abs(vector.x) > abs(vector.y):
                self.image = pygame.transform.rotate(self.permanentImage, 90)
                if self.isBoss == True:
                    self.movingDirection = "LEFT"
            else:
                self.image = self.permanentImage
                if self.isBoss == True:
                    self.movingDirection = "UP"

        elif vector.x >= 0 and vector.y <= 0:
            if abs(vector.x) > abs(vector.y):
                self.image = pygame.transform.rotate(self.permanentImage, -90)
                if self.isBoss == True:
                    self.movingDirection = "RIGHT"
            else:
                self.image = self.permanentImage
                if self.isBoss == True:
                    self.movingDirection = "UP"
        elif vector.x <= 0 and vector.y >= 0:
            if abs(vector.x) > abs(vector.y):
                self.image = pygame.transform.rotate(self.permanentImage, 90)
                if self.isBoss == True:
                    self.movingDirection = "LEFT"
            else:
                self.image = pygame.transform.rotate(self.permanentImage, -180)
                if self.isBoss == True:
                    self.movingDirection = "DOWN"
        elif vector.x >= 0 and vector.y >= 0:
            if abs(vector.x) > abs(vector.y):
                self.image = pygame.transform.rotate(self.permanentImage, -90)
                if self.isBoss == True:
                    self.movingDirection = "RIGHT"
            else:
                self.image = pygame.transform.rotate(self.permanentImage, -180)
                if self.isBoss == True:
                    self.movingDirection = "DOWN"
    def rotateimage(self):
        self.image = pygame.transform.rotate(self.image, 90)
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
        self.direction = "UP"
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
        self.harmedCount = 5
        self.killedBoss = False
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
                if spriteGroup[y].isBoss == False:
                    spriteGroup[y].health -= self.laserDamage
                else:
                    if spriteGroup[y].isStunned == True:
                        spriteGroup[y].health -= self.laserDamage
                        spriteGroup[y].isCrazy = True
                if spriteGroup[y].health <= 0:
                    if spriteGroup[y].isBoss:
                        self.killedBoss = True
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

                    spriteGroup[x].hurt = True
                    if spriteGroup[x].isBoss == False:
                        spriteGroup[x].health -= self.swordDamage
                        self.harmedCount += 1
                    else:
                        if spriteGroup[x].isStunned == True:
                            self.harmedCount += 1
                            spriteGroup[x].isCrazy = True
                            spriteGroup[x].health -= self.swordDamage
                if spriteGroup[x].health <= 0:
                    if spriteGroup[x].isBoss:
                        self.killedBoss = True
                    spriteGroup[x].kill()

            if self.attacking == False:
                for x in range(len(self.harmedGroup)):
                    self.harmedGroup[x].hurt = False
            pygame.sprite.Group.draw(self.WeaponGroup, self.DisplaySurf)
            pygame.display.update()
    def findAttackDirection(self):
        dirvect = pygame.math.Vector2(self.mousex - self.DisplaySurf.get_width()/2, self.mousey -  self.DisplaySurf.get_height()/2)
        if dirvect.x <= 0 and dirvect.y <= 0:
            if abs(dirvect.x) > abs(dirvect.y):
                self.direction = "LEFT"
            else:
                self.direction = "UP"
        elif dirvect.x >= 0 and dirvect.y <= 0:
            if abs(dirvect.x) > abs(dirvect.y):
                self.direction = "RIGHT"
            else:
                self.direction = "UP"
        elif dirvect.x <= 0 and dirvect.y >= 0:
            if abs(dirvect.x) > abs(dirvect.y):
                self.direction = "LEFT"
            else:
                self.direction = "DOWN"
        elif dirvect.x >= 0 and dirvect.y >= 0:
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
    levelNumber = 1

    #boolean
    createdBoard = False
    playable = False
    canSprint = True
    sprinting = False
    gameMode = ""
    moveOn = False
    dead = False
    onPortal = False
    sparkGoing = False
    onButton = False
    spawningTraps = True
    buttonTick = 0
    moved = False

    #player
    player = ""
    playerX = 0
    playerY = 0
    healthObj = pygame.font.Font('freesansbold.ttf', 20)

    #Board Config
    minXLength = 4
    maxXlength = 8
    minYLength = 4
    maxYlength = 8
    roomNumberMin = 6
    roomNumberMax = 10
    bossMinXLength = 11
    bossMaxXlength = 13
    bossMinYLength = 11
    bossMaxYlength = 13
    bossRoomNumberMin = 3
    bossRoomNumberMax = 4
    borderWidth = int(DISPLAYWIDTH / 2)
    hallWayRandomMove = 1
    minHallwayLength = 4
    chanceOfDoubleHallway = 0
    roomGap = 2

    #Collectables
    minNumberHealthPack = 2
    maxNumberHealthPack = 3
    minNumberDamagePack = 2
    maxNumberDamagePack = 3
    minNumberMines = 2
    maxNumberMines = 3
    minNumberTraps = 3
    maxNumberTraps = 5
    clickAmount = 3
    clickAmount2 = 1

    #Enemy Config
    maxFollowDistance = 10
    minNumberOfEnemies = 6
    maxNumberOfEnemies = 10
    bossMinNumberOfEnemies = 2
    bossMaxNumberOfEnemies = 4
    findMinNumberOfEnemies = 5
    findMaxNumberOfEnemies = 7
    minEnemyDamage = 10
    maxEnemyDamage = 30
    minEnemyHealth = 30
    maxEnemyHealth = 50
    bossHealth = 280
    bossDamage = 10

    #SpriteGroups
    playerSprite = pygame.sprite
    portalSprite = pygame.sprite
    bossSprite = pygame.sprite
    buttonSprite = pygame.sprite
    playerGroup = pygame.sprite.Group()
    backgroundGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    sparkGroup = pygame.sprite.Group()

    #Images
    Floor = pygame.image.load("images/Floor.png")
    Wall = pygame.image.load("images/TestWall.png")
    Enemy = pygame.image.load("images/Enemy1.png")
    Player = pygame.image.load("images/player.png")
    Laser = pygame.image.load("images/laser.png")
    Boss = pygame.image.load("images/Boss.png")
    Portal = pygame.image.load("images/Portal.png")
    Healthpack = pygame.image.load("images/HealthPack.png")
    Damagepack = pygame.image.load("images/DamagePack.png")
    Damager = pygame.image.load("images/Mine.png")
    Button = pygame.image.load("images/Button.png")
    Charge = pygame.image.load("images/charge.png")
    Button2 = pygame.image.load("images/Button2.png")
    Corner = pygame.image.load("images/Corner.png")
    CornerL = pygame.image.load("images/laserCorner.png")
    SideL = pygame.image.load("images/laserSide.png")

    async def main(self):
        while True:
            # Creating board
            while self.createdBoard == False:
                tempCheck = int(random.random() * 4 + 1)
                if tempCheck <= 2:
                    self.gameMode = "ENEMY"
                elif tempCheck <= 4:
                    self.gameMode = "PORTAL"
                if self.levelNumber % 5 == 0:
                    self.gameMode = "BOSS"
                print(self.gameMode)
                self.createBoard()
                self.drawBoard()
                self.createdBoard = True
                self.playable = True

                await asyncio.sleep(0)


            # Moving character
            if self.playable == True and (self.gameMode != "PORTAL" or self.sparkGoing == False):
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
                            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                                self.canGoLeft = True
                            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                                self.canGoRight = True
                            if event.key == pygame.K_w or event.key == pygame.K_UP:
                                self.canGoUp = True
                            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                                self.canGoDown = True
                            if event.key == pygame.K_LSHIFT and self.canSprint == True and self.gameMode != "BOSS":
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

                        await asyncio.sleep(0)
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.dead == True:
                                self.levelNumber = 1
                            self.restart()
                    elif event.type == MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed(3) == (True, False, False):
                            print("You cannot do that action now")
                        if pygame.mouse.get_pressed(3) == (False, False, True):
                            print("You cannot do that action now")

            #Updating board
            if self.playable == True:
                self.move()
                if self.sparkGoing == True:
                    sparkSprites = self.sparkGroup.sprites()
                    for x in range(len(sparkSprites)):
                        if self.gameMode == "ENEMY":
                            sparkSprites[x].runningSparks(self.enemyGroup, self.playerSprite)
                        else:
                            sparkSprites[x].runningLaser(self.enemyGroup)
                            self.canGoUp = False
                            self.canGoDown = False
                            self.canGoLeft = False
                            self.canGoRight = False
                        if (self.gameMode == "ENEMY" and self.buttonTick >= 200) or (self.gameMode == "PORTAL" and self.buttonTick >= 300):
                            self.buttonSprite.clickAmount -= 1
                            if self.buttonSprite.clickAmount <= 0:
                                for y in range(len(sparkSprites)):
                                    sparkSprites[y].image = self.Floor
                                self.sparkGoing = False
                                self.buttonTick = 0
                                break
                            else:
                                for y in range(len(sparkSprites)):
                                    sparkSprites[y].image = sparkSprites[y].permanentImage
                                self.sparkGoing = False
                                self.buttonTick = 0
                                break
                self.playerSprite.attackSword(self.enemyGroup, self.backgroundGroup)
                if self.playerSprite.attacking == False:
                    self.playerSprite.findAttackDirection()
                self.playerSprite.movingLaser(self.enemyGroup, self.backgroundGroup)
                self.drawBoard()
                pygame.display.update()
                if self.playerSprite.health <= 0 and self.playerSprite.attacking == False:
                    self.playable = False
                    self.dead = True
                    self.reset()
                    self.drawBoard()
                    pygame.display.update()
                elif self.gameMode == "BOSS" and self.playerSprite.attacking == False:
                    if self.playerSprite.killedBoss == True:
                        self.levelNumber += 1
                        self.playable = False
                        self.moveOn = True
                        self.increaseDifficulty()
                        self.drawBoard()
                        pygame.display.update()
                elif self.gameMode == "ENEMY" and self.playerSprite.attacking == False:
                    if len(self.enemyGroup) == 0:
                        self.levelNumber += 1
                        self.playable = False
                        self.moveOn = True
                        self.increaseDifficulty()
                        self.drawBoard()
                        pygame.display.update()
                elif self.gameMode == "PORTAL" and self.playerSprite.attacking == False:
                    if self.onPortal == True:
                        self.levelNumber += 1
                        self.playable = False
                        self.moveOn = True
                        self.increaseDifficulty()
                        self.drawBoard()
                        pygame.display.update()
            self.fpsClock.tick(30)
            self.milliseconds += self.fpsClock.tick_busy_loop(60)
            self.buttonTick += self.fpsClock.tick_busy_loop(60)

            await asyncio.sleep(0)

    def createBoard(self):
        quitEarly = False
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
            if self.gameMode == "BOSS":
                tempRoomMin = self.bossRoomNumberMin
                tempRoomMax = self.bossRoomNumberMax
            else:
                tempRoomMin = self.roomNumberMin
                tempRoomMax = self.roomNumberMax
            roomAmount = int (random.random()* tempRoomMax + 1)
            if roomAmount >= tempRoomMin and roomAmount <= tempRoomMax:
                break
        tempNumber = 0
        while roomAmount > 0:
            if self.gameMode == "BOSS":
                tempXMax = self.bossMaxXlength
                tempXMin = self.bossMinXLength
                tempYMax = self.bossMaxYlength
                tempYMin = self.bossMinYLength
            else:
                tempXMax = self.maxXlength
                tempXMin = self.minXLength
                tempYMax = self.maxYlength
                tempYMin = self.minYLength
            while True:
                xStart = int((random.random()* (self.BOARDWIDTH - tempXMax - self.borderWidth)))
                if xStart > self.borderWidth + 1 and xStart < self.BOARDWIDTH - self.borderWidth - 1:
                    break
            while True:
                yStart = int((random.random()* (self.BOARDHEIGHT - tempYMax - self.borderWidth)))
                if yStart > self.borderWidth + 1 and yStart < self.BOARDHEIGHT - self.borderWidth - 1:
                    break
            while True:
                xEnd = int ((random.random()* (tempXMax) + 1))
                if xEnd >= tempXMin and xEnd <= tempXMax:
                    xEnd = xStart + xEnd
                    break
            while True:
                yEnd = int (random.random()* (tempYMax) + 1)
                if yEnd >= tempYMin and yEnd <= tempYMax:
                    yEnd = yStart + yEnd
                    break
            tempCheck = False
            if self.tileList[yStart][xStart].isFloor != True:
                for y in range (yStart, yEnd):
                    for x in range (xStart, xEnd):
                        if self.tileList[y][x].isFloor or self.tileList[y - self.roomGap][x].isFloor or self.tileList[y + self.roomGap][x].isFloor or self.tileList[y][x - self.roomGap].isFloor or self.tileList[y][x + self.roomGap].isFloor:
                            tempCheck = True
                            tempNumber += 1
                            if tempNumber >= 20:
                                roomAmount -= 1
                                tempNumber = 0
                                quitEarly = True
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
                                self.tileList[y][x].isBossStart = True
                    roomAmount -= 1
        tempNumber = 1
        check1 = True
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
                        if check1 == False:
                            if axisTwo.roomNumber == axisOne.array[x] or axisTwo.isConnected == False:
                                breakout = False
                else:
                    breakout = False
                if breakout == True:
                    check1 = False
                    axisOne.isConnected = True
                    axisTwo.isConnected = True
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
                self.playerSprite = tempPlayer
                self.playerGroup.add(tempPlayer)
                self.playerX = self.tileList[pointy][pointx].x
                self.playerY = self.tileList[pointy][pointx].y
                for y in range(pointy - self.borderWidth, pointy + self.borderWidth):
                    for x in range(pointx - self.borderWidth, pointx + self.borderWidth):
                        self.tileList[y][x].isPlayer = True
                break

        if self.gameMode == "BOSS":
            while True:
                tempCheck = False
                pointx = int(random.random()*self.BOARDWIDTH)
                pointy = int(random.random()*self.BOARDHEIGHT)
                for y in range(pointy, pointy + 1):
                    for x in range(pointx, pointx + 1):
                        if self.tileList[y][x].isRoom == False or self.tileList[y][x].isBossStart == False or (self.tileList[y][x].isPlayer == True and quitEarly == False) or self.tileList[y][x].isEnemy == True or self.tileList[y][x].isWall == True:
                            tempCheck = True
                if tempCheck == False:
                    break
            tempEnemy= Enemy(self.TILESIZE * 2, self.tileList[pointy][pointx].left, self.tileList[pointy][pointx].top, self.Boss, 60, self.bossDamage, self.bossDamage *2, 400, self.bossHealth, True)
            tempEnemy.isBoss = True
            self.tileList[pointy][pointx].isChanged = True
            self.bossSprite = tempEnemy
            self.enemyGroup.add(tempEnemy)

        while True:
            if self.gameMode == "BOSS":
                enemyMax = self.bossMaxNumberOfEnemies
                enemyMin = self.bossMinNumberOfEnemies
            elif self.gameMode == "PORTAL":
                enemyMax = self.findMaxNumberOfEnemies
                enemyMin = self.findMinNumberOfEnemies
            else:
                enemyMax = self.maxNumberOfEnemies
                enemyMin = self.minNumberOfEnemies
            numberOfEnemies = int(random.random() * enemyMax + 1)
            if numberOfEnemies >= enemyMin and numberOfEnemies <= enemyMax:
                break
        tempCount = 0
        placedEnemy = False
        while numberOfEnemies > 0:
            pointx = int(random.random()*self.BOARDWIDTH)
            pointy = int(random.random()*self.BOARDHEIGHT)
            if self.tileList[pointy][pointx].isFloor == True and self.tileList[pointy][pointx].isPlayer == False and self.tileList[pointy][pointx].isChanged == False and self.tileList[pointy][pointx].isWall == False:
                while True:
                    tempHealth = int(random.random() * self.maxEnemyHealth + 1)
                    if tempHealth >= self.minEnemyHealth and tempHealth <= self.maxEnemyHealth:
                        break
                while True:
                    tempDamage = int(random.random() * self.maxEnemyDamage + 1)
                    if tempDamage >= self.minEnemyDamage and tempDamage <= self.maxEnemyDamage:
                        break
                tempEnemy= Enemy(self.TILESIZE, self.tileList[pointy][pointx].left, self.tileList[pointy][pointx].top, self.Enemy, 60, tempDamage, tempDamage*2, 800, tempHealth, False)
                self.tileList[pointy][pointx].isEnemy = True
                self.tileList[pointy][pointx].isChanged = True
                self.enemyGroup.add(tempEnemy)
                numberOfEnemies -= 1
                placedEnemy = True
            else:
                tempCount += 1
                if tempCount >= 50 and placedEnemy == True:
                    tempCount = 0
                    numberOfEnemies -= 1
        if self.gameMode == "PORTAL":
            while True:
                self.playerSprite.health = 450
                tempCheck = False
                pointx = int(random.random()* (self.BOARDWIDTH - 15)) + 7
                pointy = int(random.random()* (self.BOARDHEIGHT - 15)) + 7
                if self.tileList[pointy][pointx].isRoom == False or self.tileList[pointy][pointx].isWall == True or self.tileList[pointy][pointx].isChanged == True:
                    tempCheck = True
                for y in range(pointy - 6, pointy + 6):
                    for x in range(pointx - 6, pointx + 6):
                        if self.tileList[y][x].isPlayer == True:
                            tempCheck = True
                if tempCheck == False:
                    self.tileList[pointy][pointx].image = self.Portal
                    self.tileList[pointy][pointx].isPortal = True
                    self.portalSprite = self.tileList[pointy][pointx]
                    self.tileList[pointy][pointx].isChanged = True
                    break
        while True:
            numberOfPacks = int(random.random()*self.maxNumberHealthPack + 1)
            if numberOfPacks >= self.minNumberHealthPack and numberOfPacks <= self.maxNumberHealthPack:
                break
        tempCount = 0
        while numberOfPacks > 0:
            tempCheck = False
            pointx = int(random.random() * (self.BOARDWIDTH - 15)) + 7
            pointy = int(random.random() * (self.BOARDHEIGHT - 15)) + 7
            if self.tileList[pointy][pointx].isFloor == False or self.tileList[pointy][pointx].isPlayer == True or self.tileList[pointy][pointx].isWall == True or self.tileList[pointy][pointx].isChanged == True:
                tempCheck = True
            for y in range(pointy - 6, pointy + 6):
                for x in range(pointx - 6, pointx + 6):
                    if self.tileList[y][x].isHealthPack == True:
                        tempCheck = True
            if tempCheck == False:
                self.tileList[pointy][pointx].image = self.Healthpack
                self.tileList[pointy][pointx].isHealthPack = True
                self.tileList[pointy][pointx].isChanged = True
                numberOfPacks -= 1
            else:
                tempCount += 1
                if tempCount >= 50:
                    tempCount = 0
                    numberOfPacks -= 1
        while True:
            numberOfPacks = int(random.random()*self.maxNumberDamagePack + 1)
            if numberOfPacks >= self.minNumberDamagePack and numberOfPacks <= self.maxNumberDamagePack:
                break
        tempCount = 0
        while numberOfPacks > 0:
            tempCheck = False
            pointx = int(random.random() * (self.BOARDWIDTH - 15)) + 7
            pointy = int(random.random() * (self.BOARDHEIGHT - 15)) + 7
            if self.tileList[pointy][pointx].isFloor == False or self.tileList[pointy][pointx].isPlayer == True or self.tileList[pointy][pointx].isWall == True or self.tileList[pointy][pointx].isChanged == True:
                tempCheck = True
            for y in range(pointy - 6, pointy + 6):
                for x in range(pointx - 6, pointx + 6):
                    if self.tileList[y][x].isDamageBuff == True:
                        tempCheck = True
            if tempCheck == False:
                self.tileList[pointy][pointx].image = self.Damagepack
                self.tileList[pointy][pointx].isDamageBuff = True
                self.tileList[pointy][pointx].isChanged = True
                numberOfPacks -= 1
            else:
                tempCount += 1
                if tempCount >= 50:
                    tempCount = 0
                    numberOfPacks -= 1
        while True:
            numberOfMines = int(random.random()*self.maxNumberMines + 1)
            if numberOfMines >= self.minNumberMines and numberOfMines <= self.maxNumberMines:
                break
        tempCount = 0
        while numberOfMines > 0:
            tempCheck = False
            pointx = int(random.random() * (self.BOARDWIDTH - 15)) + 7
            pointy = int(random.random() * (self.BOARDHEIGHT - 15)) + 7
            if self.tileList[pointy][pointx].isRoom == False or self.tileList[pointy][pointx].isPlayer == True or self.tileList[pointy][pointx].isWall == True or self.tileList[pointy][pointx].isChanged == True:
                tempCheck = True
            for y in range(pointy - 6, pointy + 6):
                for x in range(pointx - 6, pointx + 6):
                    if self.tileList[y][x].isDamager == True:
                        tempCheck = True
            if tempCheck == False:
                    self.tileList[pointy][pointx].image = self.Damager
                    self.tileList[pointy][pointx].isDamager = True
                    self.tileList[pointy][pointx].isChanged = True
                    numberOfMines -= 1
            else:
                tempCount += 1
                if tempCount >= 50:
                    tempCount = 0
                    numberOfMines -= 1
        tempCount = 0
        if self.gameMode == "ENEMY" and self.spawningTraps == True:
            leave = False
            while leave == False:
                tempCheck = False
                pointx = int(random.random() * (self.BOARDWIDTH - 15)) + 7
                pointy = int(random.random() * (self.BOARDHEIGHT - 15)) + 7
                if self.tileList[pointy][pointx].isRoom == False or self.tileList[pointy][pointx].isPlayer == True or self.tileList[pointy][pointx].isWall == True or self.tileList[pointy][pointx].isChanged == True:
                    tempCheck = True
                if tempCheck == False:
                    self.tileList[pointy][pointx].image = self.Button
                    self.tileList[pointy][pointx].isButton = True
                    self.tileList[pointy][pointx].isChanged = True
                    self.tileList[pointy][pointx].clickAmount = self.clickAmount
                    self.buttonSprite = self.tileList[pointy][pointx]
                    while True:
                        numberofTraps = int(random.random()*self.maxNumberTraps + 1)
                        if numberofTraps >= self.minNumberTraps and numberofTraps <= self.maxNumberTraps:
                            break
                    while numberofTraps > 0:
                        tempY = int(random.random() * 4 + 1)
                        if int(random.random() * 2 + 1) == 2:
                            tempY *= - 1
                        tempX = int(random.random() * 4 + 1)
                        if int(random.random() * 2 + 1) == 2:
                            tempX *= - 1
                        y = pointy + tempY
                        x = pointx + tempX
                        if self.tileList[y][x].isRoom == True and self.tileList[y][x].isPlayer == False and self.tileList[y][x].isWall == False and self.tileList[y][x].isChanged == False:
                            self.tileList[y][x].isCharge = True
                            self.tileList[y][x].image = self.Charge
                            self.tileList[y][x].isChanged = True
                            self.sparkGroup.add(self.tileList[y][x])
                            numberofTraps -= 1
                    leave = True
                else:
                    tempCount += 1
                    if tempCount >= 70:
                        break
        elif self.gameMode == "PORTAL" and self.spawningTraps == True:
            leave = False
            while leave == False:
                tempCheck = False
                pointx = int(random.random() * (self.BOARDWIDTH - 15)) + 7
                pointy = int(random.random() * (self.BOARDHEIGHT - 15)) + 7
                for y in range(pointy - 1, pointy + 2):
                    for x in range(pointx - 1, pointx + 2):
                        if self.tileList[y][x].isRoom == False or self.tileList[y][
                            x].isPlayer == True or self.tileList[y][x].isWall == True or \
                                self.tileList[y][x].isChanged == True:
                            tempCheck = True
                if tempCheck == False:
                    self.tileList[pointy][pointx].clickAmount = self.clickAmount2
                    self.tileList[pointy][pointx].image = self.Button2
                    self.tileList[pointy][pointx].isButton = True
                    self.tileList[pointy][pointx].isChanged = True
                    self.buttonSprite = self.tileList[pointy][pointx]
                    self.tileList[pointy - 1][pointx - 1].image = self.Corner
                    self.tileList[pointy - 1][pointx - 1].laserImage = self.CornerL
                    self.tileList[pointy - 1][pointx + 1].image = pygame.transform.rotate(self.Corner, -90)
                    self.tileList[pointy - 1][pointx + 1].laserImage = pygame.transform.rotate(self.CornerL, -90)
                    self.tileList[pointy + 1][pointx - 1].image = pygame.transform.rotate(self.Corner, 90)
                    self.tileList[pointy + 1][pointx - 1].laserImage = pygame.transform.rotate(self.CornerL, 90)
                    self.tileList[pointy + 1][pointx + 1].image = pygame.transform.rotate(self.Corner, 180)
                    self.tileList[pointy + 1][pointx + 1].laserImage = pygame.transform.rotate(self.CornerL, 180)
                    self.tileList[pointy - 1][pointx].laserImage = self.SideL
                    self.tileList[pointy + 1][pointx].laserImage = pygame.transform.rotate(self.SideL, 180)
                    self.tileList[pointy][pointx - 1].laserImage = pygame.transform.rotate(self.SideL, 90)
                    self.tileList[pointy][pointx + 1].laserImage = pygame.transform.rotate(self.SideL, -90)
                    self.sparkGroup.add(self.tileList[pointy - 1][pointx - 1])
                    self.sparkGroup.add(self.tileList[pointy - 1][pointx + 1])
                    self.sparkGroup.add(self.tileList[pointy + 1][pointx - 1])
                    self.sparkGroup.add(self.tileList[pointy + 1][pointx + 1])
                    self.sparkGroup.add(self.tileList[pointy - 1][pointx])
                    self.sparkGroup.add(self.tileList[pointy + 1][pointx])
                    self.sparkGroup.add(self.tileList[pointy][pointx - 1])
                    self.sparkGroup.add(self.tileList[pointy][pointx + 1])
                    leave = True
                else:
                    tempCount += 1
                    if tempCount >= 70:
                        break
    def drawBoard(self):
        if self.dead == True:
            self.DISPLAYSURF.fill((0,0,0))
            self.healthObj = pygame.font.Font('freesansbold.ttf', 30)
            clockSurfaceObj = self.healthObj.render("Game Over!", True, (255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (139, int(self.DISPLAYSURF.get_width()/2 - 50)))
            clockSurfaceObj = self.healthObj.render("You made it to level " + str(self.levelNumber), True, (255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (73, int(self.DISPLAYSURF.get_width() / 2 - 15)))
            clockSurfaceObj = self.healthObj.render("Click Enter to Restart", True, (255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (72, int(self.DISPLAYSURF.get_width() / 2 + 20)))
        elif self.moveOn == True:
            self.DISPLAYSURF.fill((0,0,0))
            self.healthObj = pygame.font.Font('freesansbold.ttf', 30)
            clockSurfaceObj = self.healthObj.render("You won that level!", True, (255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (93, int(self.DISPLAYSURF.get_width()/2 - 40)))
            clockSurfaceObj = self.healthObj.render("Click Enter to Move on", True, (255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (63, int(self.DISPLAYSURF.get_width() / 2 - 5)))
        else:
            pygame.sprite.Group.draw(self.backgroundGroup, self.boardSurface)
            pygame.sprite.Group.draw(self.playerSprite.WeaponGroup, self.boardSurface)
            pygame.sprite.Group.draw(self.playerGroup, self.boardSurface)
            pygame.sprite.Group.draw(self.enemyGroup, self.boardSurface)
            pygame.sprite.Group.draw(self.playerSprite.laserGroup, self.boardSurface)
            self.DISPLAYSURF.blit(self.boardSurface, (int(self.DISPLAYWIDTH/ 2) * self.TILESIZE - (self.playerX*self.TILESIZE), int(self.DISPLAYHEIGHT/2) * self.TILESIZE - (self.playerY*self.TILESIZE)))
            clockSurfaceObj = self.healthObj.render("Health: " + str(self.playerSprite.health), True, (255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (330, 8))
            clockSurfaceObj = self.healthObj.render("Shots Left: " + str(int(self.playerSprite.harmedCount/5)), True, (255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (318, 31))
            clockSurfaceObj = self.healthObj.render("Level: " + str(self.levelNumber), True,(255, 255, 255))
            self.DISPLAYSURF.blit(clockSurfaceObj, (8, 8))
            if self.gameMode == "ENEMY":
                clockSurfaceObj = self.healthObj.render("Enemies Left: " + str(len(self.enemyGroup)), True,
                                                        (255, 255, 255))
                self.DISPLAYSURF.blit(clockSurfaceObj, (8, 31))
            elif self.gameMode == "BOSS":
                if self.bossSprite.health < 0:
                    self.bossSprite.health = 0
                clockSurfaceObj = self.healthObj.render("Boss Health: " + str(self.bossSprite.health), True,
                                                        (255, 255, 255))
                self.DISPLAYSURF.blit(clockSurfaceObj, (8, 31))
            elif self.gameMode == "PORTAL":
                dirvect = pygame.math.Vector2(self.playerSprite.rect.x - self.portalSprite.rect.x, self.playerSprite.rect.y - self.portalSprite.rect.y)
                dirvect.y = abs(dirvect.y)
                dirvect.x = abs(dirvect.x)
                clockSurfaceObj = self.healthObj.render("Portal Distance: " + str(dirvect), True, (255, 255, 255))
                self.DISPLAYSURF.blit(clockSurfaceObj, (8, 31))
    def restart(self):
        self.healthObj = pygame.font.Font('freesansbold.ttf', 20)
        self.createdBoard = False
        self.tileList = []
        self.centerArray = []
        self.centerArrayNumber = 0
        self.playerGroup = pygame.sprite.Group()
        self.backgroundGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.playerX = 0
        self.playerY = 0
        self.playerSprite = pygame.sprite
        self.playable = False
        self.DISPLAYSURF = pygame.display.set_mode((self.DISPLAYWIDTH * self.TILESIZE, self.DISPLAYHEIGHT * self.TILESIZE))
        self.boardSurface = pygame.Surface((self.BOARDWIDTH * self.TILESIZE, self.BOARDHEIGHT * self.TILESIZE))
        self.dead = False
        self.moveOn = False
        self.canGoUp = False
        self.canGoDown = False
        self.canGoRight = False
        self.canGoLeft = False
        self.onPortal = False
        self.sparkGoing = False
        self.onButton = False
        self.buttonTick = 0
    def move(self):
        tempOnButton = False
        enemySprites = self.enemyGroup.sprites()
        for x in range(len(enemySprites)):
            if enemySprites[x].isBoss == False:
                enemySprites[x].moveTowardsPlayer(self.playerSprite, self.backgroundGroup, self.borderWidth, self.maxFollowDistance, self.enemyGroup)
            else:
                enemySprites[x].bossMoveTowardsPlayer(self.playerSprite, self.backgroundGroup, 3)
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
                if spriteGroup[x].isPortal == True:
                    self.onPortal = True
                if spriteGroup[x].isHealthPack == True and ((self.gameMode != "PORTAL" and self.playerSprite.health < 999) or (self.gameMode == "PORTAL" and self.playerSprite.health < 450)):
                    self.playerSprite.health += 50
                    if self.gameMode == "PORTAL" and self.playerSprite.health > 450:
                        self.playerSprite.health = 450
                    elif self.playerSprite.health > 999:
                        self.playerSprite.health = 999
                    spriteGroup[x].image = self.Floor
                    spriteGroup[x].isHealthPack = False
                if spriteGroup[x].isDamageBuff == True:
                    self.playerSprite.swordDamage += 20
                    self.playerSprite.laserDamage += 20
                    spriteGroup[x].image = self.Floor
                    spriteGroup[x].isDamageBuff = False
                if spriteGroup[x].isDamager == True:
                    self.playerSprite.health -= 50
                if spriteGroup[x].isButton == True and spriteGroup[x].clickAmount > 0:
                    if self.onButton == True:
                        tempOnButton = True
                    else:
                        self.onButton = True
                        tempOnButton = True
                        self.sparkGoing = True
                        self.buttonTick = 0
            if tempOnButton == False:
                self.onButton = False
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
                if spriteGroup[x].isPortal == True:
                    self.onPortal = True
                if spriteGroup[x].isHealthPack == True and ((self.gameMode != "PORTAL" and self.playerSprite.health < 999) or (self.gameMode == "PORTAL" and self.playerSprite.health < 450)):
                    self.playerSprite.health += 50
                    if self.gameMode == "PORTAL" and self.playerSprite.health > 450:
                        self.playerSprite.health = 450
                    elif self.playerSprite.health > 999:
                        self.playerSprite.health = 999
                    spriteGroup[x].image = self.Floor
                    spriteGroup[x].isHealthPack = False
                if spriteGroup[x].isDamageBuff == True:
                    self.playerSprite.swordDamage += 20
                    self.playerSprite.laserDamage += 20
                    spriteGroup[x].image = self.Floor
                    spriteGroup[x].isDamageBuff = False
                if spriteGroup[x].isDamager == True:
                    self.playerSprite.health -= 50
                if spriteGroup[x].isButton == True and spriteGroup[x].clickAmount > 0:
                    if self.onButton == True:
                        tempOnButton = True
                    else:
                        self.onButton = True
                        tempOnButton = True
                        self.sparkGoing = True
                        self.buttonTick = 0
            if tempOnButton == False:
                self.onButton = False
    def increaseDifficulty(self):
        if self.levelNumber % 2 == 0:
            if self.maxEnemyDamage < 900:
                self.minEnemyDamage += 10
                self.maxEnemyDamage += 10
            self.minEnemyHealth += 10
            self.maxEnemyHealth += 10
            self.bossHealth += 10
            if self.bossDamage < 900:
                self.bossDamage += 10
        if self.levelNumber % 10 == 0:
            if self.levelNumber <= 40:
                self.maxFollowDistance += 1
            if self.levelNumber <= 20:
                self.minNumberMines += 1
                self.maxNumberMines += 1
        if self.levelNumber % 5 == 0:
            if self.levelNumber <= 30:
                self.hallWayRandomMove += 1
                self.minNumberOfEnemies += 1
                self.maxNumberOfEnemies += 1
                self.findMinNumberOfEnemies += 1
                self.findMaxNumberOfEnemies += 1
            if self.levelNumber <= 5:
                self.minHallwayLength -= 1
            if self.levelNumber <= 10:
                self.minNumberTraps -= 1
                self.maxNumberTraps -= 1
                self.clickAmount -= 1
        if self.levelNumber == 15:
            self.spawningTraps = False
            self.minNumberHealthPack -= 1
            self.maxNumberHealthPack -= 1
            self.minNumberDamagePack -= 1
            self.maxNumberDamagePack -= 1
        if self.levelNumber == 30:
            self.maxNumberHealthPack -= 1
            self.maxNumberDamagePack -= 1
    def reset(self):
        self.minXLength = 4
        self.maxXlength = 8
        self.minYLength = 4
        self.maxYlength = 8
        self.roomNumberMin = 6
        self.roomNumberMax = 10
        self.bossMinXLength = 11
        self.bossMaxXlength = 13
        self.bossMinYLength = 11
        self.bossMaxYlength = 13
        self.bossRoomNumberMin = 3
        self.bossRoomNumberMax = 4
        self.hallWayRandomMove = 1
        self.minHallwayLength = 4
        self.chanceOfDoubleHallway = 0
        self.roomGap = 2
        # Collectables
        self.minNumberHealthPack = 2
        self.maxNumberHealthPack = 3
        self.minNumberDamagePack = 2
        self.maxNumberDamagePack = 3
        self.minNumberMines = 2
        self.maxNumberMines = 3
        self.minNumberTraps = 3
        self.maxNumberTraps = 5
        self.clickAmount = 3
        self.clickAmount2 = 1
        # Enemy Config
        self.maxFollowDistance = 10
        self.minNumberOfEnemies = 6
        self.maxNumberOfEnemies = 10
        self.bossMinNumberOfEnemies = 2
        self.bossMaxNumberOfEnemies = 4
        self.findMinNumberOfEnemies = 5
        self.findMaxNumberOfEnemies = 7
        self.minEnemyDamage = 10
        self.maxEnemyDamage = 30
        self.minEnemyHealth = 30
        self.maxEnemyHealth = 50
        self.bossHealth = 280
        self.bossDamage = 10
        self.spawningTraps = True

if __name__ == '__main__':
    game = main()
    asyncio.run(game.main())
