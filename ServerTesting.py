# -*- coding: cp1252 -*-
import socket
import threading
import string
from Game import Game
from XMLParser import XMLParser

class SocketServer:
    clientes = dict()
    playersTeam = dict()
    server = None
    started = False
    IP = ""
    PORT = 0
    MAX_CLIENTS = 8
    END_THREAD = 0
    DATA_RECV = 1024
    game = None
    LOG = None
    
    def __init__(self):
        t = self.get_local_address(), 0
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
        self.server.bind(t)
        self.server.listen(self.MAX_CLIENTS)
        
        self.IP = t[0]
        self.PORT = self.server.getsockname()[1]

    def configGame(self, maxPlayers, tiempo, cantTeams):
        self.game = Game(maxPlayers, tiempo, cantTeams)

    def start(self):
        listening = threading.Thread(target = self.listeningFunc)
        listening.start()

    def get_local_address(self):
        return socket.gethostbyname(socket.gethostname())

    def sendPlayerList(self, playersFileName):
        f = open(playersFileName, 'r')
        self.__sendToAll__("PLAYERSFILE:"+f.read())

    def sendMap(self, gameFileName, nick):
        f = open(gameFileName, 'r')
        self.__sendDataTo__("MAPAFILE:"+f.read(),nick)

    def puedeComenzar(self):
        return not self.started
    
    def concatLength(self, data):
        dataLen = len(data)
        extraLen = len(str(dataLen)) + 2
        result = str(dataLen)+"$#"+data
        return result    

    def __sendDataTo__(self, data, nick):
        client = self.clientes[nick]
        dataSize = len(data)
        fulldata = self.concatLength(data)
        dataSent = client.send(fulldata)
        dataSize += len(str(dataSize)) + 2
        
        if dataSize != dataSent:
            self.__handleResend__(nick, fulldata[dataSent:], dataSize - dataSent)
        

    def __handleResend__(self, nick, data, size):
        sent = 0
        while sent<size:
            client = self.clientes[dest]
            sent += client.send(str(data)[sent:])

    def stop(self):
        self.END_THREAD = 1
        self.server.close()

    def listeningFunc(self):
        while True:
            if len(self.clientes)<self.MAX_CLIENTS:
                connection , address = self.server.accept()            
                if self.END_THREAD:
                    connection.close()
                    return
                else:
                    
                    nick = connection.recv(self.DATA_RECV)
                    nick = string.lower(nick)
                    
                    if self.clientes.keys().count(nick)==0:
                        self.clientes[nick] = connection
                        if self.newConnection(nick):
                            print "Cliente conectado " , address, " ", nick
                            newThread = threading.Thread(target = self.__listenClient__, args = (nick,))
                            newThread.start()
                            self.LOG.SetCliente("Cliente Conectado: "+nick)
                        else:
                            print "Cliente eliminado " + nick
                            del self.clientes[nick]
                        
                    else:
                        print "Cliente rechazado " + nick
                        connection.send(self.concatLength("ERROR: Este ID no esta disponible"))
                        #connection.close()

    def newConnection(self,nick):
        if not self.game.isFull():
            player = self.game.GenerarPlayerData(nick)
            self.game.AgregarPlayer(player)
            self.__sendToAllBut__("NEWPLAYER:"+nick+","+player.team,nick)
            self.playersTeam[nick] = player.team
            for i in self.playersTeam.keys():
                self.__sendDataTo__("NEWPLAYER:"+i+","+self.playersTeam[i],nick)

            self.sendMap("currentGame3.xml",nick)
            return True
        return False
        
        
    def cleanConnection(self, nick):
        del self.clientes[nick]
        del self.playersTeam[nick]
        self.game.BorrarPlayer(nick)
    
    def __listenClient__(self, nick):
        while True:
            try:
                data = self.clientes[nick].recv(self.DATA_RECV)
                length = self.getLength(data)
                data = self.cutString(data, "$#")
                dataReceived = self.DATA_RECV
                
                while dataReceived<length:
                    if length-dataReceived < self.DATA_RECV:
                        data += self.clientes[nick].recv(length-dataRecevied)
                        dataReceived = length
                    else:
                        data += self.clientes[nick].recv(self.DATA_RECV)
                        dataReceived += self.DATA_RECV
                
                if data == "CONNECTIONCLOSED":
                    print "Cliente desconectado " + nick
                    if not self.started:
                        self.LOG.ClienteDesconectado(nick)
                        self.__sendToAllBut__("DISCONNECT:"+nick+","+self.playersTeam[nick],nick)
                    else:
                        self.__sendToAllBut__("DISCONNECTINGAME:"+nick+","+self.playersTeam[nick],nick)
                    self.cleanConnection(nick)
                    break
                
                if data.startswith("BOMB:"):
                    self.__sendToAllBut__(data + "," + nick,nick) #no deberia ir aqui ahorita
                    data = self.cutString(data, "BOMB:")
                    
                    """tipoB = data[:string.find(data, ",")]
                    data = self.cutString(data, ",")
                    rango = int(data[:string.find(data, ",")])
                    data = self.cutString(data, ",")
                    fila = float(data[:string.find(data, ",")])
                    data = self.cutString(data, ",")
                    columna = float(data) """                   
                    #validar que se pueda poner bomba en el mapa
                    #tipo de bomba y otras cosas...
                    #enviar el mensaje al resto para que actualicen.

                if data.startswith("EXPLODE:"):
                    data = self.cutString(data, "EXPLODE:")
                    fila = int(data[:string.find(data, ",")])
                    print fila
                    data = self.cutString(data, ",")
                    columna = int(data)

                if data == "DEATH":
                    self.__sendToAll__("DEATH:"+nick)

                if data.startswith("MESSAGE:"):
                    data = self.cutString(data, "MESSAGE:")
                    if data.startswith("/all"):
                        data = self.cutString(data, "/all ")
                        self.__sendToAllBut__("MESSAGEALL:"+nick+":"+data,nick)
                    else:
                        if data.startswith("/team"):
                            data = self.cutString(data, "/team ")
                            self.__sendToTeam__("MESSAGETEAM:"+nick+":"+data,nick)
                        else:
                            if data.startswith("/"):
                                data = self.cutString(data, "/")
                                pos = string.find(data, " ")
                                if pos != -1:
                                    nickTo = data[:pos]
                                    data = self.cutString(data, nickTo)
                                    nickTo = string.lower(nickTo)
                                    if self.clientes.has_key(nickTo):
                                        self.__sendDataTo__("MESSAGE:"+nick+":"+data, nickTo)
                    
                if data.startswith("MOVEPLAYER:"):
                    direction  = self.cutString(data, "MOVEPLAYER:")
                    self.__sendToAllBut__("MOVEPLAYER:"+nick+","+direction,nick)

                if data.startswith("STOPPLAYER:"):
                    self.__sendToAllBut__(data,nick)

                if data.startswith("PUTAKEN:"):
                    pass

            except socket.error, msg:
                del self.clientes[nick]
                break
            
    def playersCount(self):
        return len(self.clientes)

            
    def cutString(self, data, delimiter):
        pos = string.find(data, delimiter)
        return data[pos+len(delimiter):]
    
    def getLength(self, data):
        pos = string.find(data, "$#")
        x = int(data[:pos])
        return x
        

    def __sendToAll__(self, data):
        for i in self.clientes:
            self.__sendDataTo__(data, i)

    def __sendToAllBut__(self, data, nick):
        for i in self.clientes:
            if i != nick:
                self.__sendDataTo__(data, i)

    def __sendToTeam__(self, data, nick):
        teamMates = self.game.GetTeamMates(nick)
        for i in teamMates:
            self.__sendDataTo__(data, i)

    def __log__(self, msg):
        pass


if __name__ == "__main__":
    xmlP = XMLParser()
    xmlP.setMapaFile("mapFile")
    xmlP.setPlayersFile("playersInfo")
    game = xmlP.reconstruirGame()
    server = SocketServer()
    server.game = game
    server.start()
    print server.game.GetTeamMates("varus")
    while 1:
        x = raw_input("TYPE STOPSERVER TO STOP SERVER...\n")
        if x=="STOPSERVER":
            break
        elif x=="SENDMAPA":
            server.sendMap('currentGame3.xml')
        elif x == "SENDPLAYERS":
            server.sendPlayerList()
        elif x.startswith("/all"):
            server.__sendToAll__(x)
        elif x=="MAPA":
            server.sendMap("currentGame3.xml","kike")
        elif x=="PLAYER":
            server.sendPlayerList("playersInfo.xml")
        elif x is not "":
            server.__sendToAll__(x)
    #server.stop()
