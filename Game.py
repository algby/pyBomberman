from PySFML import sf
from Mapa import Mapa
import os
from Wall import Wall
from Player import Player
from Entidades import Entidades

class Game:
    mapa = None
    players = []
    MAX_PLAYERS = 0
    TEAMS = 0
    COLORS = ['red','green','blue','yellow']
    tiempo = 0
    cliente = None
    
    def GetTeamMates(self, player):
        temp = []
        team = ""
        for i in self.players:
            if i.nombre == player:
                team = i.team
        for i in self.players:
            if i.team == team and not (i.nombre == player):
                temp.append(i.nombre)
        return temp

    def isFull(self):
        return len(self.players)>=self.MAX_PLAYERS

    def __init__(self, maxPlayers, tiempo, cantTeams):
        self.MAX_PLAYERS = maxPlayers
        self.tiempo = tiempo
        self.TEAMS = cantTeams

        w = 52.3077
        w_total = 784.615385
        h = 52.3077
        h_total = 680
        wall = Wall(0,0,w,h_total)
        Entidades.agregarMuro(wall)

        wall = Wall(w_total-w,0,w,h_total)
        Entidades.agregarMuro(wall)

        wall = Wall(0,0,w_total,h)
        Entidades.agregarMuro(wall)

        wall = Wall(0,h_total-h,w_total,h)
        Entidades.agregarMuro(wall)

    def GetPlayer(self, nick):
        for player in self.players:
            if player.nombre == nick:
                return player
        return None

    def SetMapa(self,mapa):
        self.mapa = mapa

    def Draw(self, gameTime, window):
        if self.mapa is not None:
            self.mapa.Draw(gameTime, window)
        for player in self.players:
            player.Draw(gameTime, window)

    def Update(self, gameTime):
        if self.mapa is not None:
            self.mapa.Update(gameTime)
        for player in self.players:
            player.Update(gameTime)
            #-----------------------------------------------------
            colis = Entidades.colisionesPlayer_Players(player.sprite)
            for c in colis:
                player.handleCollision(c[1])

            colis = Entidades.colisionesPlayer_Bloques(player.sprite)
            for c in colis:
                player.handleCollision(c[1])

            colis = Entidades.colisionesPlayer_Bombas(player.sprite)
            startCol = False
            for c in colis:
                player.handleCollisionWithBomb(c[1])                
                
                
            colis = Entidades.colisionesPlayer_Muros(player.sprite)
            for c in colis:
                player.handleCollision(c[1])
            #-----------------------------------------------------
            colis = Entidades.colisionesFuego_Bloques()
            for col in colis:
                self.mapa.destruirBloque(col[1].i, col[1].j)

            colis = Entidades.colisionesPlayer_PowerUps(player.sprite)
            for col in colis:
                self.mapa.tomarPowerUp(col[1].i, col[1].j, player)

            if player.nombre == self.cliente.nick:
                colis = Entidades.colisionesPlayer_Fuego(player.sprite)
                if len(colis) > 0:
                    self.cliente.__send__("DEATH")
                    player.handleDeath()

            #colis = Entidades.colisionesFuego_PowerUps()
            #for col in colis:
            #    self.mapa.destruirPowerUp(col[1].i, col[1].j)

    def AgregarPlayer(self,player):
        if len(self.players)<self.MAX_PLAYERS:
            self.players.append(player)

    def MatarA(self, nick):
        for player in self.players:
            if player.nombre == nick:
                player.morir()

    def PosicionarPlayer(self,W,H):
        for player in self.players:
            player.setPosInicial(player.x,player.y,W,H)

    def MoverPlayer(self, nick, direccion, gameTime):
        for player in self.players:
            if player.nombre == nick:
                player.SetDirection(direccion)

    def PosicionarPlayer2(self, nick, x, y):
        for player in self.players:
            if player.nombre == nick:
                player.x = x
                player.y = y

    def SetDirection(self, nick, direction):
        for player in self.players:
            if player.nombre == nick:
                player.SetDirection(direction)

    def GenerarPlayerData(self,nick):
        x = len(self.players)
        miColor = self.COLORS[x%self.TEAMS]
        player = Player(nick, 3, x/2, x%2, "SP_"+str(x)+"_"+miColor)
        player.setTeam(miColor)

        return player

    def PonerBomba(self, nick, client, resend):
        for player in self.players:
            if player.nombre == nick:
                player.ponerBomba(client, resend)
                break

    def BorrarPlayer(self, nick):
        for i in range(len(self.players)):
            if self.players[i].nombre == nick:
                self.players.pop(i)
                return

    def PlayerPosition(self, nick):
        for i in range(len(self.players)):
            if self.players[i].nombre == nick:
                return self.players[i].sprite.GetPosition()
        return None
    
    def ToString(self):
        s = "ClassName: Game\n"
        s += "Tiempo: " + str(self.tiempo) + "\n"
        s += "Cantidad Jugadores: " + str(len(players)) + "\n"
        for p in players:
            s += "\t" + p.toString() + "\n"

        s += mapa.toString()

        return s
        
if __name__ == "__main__":
    game = Game(8)
    mapa = Mapa("STAGE1_4")
    game.setWindow(None)
    game.setMapa(mapa)
    
