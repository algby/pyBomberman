from PySFML import sf
from Bloque import Bloque
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element
import os
from PowerUps import PowerUps
from Wall import Wall
from Entidades import Entidades
from Posiciones import Posiciones

class Mapa:
    DIRECTORIO = "bgs/"
    tableros = "tableros/"
    fondo = ""
    musica = ""
    nombre = ""
    escalaX = 1
    escalaY = 1
    x = 0
    y = 0
    bloques = None
    song = None
    window = None
    sprite = None
    PUps = None
    count = 0

    def __init__(self, nombre):
        self.bloques = dict()
        self.nombre = nombre
        self.stage = "STAGE1_4"
        self.PUps = PowerUps()


    def cargarBase(self):
        tree = ET()
        tree.parse(self.tableros+self.nombre+'.xml')
        root = tree.getroot()

        self.count = int(root.find('cantPowerUps').text)
        self.fondo = root.find('fondo').text
        self.musica = root.find('musica').text
        self.stage = root.find('title').text
        
        for child in root.iter('bloque'):
            
            x = int(child.attrib["fila"])
            if not self.bloques.has_key(x):
                self.bloques[x] = dict()
            y = int(child.attrib["col"])
            tipo = child.attrib["tipo"]
            bloque = Bloque(x, y, tipo=="D")
            bloque.destruir()
            bloque.setSpriteB(child.text)
            self.bloques[x][y] = bloque
            

    def crearMapa(self):
        self.cargarBase()
        self.PUps.totalPowerUps = self.count
        Posiciones.init()
        
        if self.nombre in ["STAGE1_4","STAGE2_4","STAGE3_4","STAGE4_4","STAGE5_4"]:
            Posiciones.setTablero(self.nombre)
            for i in self.bloques.keys():
                a = self.bloques[i]
                for j in a.keys():
                    bloque = a[j]
                    if bloque.destructible:
                        tupla = self.PUps.generarSiguiente()
                        if tupla[0]!='ninguno':
                            bloque.setPowerUp(tupla[0], tupla[1])
                            bloque.tienePowerUp = True

    def setFondo(self, f):
        self.fondo = f

    def setMusica(self, song):
        self.musica = song

    def reproducirMusica(self):
        self.song = sf.Music()
        self.song.OpenFromFile(self.musica+".ogg")
        self.song.SetLoop(True)
        self.song.Initialize(2, 44100)
        self.song.Play()

    def detenerMusica(self):
        self.song.Stop()

    def pausarMusica(self):
        self.song.Pause()

    def getSpriteBG(self):
        imagen = sf.Image()
        imagen.LoadFromFile(self.DIRECTORIO + self.fondo+".png")
        sprite = sf.Sprite(imagen)
        sprite.SetCenter(0,0)
        sprite.SetScale(self.escalaX, self.escalaY)
        return sprite

    def setWindow(self, wind):
        self.window = wind
        for i in range(len(self.bloques)):
            for j in range(len(self.bloques[i])):
                self.bloques[i][j].setWindow(wind)

    def getBloque(self, i, j):
        if self.bloques.has_key(i):
            t = self.bloques[i]
            if t.has_key(j):
                return self.bloques[i][j]
            else:
                return None
        else:
            return None

    def destruirBloque(self, i, j):
        if self.bloques.has_key(i):
            t = self.bloques[i]
            if t.has_key(j):
                if self.bloques[i][j].destructible:
                    self.bloques[i][j].destruir()

    def tomarPowerUp(self, i, j, player):
        if self.bloques.has_key(i):
            t = self.bloques[i]
            if t.has_key(j):
                if self.bloques[i][j].tienePowerUp:
                    self.bloques[i][j].tomarPowerUp(player)

    def destruirPowerUp(self, i, j):
        if self.bloques.has_key(i):
            t = self.bloques[i]
            if t.has_key(j):
                if self.bloques[i][j].tienePowerUp:
                    self.bloques[i][j].destruirPowerUp()

    def Draw(self, gameTime, window):
        window.Draw(self.sprite)
        for b in self.bloques:
            bl = self.bloques[b]
            for blo in bl:
                bloq = bl[blo]
                bloq.Draw(gameTime, window)
        
    def Update(self, gameTime):
        if self.sprite == None:
            self.sprite = self.getSpriteBG()
        self.sprite.SetPosition(self.x, self.y)
        for b in self.bloques:
            bl = self.bloques[b]
            for blo in bl:
                bloq = bl[blo]
                bloq.Update(gameTime)
        
    def toString(self):
        s = "ClassName: Mapa\n"
        s += "Nombre Mapa: " + self.nombre + "\n"
        s += "Fondo: " + self.fondo + "\n"
        s += "Musica: " + self.musica + "\n"
        for b in self.bloques:
            bl = self.bloques[b]
            for blo in bl:
                bloq = bl[blo]
                s += "\t" + bloq.toString() + "\n"

        return s



if __name__ == "__main__":
    mapa = Mapa("STAGE1_4")
    mapa.crearMapa()
    mapa.setMusica("C:\Users\Alejandro\Desktop\ejemplo.ogg")
    mapa.reproducirMusica()
    raw_input()
    print mapa.toString()
    mapa.detenerMusica()
    
