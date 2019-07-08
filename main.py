import pygame as pg
from pygame.locals import *
import sys, os, random
from entities import *

FPS = 60
BACKGROUND = (250, 250, 250)
BLANCO = (250, 250, 250)
NEGRO = (60, 60, 60)

GAMEOVER = '_go'
PARTIDA = '_game'

COLISION_INDIVIDUAL_OTRO_GRUPO = 1
COLISION_INDIVIDUAL_MI_GRUPO = 2
COGER_OBJETOS = 3
ANIMACIONES = 4
SALIR = 0

def centrar(long, en):
    return (en - long) // 2

class Game:
    clock = pg.time.Clock()
    robot = None
    treasure = None


    def __init__(self, width, height):

        self.config = {COLISION_INDIVIDUAL_OTRO_GRUPO: {'text': 'Colisión Individual. Yo contra otro grupo', 'key': K_1, 'method': self.individual_otro},
                COLISION_INDIVIDUAL_MI_GRUPO: {'text': 'Colisión Individual. Yo contra mi grupo', 'key': K_2, 'method':self.individual_mismo},
                COGER_OBJETOS: {'text': 'Agarrar objetos.', 'key': K_3, 'method': self.coger},
                ANIMACIONES: {'text': 'Animar sprites', 'key': K_4, 'method': self.anima}, 
                SALIR: {'text': 'Abandonar', 'key': K_0, 'method': None}

        }

        self.display = pg.display
        self.screen = self.display.set_mode((width, height))
        self.w = width
        self.h = height
        self.screen.fill(BACKGROUND)
        self.display.set_caption('Ejemplos')

        self.mainTitle = pg.font.Font(os.getcwd()+'/assets/fonts/fuente1.ttf', 30)
        self.Subtitle = pg.font.Font(os.getcwd()+'/assets/fonts/fuente1.ttf', 24)
        self.normalText = pg.font.Font(os.getcwd()+'/assets/fonts/normal.ttf', 16)

        self.allSprites = pg.sprite.Group()
        self.textSprites = pg.sprite.Group()
        self.playersSprites = pg.sprite.Group()
        self.enemiesSprites = pg.sprite.Group()

    def vaciaSprites(self):
        self.playersSprites.empty()
        self.allSprites.empty()
        self.textSprites.empty()
        self.enemiesSprites.empty()

    def individual_otro(self, ini=False):
        if ini:
            self.vaciaSprites()
            self.ball = Ball(random.randint(0,self.screen.get_rect().w), random.randint(0,self.screen.get_rect().h))
            self.playersSprites.add(self.ball)

            for i in range(random.randint(6,16)):
                wall = Wall(random.randint(0,self.screen.get_rect().w), random.randint(0,self.screen.get_rect().h), self.enemiesSprites)

            self.allSprites.add(self.playersSprites)
            self.allSprites.add(self.enemiesSprites)

        self.ball.comprobarChoque(self.enemiesSprites)

    def individual_mismo(self, ini):
        if ini:
            self.vaciaSprites()
            for i in range(5):
                ball = Ball(random.randint(0, self.screen.get_rect().w), random.randint(0, self.screen.get_rect().h))
                ball.color = ((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                self.playersSprites.add(ball)

            self.allSprites.add(self.playersSprites)

        for ball in self.playersSprites:
            ball.comprobarChoque(self.playersSprites)

    def coger(self, ini):
        if ini:
            print("ini")
            self.vaciaSprites()

            self.robot = Robot(random.randint(0,672), random.randint(0,472))

            for i in range(5):
                b = Ball(random.randint(0,672), random.randint(0,472))
                b.color = ((random.randint(0,255), random.randint(0,255), random.randint(0,255)))          
                self.enemiesSprites.add(b)      

            self.playersSprites.add(self.robot)
            self.allSprites.add(self.playersSprites)
            self.allSprites.add(self.enemiesSprites)


        cara_cruz = random.randint(0, 20)
        if cara_cruz == 1:
            new_dir = random.choice((0,1,2,3))
            self.robot.direction = new_dir

        self.robot.cogerAlTocar(self.enemiesSprites)

    def anima(self, ini):
        if ini:
            self.vaciaSprites()

            for i in range(5):
                xplosion = Explosion(random.randint(0,672), random.randint(0,472))
                self.playersSprites.add(xplosion)
            self.allSprites.add(self.playersSprites)


    def handleevent(self, status, option):
        for event in pg.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_0:
                return GAMEOVER, None, None

            if event.type == KEYDOWN:
                if not status:
                    for option in self.config:
                        if event.key == self.config[option]['key']:
                            return PARTIDA, option, True
                else:
                    if event.key == K_ESCAPE:
                        return None, None, None

        return status, option, False
                  
    def creaTexto(self, cadena, fuente, color):
        aText = pg.sprite.Sprite()
        aText.image = fuente.render(cadena, 1, color)
        aText.rect = aText.image.get_rect()

        return aText

    def menuInicial(self):
        self.textSprites.empty()
        self.allSprites.empty()
        logo = pg.sprite.Sprite()
        logo.image = pg.image.load(os.getcwd()+'/assets/images/logoKC.png').convert_alpha()
        logo.rect = logo.image.get_rect()
        logo.rect.y = 42
        logo.rect.x = centrar(logo.rect.w, self.w)
        self.allSprites.add(logo)

        aText = self.creaTexto("Elige una opción", self.mainTitle, NEGRO)
        aText.rect.y = 230
        aText.rect.x = centrar(aText.rect.w, self.w)
        self.textSprites.add(aText)

        aText = self.creaTexto("Pulsa la tecla que corresponda", self.Subtitle, NEGRO)
        aText.rect.y = 270
        aText.rect.x = centrar(aText.rect.w, self.w)
        self.textSprites.add(aText)

        for option in self.config:
            aText = self.creaTexto("{} - {}".format(option, self.config[option]['text']), self.normalText, NEGRO)
            aText.rect.x = centrar(aText.rect.w, self.w)
            aText.rect.y = 310 + int(option)*24
            self.textSprites.add(aText)

        self.allSprites.add(self.textSprites)

    def game_over(self):
        pg.quit()
        sys.exit()

    def render(self, dt=None):
        self.screen.fill((BACKGROUND))

        self.allSprites.update(dt)
        self.allSprites.draw(self.screen)

        self.display.flip()

    def mainloop(self):
        game_over = False
        new_game = False
        status = None
        addinfo = None

        while not game_over:
            dt = self.clock.tick(FPS)

            status, addinfo, ini = self.handleevent(status, addinfo)
            if status == GAMEOVER:
                game_over = True
            elif status == PARTIDA:
                if self.config.get(addinfo):
                    self.config[addinfo]['method'](ini)
            else:
                self.menuInicial()

            self.render(dt)

if __name__ == '__main__':
    pg.init()
    game = Game(800, 600)
    game.mainloop()



