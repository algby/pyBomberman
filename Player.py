from PySFML import sf
from MySprite import MySprite
from BombaNormal import BombaNormal
from Bomba import Bomba
from Entidades import Entidades
from Posiciones import Posiciones

class Player(object):
    nombre = ""
    team = "" #color
    spritePlayer = ""
    tipoBomba = ""
    sprite = None
    escalaX = 1
    escalaY = 1
    alcance = 1
    x = 0
    y = 0
    vidas = 10
    muertes = 0
    score = 0
    velocidad = 90
    iniX = x
    iniY = y
    direccion = "None"
    MAX_BOMBAS = 1
    DIRECTORIO = "players/"
    vidasNoImportan = True
    
    def __init__(self, nombre, vidas, posX, posY, spPlayer):

        self.nombre = nombre
        self.vidas = vidas
        self.setPosicion(posX, posY)
        self.iniX = posX
        self.iniY = posY
        self.spritePlayer = spPlayer
        self.velocidad = 120
        self.tipoBomba = "Normal"
        self.dejoColisionar = False
        self.bombas = []
        self.TimeDeath = 0

    def setNombre(self, nom):
        self.nombre = nom

    def setTeam(self, team):
        self.team = team

    def setScales(self, scaleX, scaleY):
        self.escalaX = scaleX
        self.escalay = scaleY

    def setPosicion(self, x, y):
        self.x = x
        self.y = y

    def setPosInicial(self, posX, posY, W, H):
        """self.iniX = self.x*((posX + W)-20)
        self.iniY = self.y*float(H)-50
        self.x = self.iniX
        self.y = self.iniY
        """
        Posiciones.init()
        x,y = Posiciones.getPosicion(posX, posY)
        self.x = x
        self.y = y
        self.iniX = x
        self.iniY = y

    def contarBombas(self):
        cont = 0
        for i in self.bombas:
            if i.sprite.visible:
                cont += 1
        return cont

    def incrementarScore(self, inc):
        if inc>0:
            self.score += inc

    def disminuirScore(self, dec):
        if dec>0:
            self.score -= dec

    def ponerBomba(self, client, resend):
        if self.contarBombas()<self.MAX_BOMBAS:
            bomba = None
            w,h = self.sprite.GetSize()
            x = self.x + w/2
            y = self.y + h/2
            if self.tipoBomba is "Calabaza":
                bomba = BombaNormal(x, y, True)
                bomba.setRango(self.alcance)
            if self.tipoBomba is "Normal":
                bomba = BombaNormal(x, y, False)
                bomba.setRango(self.alcance)
            if self.tipoBomba is "Detonable":
                bomba = BombaDetonable()
            if bomba != None:
                self.bombas.append(bomba)
                if resend:
                    client.__send__("BOMB:Normal,"+str(self.alcance)+","+str(self.x)+","+str(self.y))

    def tomoPowerUp(self, tipo):
        if tipo== "Bomb_Up":
            self.MAX_BOMBAS += 1
            self.incrementarScore(5)
        if tipo=="Fire":
            if self.alcance<Bomba.getMaxRango():
                self.alcance += 1
            self.incrementarScore(5)
        if tipo=="Skate":
            if self.velocidad<300:
                self.velocidad += 30
            self.incrementarScore(5)
        if tipo=="Sandal":
            self.disminuirScore(5)
            if self.velocidad>30:
                self.velocidad -= 30
        if tipo=="Full_Fire":
            self.alcance = Bomba.getMaxRango()
            self.incrementarScore(15)
        if tipo=="Pierce_Bomb":
            self.tipoBomba = "Calabaza"
            self.incrementarScore(15)
    
    def moverArriba(self,gameTime):
        self.y -= self.velocidad * gameTime

    def moverAbajo(self, gameTime):
        self.y += self.velocidad * gameTime

    def moverDerecha(self, gameTime):
        self.x += self.velocidad * gameTime

    def moverIzquierda(self, gameTime):
        self.x -= self.velocidad * gameTime

    def getSpriteFullName(self):
        return self.DIRECTORIO+self.spritePlayer+"_"+self.team+".png"

    def getSprite(self):
        sprite = MySprite(self.spritePlayer,self.iniX+52, self.iniY+52, 10)
        #sprite.listframes(12, 6, 44, 49)
        sprite.listframes(4,4,40,50)
        sprite.setframe(2)
        return sprite

    def Draw(self, gameTime, window):
        if self.vidas > 0 or self.vidasNoImportan:
            for bomb in self.bombas:
                bomb.Draw(gameTime, window)
            if self.sprite.visible:
                window.Draw(self.sprite)
        else:
            Entidades.eliminarPlayer(self.sprite)

    def Update(self, gameTime):
        self.TimeDeath += gameTime
        self.AutoMover(gameTime)
        self.collideDir = ""
        if self.sprite == None:
            self.sprite = self.getSprite()
            self.sprite.setRelated(self.nombre)
            self.sprite.SetScale(self.escalaX, self.escalaY)
            Entidades.agregarPlayer(self.sprite)
        self.sprite.SetPosition(self.x, self.y)
        for bomb in self.bombas:
            bomb.Update(gameTime)

    def AutoMover(self, gameTime):
        if self.direccion == "None":
            return
        self.sprite.mover(self.direccion, gameTime)
        if self.direccion == "Arriba":
            self.moverArriba(gameTime)
        if self.direccion == "Abajo":
            self.moverAbajo(gameTime)
        if self.direccion == "Derecha":
            self.moverDerecha(gameTime)
        if self.direccion == "Izquierda":
            self.moverIzquierda(gameTime)            

    def SetDirection(self, direction):
        if direction == "None":
            if self.direccion == "Derecha":
                self.sprite.setframe(14)
            if self.direccion == "Arriba":
                self.sprite.setframe(6)
            if self.direccion == "Izquierda":
                self.sprite.setframe(14)
                self.sprite.FlipX(True)
            if self.direccion == "Abajo":
                self.sprite.setframe(2)
        self.direccion  = direction

    def handleCollision(self, colSprite):
        delta = 3
        co_rect = colSprite.collision_area
        my_rect = self.sprite.collision_area
        
        w = my_rect.Right - my_rect.Left
        h = my_rect.Bottom - my_rect.Top
        left = my_rect.Left
        top = my_rect.Top

        if co_rect.Contains(left+w/2, top) and self.direccion == "Arriba":
            self.y += delta
        if co_rect.Contains(left+w/2, top+h) and self.direccion == "Abajo":
            self.y -= delta
        if co_rect.Contains(left, top+h/2) and self.direccion == "Izquierda":
            self.x += delta
        if co_rect.Contains(left+w, top+h/2) and self.direccion == "Derecha":
            self.x -= delta
            

    def handleCollisionWithBomb(self, colSprite):
        delta = 3
        co_rect = colSprite.collision_area
        my_rect = self.sprite.collision_area
        
        w = my_rect.Right - my_rect.Left
        h = my_rect.Bottom - my_rect.Top
        left = my_rect.Left
        top = my_rect.Top
        if not co_rect.Contains(left+w/2, top+h/2):
            if co_rect.Contains(left+w/2, top) and self.direccion == "Arriba":
                self.y += delta
            if co_rect.Contains(left+w/2, top+h) and self.direccion == "Abajo":
                self.y -= delta
            if co_rect.Contains(left, top+h/2) and self.direccion == "Izquierda":
                self.x += delta
            if co_rect.Contains(left+w, top+h/2) and self.direccion == "Derecha":
                self.x -= delta
        

    def handleDeath(self):
        #self.morir()
        self.setPosicion(self.iniX,self.iniY)
        
    def morir(self):
        if self.TimeDeath > 2.0:
            self.TimeDeath = 0
            self.setPosicion(self.iniX,self.iniY)
            self.sprite.SetPosition(self.iniX, self.iniY)
            self.sprite.post_update("Estatico")        
            self.vidas -= 1
            self.muertes += 1
            self.disminuirScore(20)
            

    def toString(self):
        s = "ClassName: Player\n"
        s += "Nombre: " + self.nombre + "\n"
        s += "Team: " + self.team + "\n"
        s += "Vidas: " + str(self.vidas) + "\n"
        s += "Sprite: " + self.spritePlayer + "\n"

        return s
        
