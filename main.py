#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import math
from os import path
from constants import *
#from background import *
#from explosion import *
#from weapons import *


# Define Screen paramters
WIDTH = 800
HEIGHT = 600
FPS = 60

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set folder
folder = {}
folder['gfx'] = path.join(path.dirname(__file__), 'data/gfx')
folder['sounds'] = path.join(path.dirname(__file__), 'data/sounds')
folder['fonts'] = path.join(path.dirname(__file__), 'data/fonts')

# initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)# | pygame.FULLSCREEN)
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

font_name = folder['fonts'] + '/PressStart2P-Regular.ttf'
###############################


class BackgroundVerticalScroll(object):
    def __init__(self, screen, background, speedy):
        self.background = background
        self.w, self.h = self.background.get_size()
        self.speedy = speedy
        self.screen = screen
        
        self.x = 0
        self.y = 0
        self.x1 = 0
        self.y1 = -self.h
    
    
    def update(self):
        self.y1 += self.speedy
        self.y += self.speedy
        
        self.screen.blit(self.background, (self.x, self.y))
        self.screen.blit(self.background, (self.x1, self.y1))
        
        if self.y > self.h:
            self.y = -self.h
        if self.y1 > self.h:
            self.y1 = -self.h


class Explosion(pygame.sprite.Sprite):
    def __init__(self, explosionAnim, center, explosionType):
        pygame.sprite.Sprite.__init__(self)
        self.explosionType = explosionType
        self.explosionAnim = explosionAnim
        self.image = self.explosionAnim[self.explosionType][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 65


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosionAnim[self.explosionType]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosionAnim[self.explosionType][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = weaponSprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.player = player
        self.allspritesGroup = allspritesGroup
        self.bulletGroup = bulletGroup
        self.bulletSprite = bulletSprite
        
        ## place the bullet according to the current position of the player
        self.rect.bottom = 0
        self.rect.centerx = 0
        
        self.lastshot = pygame.time.get_ticks()
        self.shotdelay = 0
        self.power = 0
        
        self.speedx = 0
        self.speedy = 0
        self.accelx = 0
        self.accely = 0
        
    def update(self):
        self.rect.bottom = self.player.rect.top
        self.rect.centerx = self.player.rect.left
        


## defines the sprites for weapons
class Weapon_Standard(pygame.sprite.Sprite):
    def __init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup):
        #super(Weapon, self).__init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup)
        
        pygame.sprite.Sprite.__init__(self)
        self.image = weaponSprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.player = player
        self.allspritesGroup = allspritesGroup
        self.bulletGroup = bulletGroup
        self.bulletSprite = bulletSprite
        
        ## place the bullet according to the current position of the player
        self.rect.bottom = 0
        self.rect.centerx = 0
        
        self.lastshot = pygame.time.get_ticks()
        self.shotdelay = 0
        self.power = 0
        
        self.speedx = 0
        self.speedy = 0
        self.accelx = 0
        self.accely = 0
        
        ## place the bullet according to the current position of the player
        self.rect.bottom = self.player.rect.top
        self.rect.centerx = self.player.rect.centerx
        self.shotdelay = 200
        self.power = 1
        self.speedy = -10


    def update(self):
        self.rect.bottom = self.player.rect.top
        self.rect.centerx = self.player.rect.centerx


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastshot > self.shotdelay:
            self.lastshot = now

            bullet = Bullet(self.rect.centerx, self.rect.centery, self.speedx, self.speedy, self.accelx, self.accely, self.bulletSprite)
            self.allspritesGroup.add(bullet)
            self.bulletGroup.add(bullet)
            
            sounds['laser'].play()



class Weapon_Rocket(pygame.sprite.Sprite):
    def __init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup):
#        super(Weapon, self).__init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup)
        pygame.sprite.Sprite.__init__(self)
        self.image = weaponSprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.player = player
        self.allspritesGroup = allspritesGroup
        self.bulletGroup = bulletGroup
        self.bulletSprite = bulletSprite
        
        ## place the bullet according to the current position of the player
        self.rect.bottom = 0
        self.rect.centerx = 0
        
        self.lastshot = pygame.time.get_ticks()
        self.shotdelay = 0
        self.power = 0
        
        self.speedx = 0
        self.speedy = 0
        self.accelx = 0
        self.accely = 0
       
        ## place the bullet according to the current position of the player
        self.rect.bottom = self.player.rect.bottom
        self.rect.centerx = self.player.rect.centerx
        self.shotdelay = 400
        self.power = 10
        self.speedx = 5
        self.speedy = -2
        self.accely = -0.5


    def update(self):
        self.rect.bottom = self.player.rect.bottom
        self.rect.centerx = self.player.rect.centerx


    def shoot(self):
        if self.player.bullets == 0:
            return
        
        now = pygame.time.get_ticks()
        if now - self.lastshot > self.shotdelay:
            self.lastshot = now

            bullet1 = Bullet(self.rect.left, self.rect.centery, -self.speedx, self.speedy, self.accelx, self.accely, self.bulletSprite)
            bullet2 = Bullet(self.rect.right, self.rect.centery, self.speedx, self.speedy, self.accelx, self.accely, self.bulletSprite)
            self.allspritesGroup.add(bullet1)
            self.allspritesGroup.add(bullet2)
            self.bulletGroup.add(bullet1)
            self.bulletGroup.add(bullet2)
            
            self.player.decreaseBullets(2)
            
            sounds['rocket'].play()


class Weapon_Back(pygame.sprite.Sprite):
    def __init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup):
        #super(Weapon, self).__init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup)
        
        pygame.sprite.Sprite.__init__(self)
        self.image = weaponSprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.player = player
        self.allspritesGroup = allspritesGroup
        self.bulletGroup = bulletGroup
        self.bulletSprite = bulletSprite
        
        ## place the bullet according to the current position of the player
        self.rect.bottom = 0
        self.rect.centerx = 0
        
        self.lastshot = pygame.time.get_ticks()
        self.shotdelay = 0
        self.power = 0
        
        self.speedx = 0
        self.speedy = 0
        self.accelx = 0
        self.accely = 0

        ## place the bullet according to the current position of the player
        self.rect.bottom = self.player.rect.bottom
        self.rect.centerx = self.player.rect.centerx
        self.shotdelay = 100
        self.power = 1
        self.speedy = 8


    def update(self):
        self.rect.bottom = self.player.rect.bottom
        self.rect.centerx = self.player.rect.centerx


    def shoot(self):
        if self.player.bullets == 0:
            return

        now = pygame.time.get_ticks()
        if now - self.lastshot > self.shotdelay:
            self.lastshot = now

            bullet = Bullet(self.rect.centerx, self.rect.centery, self.speedx, self.speedy, self.accelx, self.accely, self.bulletSprite)
            self.allspritesGroup.add(bullet)
            self.bulletGroup.add(bullet)
            self.player.decreaseBullets(1)
            

class Weapon_Side(pygame.sprite.Sprite):
    def __init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup):
#        super(Weapon, self).__init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup)
 
        pygame.sprite.Sprite.__init__(self)
        self.image = weaponSprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.player = player
        self.allspritesGroup = allspritesGroup
        self.bulletGroup = bulletGroup
        self.bulletSprite = bulletSprite
        
        ## place the bullet according to the current position of the player
        self.rect.bottom = 0
        self.rect.centerx = 0
        
        self.lastshot = pygame.time.get_ticks()
        self.shotdelay = 0
        self.power = 0
        
        self.speedx = 0
        self.speedy = 0
        self.accelx = 0
        self.accely = 0

        ## place the bullet according to the current position of the player
        self.rect.bottom = self.player.rect.bottom
        self.rect.centerx = self.player.rect.centerx
        self.shotdelay = 300
        self.power = 1
        self.speedx = -10


    def update(self):
        self.rect.bottom = self.player.rect.bottom
        self.rect.centerx = self.player.rect.centerx


    def shoot(self):
        if self.player.bullets == 0:
            return

        now = pygame.time.get_ticks()
        if now - self.lastshot > self.shotdelay:
            self.lastshot = now

            bullet1 = Bullet(self.rect.centerx, self.rect.centery, -self.speedx, self.speedy, self.accelx, self.accely, self.bulletSprite)
            bullet2 = Bullet(self.rect.centerx, self.rect.centery, self.speedx, self.speedy, self.accelx, self.accely, self.bulletSprite)
            self.allspritesGroup.add(bullet1)
            self.allspritesGroup.add(bullet2)
            self.bulletGroup.add(bullet1)
            self.bulletGroup.add(bullet2)
            
            self.player.decreaseBullets(2)



class Weapon_Enemy_Standard(pygame.sprite.Sprite):
    def __init__(self, enemy, weaponSprite, allspritesGroup, bulletSprite, bulletGroup):
#        super(Weapon, self).__init__(self, player, weaponSprite, allspritesGroup, bulletSprite, bulletGroup)
 
        pygame.sprite.Sprite.__init__(self)
        self.image = weaponSprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.enemy = enemy
        self.allspritesGroup = allspritesGroup
        self.bulletGroup = bulletGroup
        self.bulletSprite = bulletSprite
        
        ## place the bullet according to the current position of the enemy
        self.rect.bottom = 0
        self.rect.centerx = 0
        
        self.lastshot = pygame.time.get_ticks()
        self.shotdelay = 0
        self.power = 0
        
        self.speedx = 0
        self.speedy = 0
        self.accelx = 0
        self.accely = 0

        ## place the bullet according to the current position of the enemy
        self.rect.bottom = self.enemy.rect.bottom
        self.rect.centerx = self.enemy.rect.centerx
        self.power = 1
        self.speedy = 8


    def update(self):
        self.rect.bottom = self.enemy.rect.bottom
        self.rect.centerx = self.enemy.rect.centerx


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.speedx, self.speedy, self.accelx, self.accely, self.bulletSprite)
        self.allspritesGroup.add(bullet)
        self.bulletGroup.add(bullet)
            


class Player(pygame.sprite.Sprite):
    def __init__(self, startPositionX, startPositionY):
        pygame.sprite.Sprite.__init__(self)
        
        ## scale the player img down
        self.image = sprites['player']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = startPositionX
        self.rect.bottom = startPositionY
        self.speedx = 0
        self.speedy = 0
        self.weapons = []
        self.lives = 3
        self.shield = 100
        self.hidden = False
        self.age = 0
        self.buddyCount = 0
        self.bullets = 500
        self.hide_timer = pygame.time.get_ticks()
        
        
    def addBuddy(self, buddy):
        if self.buddyCount == 0:
            self.buddyCount = 1
            self.buddy = buddy
            all_sprites.add(buddy)
            buddies.add(buddy)
        
        
    def clearBuddies(self):
        if self.buddyCount == 1:
            self.buddy.kill()
            self.buddyCount = 0
        
    
    def addWeapon(self, weapon):
        self.weapons.append(weapon)
        all_sprites.add(weapon)
        
    
    def clearWeapons(self):
        for weapon in self.weapons:
            weapon.kill()
            
        self.weapons = []
        
    
    def decreaseBullets(self, number):
        self.bullets -= number
        if self.bullets < 0:
            self.bullets = 0
        

    def increaseBullets(self, number):
        self.bullets += number
        if self.bullets > 500:
            self.bullets = 500

    def update(self):
        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30
            
        self.speedx = 0
        self.speedy = 0
        # then we have to check whether there is an event hanlding being done for the arrow keys being pressed 

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()
        
        #Fire weapons
        if keystate[pygame.K_LCTRL]:
            self.shoot()

        #Handle keys to move ship
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        elif keystate[pygame.K_DOWN]:
            self.speedy = 8
            
        ## check for the borders at the left and right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
        if self.rect.top < 0:
            self.rect.top = 0
    
        self.rect.x += self.speedx
        self.rect.y += self.speedy


    def shoot(self):
        for weapon in self.weapons:
            weapon.shoot()
            

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, accelx, accely, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        ## place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedx = speedx
        self.speedy = speedy
        self.accelx = accelx
        self.accely = accely


    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        self.speedx += self.accelx
        self.speedy += self.accely
        
        ## kill the sprite after it moves out of screen
        if self.speedy < 0:
            if self.rect.bottom < 0:
                self.kill()
        
        if self.speedy > 0:
            if self.rect.top > HEIGHT:
                self.kill()
                
        if self.speedx < 0:
            if self.rect.left < 0:
                self.kill()
                
        if self.speedx > 0:
            if self.rect.right > WIDTH:
                self.kill()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(asteroidSprites)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)        ## for randomizing the speed of the Asteroid

        ## randomize the movements a little more 
        self.speedx = random.randrange(-3, 3)

        ## adding rotation to the asteroid element
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
        
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'weapon', 'buddy'])
        self.image = powSprites[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4


    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
            

            
class Buddy(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.image = pygame.image.load(path.join(folder['gfx'], 'buddy.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.phase = 3.1415
        self.angle = 0
        
    def update(self):
        self.angle += 0.2
        self.rect.top = -15 + self.player.rect.top + self.player.rect.height / 2 + 3 * 30 * math.sin(self.phase + self.angle)
        self.rect.left = -15 + self.player.rect.left + self.player.rect.width / 2 + 3 * 30 * math.cos(self.phase + self.angle)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, sprite, bezier):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.bezier = bezier
        self.point = 0
        self.last_shoot = pygame.time.get_ticks()
        self.weapons = []
        

    def update(self):
        self.shoot()
        self.rect.x = self.bezier[self.point][0]
        self.rect.y = self.bezier[self.point][1]
        
        self.point += 1
        if self.point >= len(self.bezier):
            self.kill()
            
            
    def shoot(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_shoot > random.randrange(50, 500): # in milliseconds
            self.last_shoot = time_now
            for weapon in self.weapons:
                weapon.shoot()            


    def addWeapon(self, weapon):
        self.weapons.append(weapon)
        all_sprites.add(weapon)
        
    
    def clearWeapons(self):
        for weapon in self.weapons:
            weapon.kill()
            
        self.weapons = []       



def draw_text(surf, text, size, x, y):
    ## selecting a cross platform font to display the score
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)       ## True denotes the font to be anti-aliased 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0 
    BAR_LENGTH = 100.0
    BAR_HEIGHT = 10
    fill = (pct / 100.0) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

    if pct < 0:
        pct = 0 
    BAR_LENGTH = 100.0
    BAR_HEIGHT = 10
    fill = (pct / 100.0) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_bullet_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0 
    BAR_LENGTH = 100.0
    BAR_HEIGHT = 10
    fill = (pct / 500.0) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def computeBezierPoints(vertices, numPoints = None):
    if numPoints is None:
        numPoints = 80
        
    if numPoints < 2 or len(vertices) != 4:
        return None
 
    result = []
 
    b0x = vertices[0][0]
    b0y = vertices[0][1]
    b1x = vertices[1][0]
    b1y = vertices[1][1]
    b2x = vertices[2][0]
    b2y = vertices[2][1]
    b3x = vertices[3][0]
    b3y = vertices[3][1]
 
    # Compute polynomial coefficients from Bezier points
    ax = -b0x + 3 * b1x + -3 * b2x + b3x
    ay = -b0y + 3 * b1y + -3 * b2y + b3y
 
    bx = 3 * b0x + -6 * b1x + 3 * b2x
    by = 3 * b0y + -6 * b1y + 3 * b2y
 
    cx = -3 * b0x + 3 * b1x
    cy = -3 * b0y + 3 * b1y
 
    dx = b0x
    dy = b0y
 
    # Set up the number of steps and step size
    numSteps = numPoints - 1 # arbitrary choice
    h = 1.0 / numSteps # compute our step size
 
    # Compute forward differences from Bezier points and "h"
    pointX = dx
    pointY = dy
 
    firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
    firstFDY = ay * (h * h * h) + by * (h * h) + cy * h
 
    secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
    secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)
 
    thirdFDX = 6 * ax * (h * h * h)
    thirdFDY = 6 * ay * (h * h * h)
 
    # Compute points at each step
    result.append((int(pointX), int(pointY)))
 
    for i in range(numSteps):
        pointX += firstFDX
        pointY += firstFDY
 
        firstFDX += secondFDX
        firstFDY += secondFDY
 
        secondFDX += thirdFDX
        secondFDY += thirdFDY
 
        result.append((int(pointX), int(pointY)))
 
    return result


def createBezierCurve(width, height, numControlPoints, numPoints):
    controlPoints = []
    for i in range(numControlPoints):
        x = random.randrange(0, width)
        y = random.randrange(0, height)

        #random start and endpoints
        p = random.randrange(0, 4)
        if i == 0 or i == numControlPoints - 1: 
            if p == 0:
                x = -30
            if p == 1:
                x = width + 30
            if p == 2:
                y = -30
            if p == 3:
                y = height + 30
                        
        controlPoints.append((x, y))
    
    points = computeBezierPoints(controlPoints)
    return points


###################################################
## Load all game images
background = BackgroundVerticalScroll(screen, pygame.image.load(path.join(folder['gfx'], 'starfield.png')).convert(), 2)

## sprites
sprites = {}
sprites['player'] = pygame.image.load(path.join(folder['gfx'], 'player.png')).convert_alpha()
sprites['enemy'] = pygame.image.load(path.join(folder['gfx'], 'schaedelbrecher.png')).convert_alpha()

sprites['bullet_standard'] = pygame.image.load(path.join(folder['gfx'], 'bullet_standard.png')).convert_alpha()
sprites['bullet_rocket'] = pygame.image.load(path.join(folder['gfx'], 'bullet_rocket.png')).convert_alpha()
sprites['bullet_back'] = pygame.image.load(path.join(folder['gfx'], 'bullet_back.png')).convert_alpha()

sprites['weapon_standard'] = pygame.image.load(path.join(folder['gfx'], 'weapon_standard.png')).convert_alpha()
sprites['weapon_rocket'] = pygame.image.load(path.join(folder['gfx'], 'weapon_rocket.png')).convert_alpha()
sprites['weapon_enemy_standard'] = pygame.image.load(path.join(folder['gfx'], 'weapon_standard.png')).convert_alpha()

player_mini_img = pygame.transform.scale(sprites['player'], (25, 19))
player_mini_img.set_colorkey(BLACK)

## player explosion
explosionAnim = {}
explosionAnim['player'] = []
for i in range(9):
    filename = 'explosion_player0{}.png'.format(i)
    img = pygame.image.load(path.join(folder['gfx'], filename)).convert()
    img.set_colorkey(BLACK)
    explosionAnim['player'].append(img)
    
asteroidSprites = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    asteroidSprites.append(pygame.image.load(path.join(folder['gfx'], image)).convert())


## load power ups
powSprites = {}
powSprites['shield'] = pygame.image.load(path.join(folder['gfx'], 'powerupShield.png')).convert()
powSprites['weapon'] = pygame.image.load(path.join(folder['gfx'], 'powerupWeapon.png')).convert()
powSprites['buddy'] = pygame.image.load(path.join(folder['gfx'], 'powerupBuddy.png')).convert()

## Load all game sounds
sounds = {}
sounds['laser'] = pygame.mixer.Sound(path.join(folder['sounds'], 'tilli_badung.ogg'))
sounds['rocket'] = pygame.mixer.Sound(path.join(folder['sounds'], 'rocket1.ogg'))
sounds['explosion_player'] = pygame.mixer.Sound(path.join(folder['sounds'], 'explosion_tilli1.ogg'))

pygame.mixer.music.set_volume(0.2)      ## simmered the sound down a little

## group all the sprites together for ease of update
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
buddies = pygame.sprite.Group()
player = Player(WIDTH / 2, HEIGHT - 10)
all_sprites.add(player)

player.addWeapon(Weapon_Standard(player, sprites['weapon_standard'], all_sprites, sprites['bullet_standard'], bullets))

## spawn a group of asteroid
asteroids = pygame.sprite.Group()
for i in range(3):
    asteroid_element = Asteroid()
    all_sprites.add(asteroid_element)
    asteroids.add(asteroid_element)

#### Score board variable
score = 0
weapon = 0
difficultyBoost = 0


### Control points that are later used to calculate the curve
bezier = createBezierCurve(WIDTH, HEIGHT, 4, 100)

#############################
## Game loop
running = True
while running:        
    #1 Process input/events
    clock.tick(FPS)
    for event in pygame.event.get():
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
            if event.key == pygame.K_e:
                bezier = createBezierCurve(WIDTH, HEIGHT, 4, 100)
                enemy = Enemy(sprites['enemy'], bezier)
                #enemy.addWeapon(Weapon_Enemy_Standard(enemy))
                enemy.addWeapon(Weapon_Enemy_Standard(enemy, sprites['weapon_enemy_standard'], all_sprites, sprites['bullet_standard'], bullets))
                all_sprites.add(enemy)

            if event.key == pygame.K_p:
                player.addWeapon(Weapon_Side(player, sprites['weapon_standard'], all_sprites, sprites['bullet_standard'], bullets))
                player.addWeapon(Weapon_Back(player, sprites['weapon_standard'], all_sprites, sprites['bullet_back'], bullets))
                player.addWeapon(Weapon_Rocket(player, sprites['weapon_rocket'], all_sprites, sprites['bullet_rocket'], bullets))
                player.addBuddy(Buddy(player))
                
    #2 Update
    all_sprites.update()
    
    #3 collision detection
    ## check if a bullet hit a asteroid
    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for hit in hits:
        score += 75 - hit.radius         ## give different scores for hitting big and small metoers
        expl = Explosion(explosionAnim, hit.rect.center, 'player')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
            
        asteroid_element = Asteroid()
        all_sprites.add(asteroid_element)
        asteroids.add(asteroid_element)

    ## check if a buddy hit a asteroid
    hits = pygame.sprite.groupcollide(asteroids, buddies, True, True)
    for hit in hits:
        player.buddyCount -= 1
        score += 50 - hit.radius         ## give different scores for hitting big and small metoers
        if score <= 0:
            score = 0
            
        expl = Explosion(explosionAnim, hit.rect.center, 'player')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
            
        asteroid_element = Asteroid()
        all_sprites.add(asteroid_element)
        asteroids.add(asteroid_element)

    ## check if a asteroid hits player
    hits = pygame.sprite.spritecollide(player, asteroids, True, pygame.sprite.collide_circle)        ## gives back a list, True makes the asteroid element disappear
    for hit in hits:
        player.shield -= hit.radius
        expl = Explosion(explosionAnim, hit.rect.center, 'player')
        all_sprites.add(expl)
        
        asteroid_element = Asteroid()
        all_sprites.add(asteroid_element)
        asteroids.add(asteroid_element)        
        
        if player.shield <= 0: 
            sounds['explosion_player'].play()
            death_explosion = Explosion(explosionAnim, player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
            
            player.clearWeapons()
            #player.addWeapon(Weapon_Standard(player))
            player.addWeapon(Weapon_Standard(player, sprites['weapon_standard'], all_sprites, sprites['bullet_standard'], bullets))

            player.clearBuddies()
            player.bullets = 500
            weapon = 0

    ## if the player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        
        if hit.type == 'weapon':
            weapon += 1
            
            player.increaseBullets(50)
            
            if weapon == 1:
                #player.addWeapon(Weapon_Back(player))
                player.addWeapon(Weapon_Back(player, sprites['weapon_standard'], all_sprites, sprites['bullet_back'], bullets))
                
            if weapon == 2:
                #player.addWeapon(Weapon_Rocket(player))
                player.addWeapon(Weapon_Rocket(player, sprites['weapon_rocket'], all_sprites, sprites['bullet_rocket'], bullets))
                
            if weapon == 3:
                #player.addWeapon(Weapon_Side(player))
                player.addWeapon(Weapon_Side(player, sprites['weapon_standard'], all_sprites, sprites['bullet_standard'], bullets))
                
        if hit.type == 'buddy':
                player.addBuddy(Buddy(player))


    ## boost difficulty
    if score > 0 and score // 5000 == difficultyBoost:
        asteroid_element = Asteroid()
        all_sprites.add(asteroid_element)
        asteroids.add(asteroid_element)
        difficultyBoost += 1
        

    #4 Draw/render
    screen.fill(BLACK)
    background.update()
    
    all_sprites.draw(screen)

    draw_text(screen, str(score), 18, WIDTH / 2, 10)     ## 10px down from the screen
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_bullet_bar(screen, 5, 20, player.bullets)

    # Draw lives
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    
    
    #pygame.draw.lines(screen, pygame.Color("red"), False, bezier, 2)
    

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()
