from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element
from GameOverLogic import GameOverLogic
from Player import Player
from Bloque import Bloque
from Game import Game
from Mapa import Mapa
from PlayerSemiAutomatico import PlayerSemiAutomatico


class XMLParser:
    mapaFile = ""
    playersFile = ""
    game = None

    def __init__(self):
        pass

    def setMapaFile(self, fileName):
        self.mapaFile = fileName

    def setPlayersFile(self, fileName):
        self.playersFile = fileName

    #pre-requisito: setMapaFile usado
    def reconstruirGame(self,nick):
        #agregar players al game
        treeP = ET()
        treeP.parse(self.playersFile + ".xml")
        root = treeP.getroot()
        self.game = Game(len(root.findall("team/player")),0,len(root.findall('team')))
        for team in root.iter("team"):
            color = team.attrib["color"]
            for tagPlayer in team.iter("player"):
                nombre = tagPlayer.attrib["nombre"]
                x = int(tagPlayer.attrib["iniX"])
                y = int(tagPlayer.attrib["iniY"])
                vidas = int(tagPlayer.attrib["vidas"])
                if nombre == nick:
                    player = Player(nombre, vidas, x, y, tagPlayer.text)
                else:
                    player = PlayerSemiAutomatico(nombre, vidas, x, y, tagPlayer.text)
                player.setTeam(color)
                self.game.AgregarPlayer(player)
        #-------------------------------------------------------------
        treeM = ET()
        treeM.parse(self.mapaFile+".xml") #revisar donde se generara el XML
        root = treeM.getroot()
        config = root.find("config")

        mapa = Mapa("currentGame")
        self.game.tiempo = int(config.attrib["tiempo"])
        mapa.setFondo(config.attrib["BG"])
        mapa.setMusica(config.attrib["BGSound"])
        mapa.stage = config.attrib["stage"]
        print "STAGE!!!!: " + mapa.stage 
        tablero = root.find("tablero")
        cuadros = tablero.find("cuadros")
        for cuadro in cuadros.iter("cuadro"):
            fila = int(cuadro.attrib["fila"])
            col = int(cuadro.attrib["columna"])
            dest = cuadro.attrib["tipo"]
            
            bloque = Bloque(fila, col, dest=="D")
            bloque.setSpriteB(cuadro.text)
            bloque.setPowerUp(cuadro.attrib["tipoPower"], cuadro.attrib["powerup"])
            bloque.tienePowerUp = not(cuadro.attrib["powerup"] == "__EMPTY__")
            if mapa.stage == "STAGE3_4":
                bloque.autoDisappear = False
                bloque.destruir()
            if not mapa.bloques.has_key(fila):
                mapa.bloques[fila] = dict()
            mapa.bloques[fila][col] = bloque

        self.game.mapa = mapa
        GameOverLogic.game = self.game

        return self.game


if __name__ == "__main__":
    xml = XMLParser()
    xml.setMapaFile("currentGame3")
    xml.setPlayersFile("playersInfo")
    gam = xml.reconstruirGame()
    print gam.mapa.toString()
