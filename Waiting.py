import sys
import string
import threading
from PySFML import sf
from ventana import ventana
from Sonidos import Sonidos

class Waiting:
    BombermanB = None
    lista_players = None
    lista_temp = ''
    window = None
    socket = None
    sonidos = None
    DIRECTORIO = "bgs/"
    def __init__(self):
        self.blanco = sf.Color(250, 250, 250)
        self.negro =  sf.Color(0, 0, 0)
        self.window = sf.RenderWindow(sf.VideoMode(300, 200), "BOMBERMAN CLIENT")
        self.Evento = sf.Event()
        self.PintarFondo()
        self.PintarListaClientes()
        
        
    def setClientSocket(self, cliente):
        self.socket = cliente
        
    def disconnect(self):
        self.socket.stop()
        
    def PintarFondo(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"lista2.png")
        self.BombermanB = sf.Sprite(image)
        self.BombermanB.Resize(300,200)
        self.BombermanB.SetCenter(0, 0)
        self.BombermanB.SetPosition(0,0)
        
    def PintarListaClientes(self):
        self.lista_players = sf.String('')
        self.lista_players.SetColor(self.negro)
        self.lista_players.SetCenter(0,0)
        self.lista_players.SetPosition(31,15)
        self.lista_players.SetSize(15)
        
    def DeleteClient(self,nick,team):
        inicio = string.find(self.lista_temp, nick)
        final = string.rfind(nick +"--> "+ string.upper(team) + "\n","\n")
        top = self.lista_temp[:inicio]
        bot = self.lista_temp[inicio+final+1:]
        self.lista_temp = top + bot
        self.lista_players.SetText(self.lista_temp)

    def CatchClient(self,nick,team):
        self.lista_temp += nick +"--> "+ string.upper(team) + "\n"
        self.lista_players.SetText(self.lista_temp)

    def Levantar(self):
        self.sonidos.StopScreenClient1()
        self.window.Close()
        t = threading.Thread(target = self.Jugar)
        t.start()
        

    def Jugar(self):
        v = ventana(self.socket)
        v.Run()

    def Pintar(self):
        self.window.Draw(self.BombermanB)
        self.window.Draw(self.lista_players)
        
    def Update(self):
        input = self.window.GetInput()
        quit = False 
        while not quit:
            x = input.GetMouseX()
            y = input.GetMouseY()     
            while self.window.GetEvent(self.Evento):
                if self.Evento.Type == sf.Event.Closed:
                        quit = True
                        #self.musica.Stop()

            self.window.Clear(self.blanco)
            self.Pintar()
            self.window.Display()            
        self.window.Close()

