from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from PySFML import sf
import random
from Mapa import Mapa
from Player import Player

class XMLGenerator:
    count = 0
    def __init__(self):
        #las probabilidades se le setearan a la clase PowerUps
        self.numPlayers = 8
        self.teamsCount = 0
        self.cantPowerUps = 0
        self.tiempo = 0 #en segundos
        self.players = []
        self.teams = []
        self.filas = 1
        self.columnas = 1

        self.tree = ElementTree()
        self.root = Element("root")

        self.tablero = Element("tablero")
        self.tagCuadros = Element("cuadros")
        self.tagPowerups = Element("powerups")
        self.tagPlayers = Element("players")

    #--------------------------------------
    def setTeams(self, teams):
        self.teams = teams
        self.teamsCount = len(self.teams)

    def setPlayers(self, plays):
        self.players = plays
        self.numPlayers = len(plays)

    def setCantidadPowerUps(self, cant):
        self.cantPowerUps = cant

    def setDimensiones(self, filas, cols):
        self.filas = filas
        self.columnas = cols

    def setMapa(self, mapa):
        self.mapa = mapa

    #---------------------------------------
    def configurarGame(self, cantPU, cantTeams, plays):
        self.setTeams(cantTeams)
        self.setPlayers(plays)
        self.setCantidadPowerUps(cantPU)

    def generarXMLGame(self):
        #config
        config = Element("config")
        config.set("tiempo", str(self.tiempo))
        config.set("BG", self.mapa.fondo)
        config.set("BGSound", self.mapa.musica)
        config.set("stage",self.mapa.nombre)
        
        #cuadros
        for i in self.mapa.bloques:
            bl = self.mapa.bloques[i]
            for blo in bl:
                bloque = bl[blo]
                if bloque is not None:
                    i = bloque.x
                    j = bloque.y
                    cuadro =  Element("cuadro")
                    cuadro.set("fila", str(j))
                    cuadro.set("columna", str(i))
                    cuadro.set("tipo", bloque.getTipo())
                    if bloque.tienePowerUp:
                        cuadro.set("powerup", bloque.getPUSprite())
                        cuadro.set("tipoPower", bloque.tipoPowerUp)
                    else:
                        cuadro.set("powerup", "__EMPTY__")
                        cuadro.set("tipoPower", "__EMPTY__")
                    cuadro.text = bloque.spriteBloque
                    self.tagCuadros.append(cuadro)

        self.tablero.append(self.tagCuadros)
        self.root.append(config)
        self.root.append(self.tablero)
        self.tree._setroot(self.root)
        self.tree.write("currentGame3.xml", "utf-8")


    def generarXMLPlayers(self):
        pperteam = self.numPlayers/self.teamsCount
        rootP = Element("root")
        for team in self.teams:
            tagTeam = Element("team")
            tagTeam.set("color", team)
            for player in self.players:
                if player.team == team:
                    tagPlayer = Element("player")
                    tagPlayer.set("nombre", player.nombre)
                    tagPlayer.set("iniX", str(player.iniX))
                    tagPlayer.set("iniY", str(player.iniY))
                    tagPlayer.set("vidas", str(player.vidas))
                    tagPlayer.text = player.getSpriteFullName()
                    tagTeam.append(tagPlayer)
            rootP.append(tagTeam)
        treeP = ElementTree()
        treeP._setroot(rootP)
        treeP.write("playersInfo.xml","utf-8")


if __name__ == "__main__":
    mapa = Mapa("STAGE1_4")
    mapa.crearMapa()
    maker = XMLGenerator()
    maker.setMapa(mapa)
    maker.setDimensiones(10,10)
    maker.generarXMLGame()
    player1 = Player('kike',2,1,0,"sprite1")
    player1.setTeam("purple")
    player2 = Player('varus',3,1,0,"sprite4")
    player2.setTeam("blue")
    player3 = Player('hector',2,1,0,"sprite3")
    player3.setTeam("blue")
    player4 = Player('elkin',2,1,0,"sprite1")
    player4.setTeam("purple")
    maker.setPlayers([player1, player2, player3, player4])
    maker.setTeams(['purple','blue'])
    maker.generarXMLPlayers()
