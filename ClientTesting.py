import socket
import string
import threading
from chat import chat

class SocketClient:
    nick = ""
    IP = ""
    PORT = 0
    client = None
    listening = None
    chat = None
    Wait = None
    Window = None

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __connect__(self, ip, port, nick):
        self.nick = nick
        self.IP = ip
        self.PORT = port
        tupla = ip, port

        self.client.connect(tupla)
        self.listening = threading.Thread(target = self.listeningFunc)
        self.listening.start()
        #client.send(len(nick))
        self.client.send(nick)

    def setChat(self, chat):
        self.chat = chat

    def setWait(self, wait):
        self.Wait = wait

    def setWindow(self, window):
        self.Window = window

    def __send__(self, msg):
        self.client.send(self.concatLength(msg))

    def sendMessage(self, msg):
        self.client.send(self.concatLength("MESSAGE:"+msg))

    def movePlayer(self,direction):
        self.client.send(self.concatLength("MOVEPLAYER:"+direction))

    def stopPlayer(self):
        self.client.send(self.concatLength("STOPPLAYER:"))

    def concatLength(self, data):
        dataLen = len(data)
        extraLen = len(str(dataLen)) + 2
        result = str(dataLen)+"$#"+data
        return result

    def stop(self):
        #stop el thread de listening?
        self.client.send(self.concatLength("CONNECTIONCLOSED"))
        self.client.close()
        
    def createFile(self,data,fileName):
        f= open(fileName,"w")
        f.write(data)
        f.close()

    def cutString(self, data, delimiter):
        pos = string.find(data, delimiter)
        return data[pos+len(delimiter):]

    def listeningFunc(self):
        data = ""
        while True:
            try:
                if data == "":
                    data = self.client.recv(1024)
                if data == "":
                    return
                pos = string.find(data, "$#")
                length = int(data[:pos])
                recibidos = len(data)
                while recibidos<length-2-len(str(length)):
                    data += self.client.recv(1024)
                    recibidos = len(data)
                data = data[pos+2:]
                
                tempData = ""
                
                if len(data)>length:
                    tempData = data[length:]
                    data = data[:length]

                if string.find(data, "$#")!=-1:
                    data = data[:string.find(data,"$#")-2]
                
                if data.startswith("MESSAGE:"):
                    data = self.cutString(data, "MESSAGE:")
                    self.chat.Append(data)
                if data.startswith("MESSAGEALL:"):
                    data = self.cutString(data, "MESSAGEALL:")
                    self.chat.Append("[All]"+data)
                if data.startswith("MESSAGETEAM:"):
                    data = self.cutString(data, "MESSAGETEAM:")
                    self.chat.Append("[Team]"+data)
                if data.startswith("MAPAFILE:"):
                    data = self.cutString(data, "MAPAFILE:")
                    self.createFile(data, "mapFile.xml")
                if data.startswith("PLAYERSFILE:"):
                    data = self.cutString(data, "PLAYERSFILE:")
                    self.createFile(data, "playersFile.xml")

                    self.Wait.Levantar()
                if data.startswith("ERROR:"):
                    self.stop()
                if data.startswith("NEWPLAYER:"):
                    data = self.cutString(data, "NEWPLAYER:")
                    nick = data[:string.find(data,",")]
                    team = self.cutString(data, ",")
                    self.Wait.CatchClient(nick,team)

                if data.startswith("MOVEPLAYER:"):
                    data = self.cutString(data, "MOVEPLAYER:")
                    nick = data[:string.find(data, ",")]
                    direction = self.cutString(data, ",")
                    self.Window.MoverPlayer(direction, nick)

                if data.startswith("STOPPLAYER:"):
                    data = self.cutString(data, "STOPPLAYER:")
                    nick = data[:string.find(data,",")]
                    data = self.cutString(data, ",")
                    x = int(float(data[:string.find(data,",")]))
                    data = self.cutString(data, ",")
                    y = int(float(data))
                    self.Window.DetenerPlayer("None", nick, x, y)

                if data.startswith("DISCONNECT:"):
                    data = self.cutString(data, "DISCONNECT:")
                    nick = data[:string.find(data, ",")]
                    team = self.cutString(data, ",")
                    self.Wait.DeleteClient(nick,team)

                if data.startswith("DISCONNECTINGAME:"):
                    data = self.cutString(data, "DISCONNECTINGAME:")
                    nick = data[:string.find(data, ",")]
                    team = self.cutString(data, ",")
                    self.Window.MoverPlayer("None", nick)

                if data.startswith("DEATH:"):
                    data = self.cutString(data, "DEATH:")
                    nick = data
                    self.Window.matarA(nick)

                if data.startswith("BOMB:"):
                    tipoB = data[:string.find(data, ",")]
                    data = self.cutString(data, ",")
                    rango = int(data[:string.find(data, ",")])
                    data = self.cutString(data, ",")
                    fila = float(data[:string.find(data, ",")])
                    data = self.cutString(data, ",")
                    columna = float(data[:string.find(data,",")])
                    nnick = self.cutString(data,",")
                    self.Window.PonerBomba(nnick)
                #mensajes de cambio de estado del personaje
                data = tempData
            except socket.error, msg:
                print msg
                break
        #self.stop()


if __name__ == "__main__":
    client = SocketClient()
    #ip = raw_input("IP: ")
    ip = "169.254.229.236"
    ip = "127.0.0.1"
    ip = "10.42.86.165"
    port = raw_input("PORT: ")
    client.__connect__(ip, int(port), "kike")
    #client.receive()    
    #client.__send__("BOMB:NORMAL,2,5,6")
    while True:
        x = raw_input("PRESS TO FINISH")
        if x == "QUIT":
            break
        else:
            client.__send__(x)
    client.stop()
