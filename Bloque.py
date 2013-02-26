from PySFML import sf
from Player import Player
from Sonidos import Sonidos
from MySprite import MySprite
from Entidades import Entidades
from Statics import Statics
import threading


class Bloque:
    directorio = "bloques/"
    spriteBloque = "hola"
    spritePowerUp = ""
    x = 0
    y = 0
    destructible = True
    tienePowerUp = False
    bloqueDestruido = False
    enUso = True        
    escalaX = 1.0462
    escalaY = 1.0462
    spriteB = None
    spriteP = None
    tipoPowerUp = ""
    autoDisappear = True
    
    
    def __init__(self, fila, colu, dest):
        self.spriteBloque = "nada"
        self.x = fila
        self.y = colu
        self.destructible = dest
        self.sonidos = Sonidos()

    def destruir(self):
        self.bloqueDestruido = True
        Entidades.eliminarBloque(self.spriteB)
        if self.autoDisappear:
            t = threading.Timer(12, self.destruirPowerUp)
            t.start()

    def destruirPowerUp(self):
        if self.spriteP != None:
            self.enUso = False
            self.spriteP.visible = False
            Entidades.eliminarPowerUp(self.spriteP)

    #regresa el sprite con la escala adecuada pero
    #sin setear la posicion x,y en el tablero!
    def getSprite(self):
        if not self.bloqueDestruido:
            sprite = MySprite(self.directorio + self.spriteBloque + ".png",self.x, self.y, 0)
        else:
            if self.tienePowerUp:
                sprite = MySprite(self.spritePowerUp,self.x, self.y, 0)
        if (not self.bloqueDestruido) or (self.tienePowerUp):
            sprite.listframes(1,1,50,50)
            sprite.setframe(1)
            #sprite = sf.Sprite(imagen)
            sprite.SetCenter(0,0)
            sprite.SetScale(self.escalaX,self.escalaY)
            return sprite
    
    def tomarPowerUp(self, player):
        self.sonidos.PlayPowerUp()
        self.enUso = False
        self.spriteP.visible = False
        Entidades.eliminarPowerUp(self.spriteP)
        player.tomoPowerUp(self.tipoPowerUp)
        #Statics.GetClient().__send__("PUTAKEN:"+str(self.spriteB.i)+","+ str(self.spriteB.j)+","+player.nombre)

    def setSpriteB(self, spBloque):
        self.spriteBloque = spBloque

    def setSprites(self, spBloque, spPowerUp):
        self.spriteBloque = spBloque
        self.spritePowerUp = spPowerUp

    def setPowerUp(self, tipo, sprite):
        self.tipoPowerUp = tipo
        self.spritePowerUp = sprite

    def destroyed(self):
        return bloqueDestruido

    def getTipo(self):
        if self.destructible:
            return "D"
        else:
            return "I"

    def getPUSprite(self):
        return self.spritePowerUp

    def setScales(self, scaleX, scaleY):
        self.escalaX = scaleX
        self.escalaY = scaleY

    def Draw(self, gameTime, window):
        if self.enUso:
            if not self.bloqueDestruido:
                window.Draw(self.spriteB)
            else:
                if self.tienePowerUp:
                    if self.spriteP == None:
                        self.Update(gameTime)
                    if self.spriteP.visible:
                        window.Draw(self.spriteP)

    def Update(self, gameTime):
        if self.enUso:
            if not self.bloqueDestruido: 
                if self.spriteB == None:
                    self.spriteB = self.getSprite()
                    self.spriteB.SetPosition(self.x*self.spriteB.GetSize()[0] + 52.3077, self.y*self.spriteB.GetSize()[1] + 50)
                    self.spriteB._create_collision_area()
                    self.spriteB.i = self.x
                    self.spriteB.j = self.y
                    self.spriteB.destruible = self.destructible
                    Entidades.agregarBloque(self.spriteB)
                self.spriteB.SetPosition(self.x*self.spriteB.GetSize()[0] + 52.3077, self.y*self.spriteB.GetSize()[1] + 50)
                self.spriteB.post_update("Estatico")
            else:
                if self.spriteP == None:
                    self.spriteP = self.getSprite()
                    if self.spriteP == None:
                        return
                    self.spriteP.i = self.x
                    self.spriteP.j = self.y
                    self.spriteP.SetPosition(self.x*self.spriteP.GetSize()[0] + 52.3077, self.y*self.spriteP.GetSize()[1] + 50)
                    Entidades.agregarPowerUp(self.spriteP)
                self.spriteP.SetPosition(self.x*self.spriteP.GetSize()[0] + 52.3077, self.y*self.spriteP.GetSize()[1] + 50)
                self.spriteP.post_update("Estatico")
            
            

    def toString(self):
        s = "ClassName: Bloque\n"
        s += "Sprite: " + str(self.spriteBloque) + "\n"
        s += "Destructible: " + str(self.destructible) + "\n"
        s += "Tiene powerup: " + str(self.tienePowerUp) + "\n"
        s += "Sprite PowerUp: " + self.spritePowerUp + "\n"
        s += "Pos x: "+ str(self.x)
        s += "Pos y: "+ str(self.y)

        return s
