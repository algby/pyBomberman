import sys
import string
from PySFML import sf
from Mapa import Mapa
from Sonidos import Sonidos
from ServerTesting import SocketServer
from XMLMaker import XMLGenerator

class FormServidorLog:
    window = None
    lista_players = None
    lista_temp = ''
    fondo_lista = None
    
    Evento = None
    blanco = None
    negro = None

    IP = None
    PORT = None
    numeroTeams = None
    server = None
    DIRECTORIO = "bgs/"
    
    
    def __init__(self,cantidad_jugadores,cantidad_equipos,tiempo):
        self.blanco = sf.Color(250, 250, 250)
        self.negro =  sf.Color(0, 0, 0)
        self.window = sf.RenderWindow(sf.VideoMode(500, 300), "BOMBERMAN SERVER")
        self.Evento = sf.Event()
        self.window.SetFramerateLimit(60)
        self.server = SocketServer()
        self.server.configGame(cantidad_jugadores,tiempo,cantidad_equipos)
        self.server.start()
        IP = self.server.IP
        PORT = self.server.PORT
        self.PintarIP_PORT(IP,PORT)
        self.server.LOG = self
        self.PintarLista()
        self.PintarBoton()
        self.PintarListaClientes()
        
    def PintarIP_PORT(self,ip,port):
        #IP
        self.IP = sf.String("IP: "+ip)
        self.IP.SetColor(self.negro)
        self.IP.SetCenter(0,0)
        self.IP.SetPosition(30,5)
        self.IP.SetSize(20)
        #PORT
        self.PORT = sf.String("PORT: "+str(port))
        self.PORT.SetColor(self.negro)
        self.PORT.SetCenter(0,0)
        self.PORT.SetPosition(30,30)
        self.PORT.SetSize(20)
        
    def PintarLista(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"lista.png")
        self.fondo_lista = sf.Sprite(image)
        self.fondo_lista.Resize(500,300)
        self.fondo_lista.SetCenter(0, 0)
        self.fondo_lista.SetPosition(0,0)

    def PintarListaClientes(self):
        self.lista_players = sf.String('')
        self.lista_players.SetColor(self.negro)
        self.lista_players.SetCenter(0,0)
        self.lista_players.SetPosition(30,60)
        self.lista_players.SetSize(15)
    
    def PintarBoton(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"boton1.png")
        self.boton1 = sf.Sprite(image)
        self.boton1.Resize(164,300)
        self.boton1.SetCenter(0, 0)
        self.boton1.SetPosition(336,0)

        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"boton2.png")
        self.boton2 = sf.Sprite(image)
        self.boton2.Resize(164,300)
        self.boton2.SetCenter(0, 0)
        self.boton2.SetPosition(336,0)

    def Pintar(self,x):
        self.window.Draw(self.fondo_lista)
        self.window.Draw(self.boton1)
        self.window.Draw(self.IP)
        self.window.Draw(self.PORT)
        self.window.Draw(self.lista_players)
        if(self.isMouseOver(x)):
            self.window.Draw(self.boton2)
            
    def BotonAceptar(self):
        if self.server.puedeComenzar():
            XML = XMLGenerator()
            XML.setPlayers(self.server.game.players)
            XML.setTeams(self.server.game.COLORS[:self.numeroTeams])
            XML.generarXMLPlayers()
            self.server.sendPlayerList("playersInfo.xml")
            self.server.started = True
            self.window.Close()
            self.sonidos.StopScreenServer1()

    def isMouseOver(self,x):
        if x >= 336:
            return True

    def SetCliente(self,nick):
        self.lista_temp += nick + "\n"
        self.lista_players.SetText(self.lista_temp)

    def ClienteDesconectado(self,nick):
        inicio = string.find(self.lista_temp,"Cliente Conectado: "+nick)
        final = string.rfind("Cliente Conectado: "+nick+"\n","\n")
        #top = self.lista_temp[:inicio]
        #final = string.find(top,"\n")+1
        print str(inicio)+"--"+str(final)
        top = self.lista_temp[:inicio]
        bot = self.lista_temp[inicio+final+1:]
        self.lista_temp = top + bot
        self.lista_players.SetText(self.lista_temp)
            
    def Update(self):
        input = self.window.GetInput()
        quit = False 
        while not quit:
            x = input.GetMouseX()
            y = input.GetMouseY()     
            while self.window.GetEvent(self.Evento):
                if self.Evento.Type == sf.Event.Closed:
                    quit = True        
                if self.Evento.Type == sf.Event.MouseButtonPressed:
                    if(self.isMouseOver(x)):
                        self.BotonAceptar()

                if self.Evento.Type == sf.Event.JoyButtonPressed:
                    evento = self.Evento
                    if evento.JoyButton.Button + 1 == 10:
                        self.BotonAceptar()
                    
            self.window.Clear(self.blanco)
            self.Pintar(x)
            self.window.Display()
        self.window.Close()
#w = FormServidorLog(0,0,0)
#w.Update()
