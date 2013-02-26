from MySprite import MySprite
import threading
from Entidades import Entidades
from Explosion import Explosion
from Sonidos import Sonidos


class Bomba(object):
    MAX_RANGO = 15
    @staticmethod
    def getMaxRango():
        return Bomba.MAX_RANGO
    
    def __init__(self, nombre, x, y, atrav):
        self.rango = 3
        self.sprite = None
        self.spriteName = nombre
        self.escalaX = 1
        self.escalaY = 1
        self.atraviesa = atrav
        
        self.x = int(x/52.3076923077)*52.3076923077
        self.y = int(y/52.3076923077)*52.3076923077
        
        self.sonidos = Sonidos()
        self.exp = None
        self.explosionEnded = False
        self.atraviesa = atrav
        time = threading.Timer(2.5, self.explode)
        time.start()

    def setScales(self, scaleX, scaleY):
        self.escalaX = scaleX
        self.escalaY = scaleY

    def setPosicion(self, x, y):
        self.x = x
        self.x = int(x/52.3076923077)*52.3076923077
        self.y = y
        self.y = int(y/52.3076923077)*52.3076923077

    def setRango(self, rango):
        self.rango = rango

    def explode(self):
        self.sonidos.PlayExplosion()
        self.sprite.visible = False
        Entidades.eliminarBomba(self.sprite)
        self.exp = Explosion(self.rango,self.x, self.y, self.atraviesa)
        t = threading.Timer(1, self.destroyExplode)
        t.start()

    def destroyExplode(self):
        self.explosionEnded = True
        self.exp.endExplosion()

    def getSprite(self):
        sprite = MySprite(self.spriteName, self.x, self.y, 10)
        sprite.t = 20.0
        sprite.listframes(1,7,50,50)
        sprite.setframe(1)
        return sprite

    def Update(self, gameTime):
        if self.sprite == None:
            self.sprite = self.getSprite()
            Entidades.agregarBomba(self.sprite)
        if self.sprite.visible:
            self.sprite.animar(False, [1, 2, 3, 4, 5, 6, 7], gameTime)
            self.sprite.post_update("Estatico")
        else:
            if self.exp != None:
                if not self.explosionEnded:
                    self.exp.Update(gameTime)

    def Draw(self, gameTime, window):
        if self.sprite == None:
            self.sprite = self.getSprite()
            Entidades.agregarBomba(self.sprite)
        if self.sprite.visible:
            window.Draw(self.sprite)
        else:
            if self.exp != None:
                if not self.explosionEnded:
                    self.exp.Draw(gameTime, window)

    def toString(self):
        s = "ClassName: Bomba\n"
        s += "Sprite: " + self.spriteName + "\n"
