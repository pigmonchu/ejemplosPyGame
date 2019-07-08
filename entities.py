import pygame as pg
from pygame.locals import *
import random
import sys, os

def memberinList(m, l):
    try:
        l.index(m)
        return True
    except:
        return False

class Ball(pg.sprite.Sprite):
    color = (0, 0, 255)
    dirx = 1
    diry = 1
    velocidadx = 5
    velocidady = 5

    def __init__(self, x, y, w=16, h=16):
        self.w = w
        self.h = h
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def changeY(self):
        self.diry = -self.diry
        self.velocidady = max(2, min(random.randint(self.velocidady // 2, self.velocidady * 2), 10))
        self.rect.y = self.rect.y + (self.rect.h)*self.diry

    def changeX(self):
        self.dirx = -self.dirx
        self.velocidadx = max(2, min(random.randint(self.velocidadx // 2, self.velocidadx * 2), 10))
        self.rect.x = self.rect.x + (self.rect.w)*self.dirx

    def update(self, dt=None):
        self.rect.x += self.dirx * self.velocidadx
        self.rect.y += self.diry * self.velocidady

        if self.rect.x >= 800 or self.rect.x <= 0:
            self.changeX()
        if self.rect.y >= 600 or self.rect.y <= 0:
            self.changeY()

        self.image.fill(self.color)

    def comprobarChoque(self, spriteGroup, borra=False):
        candidates = pg.sprite.spritecollide(self, spriteGroup, borra)
        if memberinList(self, candidates) and len(candidates) == 1:
            return

        if len(candidates)>0:    
            if random.choice([0,1]):
                self.dirx = -self.dirx
                self.velocidadx = random.randrange(5, 15)
            else:
                self.diry = -self.diry
                self.velocidady = random.randrange(5, 15)

    def choqueResponse(self, obstaculo):
        distR = self.rect.right - obstaculo.rect.left
        distL = obstaculo.rect.right - self.rect.left 
        distT = self.rect.top - obstaculo.rect.bottom
        distB = obstaculo.rect.top-self.rect.bottom   


        if distR < 0 and abs(distR) < self.rect.w:
            self.rect.right = obstaculo.rect.left-1 
            self.dirx = -self.dirx
        
        if distL < 0 and abs(distL) < self.rect.w:
            self.rect.left = obstaculo.rect.right + 1
            self.dirx = -self.dirx

        if distT < 0 and abs(distT) < self.rect.h:
            self.rect.top = obstaculo.rect.bottom + 1
            self.diry = -self.diry

        if distB < 0 and abs(distB) < self.rect.h:
            self.rect.bottom = obstaculo.rect.top - 1
            self.diry = -self.diry


    def comprobarChoque(self, spriteGroup, borra=False):
        candidates = pg.sprite.spritecollide(self, spriteGroup, borra)
        if memberinList(self, candidates):
            #Evitamos los choques conmigo mismo 
            candidates.remove(self)

        for obstaculo in candidates:
            self.choqueResponse(obstaculo)


class Wall(pg.sprite.Sprite):
    color = (255, 125, 0)
    dirx = random.choice([-1, 1])
    diry = random.choice([-1, 1])
    velocidadx = 3
    velocidady = 3

    def __init__(self, x, y, mygroup=None, w=200, h=16):
        self.w = w
        self.h = h
        self.mygroup = mygroup
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.reasigna()

    def reasigna(self):
        if self.mygroup == None:
            return
        cols = pg.sprite.spritecollide(self, self.mygroup, False)
        if len(cols) > 0:
            self.rect.x = random.randint(0,600)
            self.rect.y = random.randint(0, 584)
            self.reasigna()
        else:
            self.mygroup.add(self)


class Explosion(pg.sprite.Sprite):
    def __init__(self, posx, posy):
        pg.sprite.Sprite.__init__(self)
        self.sprite_sheet = pg.image.load(os.getcwd()+'/assets/images/explode.png').convert_alpha()
        self.width = 128
        self.height = 128
        self.how_many = 16
        self.animation_time = 30

        self.images = [] # Aquí irán las 16 imagenes de la explosión

        x = 0 # Utilizaremos esto para cortar la imágen original en 16 cuadrados de 128 x 128
        y = 0

        for i in range(self.how_many):
            image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha() # Creo Lienzo de 128x128
            image.blit(self.sprite_sheet, (0,0), (x, y, self.width, self.height)) # Relleno con fragmenteo de 128x128 de la imágen original
            self.images.append(image) # guardo en self.images
            x+=self.width # Avanzo el punto de corte

        self.index = random.randint(0,15)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index +=1
            if self.index >= len(self.images):
                self.index = 0
                self.rect.x = random.randint(0,672)
                self.rect.y = random.randint(0, 472)
            self.image = self.images[self.index]

class Robot(pg.sprite.Sprite):
    __directions__ = ('up', 'down', 'left', 'right')
    def __init__(self, posx, posy):
        pg.sprite.Sprite.__init__(self)

        self.width = 64
        self.height = 64
        self.how_many = 16
        self.animation_time = 10
        self.bolsa = []

        self.images = [] # Aquí iran 4 listas de 16 imágenes una por dirección de avance UP, DOWN, LEFT, RIGHT
        for i in range(4):
            direct = []
            x = 0
            y = 0
            img = pg.image.load(os.getcwd()+'/assets/images/{}.png'.format(self.__directions__[i])).convert_alpha()
            for j in range(self.how_many):
                image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
                image.blit(img, (0,0), (x, y, self.width, self.height))
                direct.append(image)
                x+=self.width
            self.images.append(direct)

        self.direction = 2 #left
        self.index = 0

        self.image = self.images[self.direction][self.index]
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy 
        self.current_time = 0
       

    def update(self, dt):
        self.current_time += dt

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index += 1
            if self.index >= len(self.images[self.direction]):
                self.index = 0
            self.image = self.images[self.direction][self.index]

        if self.direction == 0:
            self.rect.y -= 10
        elif self.direction == 1:
            self.rect.y += 10
        elif self.direction == 2:
            self.rect.x -= 10
        elif self.direction == 3:
            self.rect.x += 10
        else:
            pass

        if self.rect.x <= 0:
            self.direction = 3
        if self.rect.x >= 800-self.rect.w:
            self.direction = 2

        if self.rect.y <=0:
            self.direction = 1
        if self.rect.y >= 600-self.rect.h:
            self.direction = 0

        for micosa in self.bolsa:
            micosa.rect.midbottom = self.rect.midtop

    def cogerAlTocar(self, spriteGroup):
        candidates = pg.sprite.spritecollide(self, spriteGroup, False)
        for obstaculo in candidates:
            if obstaculo not in self.bolsa:
                self.bolsa.append(obstaculo)

