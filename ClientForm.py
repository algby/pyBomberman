import sys
import string
from PySFML import sf
from ClientTesting import SocketClient
from Waiting import Waiting
from Sonidos import Sonidos
from Statics import Statics

class ClientForm:
    Fondo = None
    FondoNuevo = None
    
    msjIp = None
    temText1 = ''
    temLinea1 = ''
    CONSTANTE_IP = 15
    
    msjPort = None
    temText2 = ''
    temLinea2 = ''
    CONSTANTE_PORT = 5

    msjNick = None
    temText3 = ''
    temLinea3 = ''
    CONSTANTE_NICK = 15

    FocusText1 = False
    FocusText2 = False
    FocusText3 = False
    
    conectado = False
    DIRECTORIO = "bgs/"

    #cuando se conecte
    client = None
    lista_players = None
    lista_temp = ''
    
    
    def __init__(self):
        self.window = sf.RenderWindow(sf.VideoMode(700,400), "BOMBERMAN SERVER")
        self.Evento = sf.Event()
        self.window.SetFramerateLimit(60)
        self.blanco = sf.Color(250, 250, 250)
        self.negro =  sf.Color(0, 0, 0)
        self.PintarFondo()
        self.PintarTextbox()
        self.sonidos = Sonidos()
        self.sonidos.PlayScreenClient1()
        #self.PintarListaClientes()

    def PintarFondo(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"main_cliente.jpg")
        self.Fondo = sf.Sprite(image)
        self.Fondo.Resize(700,400)
        self.Fondo.SetCenter(0, 0)
        self.Fondo.SetPosition(0,0)

    def PintarTextbox(self):
        #Texto del Textbox 
        self.msjNick = sf.String('')
        self.msjNick.SetColor(self.negro)
        self.msjNick.SetCenter(0,0)
        self.msjNick.SetPosition(100,250)
        self.msjNick.SetSize(20)
        
        #Texto del Textbox
        self.msjIp = sf.String('')
        self.msjIp.SetColor(self.negro)
        self.msjIp.SetCenter(0,0)
        self.msjIp.SetPosition(104,300)
        self.msjIp.SetSize(20) 

        #Texto del Textbox 
        self.msjPort = sf.String('')
        self.msjPort.SetColor(self.negro)
        self.msjPort.SetCenter(0,0)
        self.msjPort.SetPosition(104,350)
        self.msjPort.SetSize(20) 
 
    def EscrirMensajeNick(self,event):
        if event.Text.Unicode == 8:
            self.temLinea1 = self.temLinea1[:len(self.temLinea1)-1]
            self.temText1 = self.temText1[:len(self.temText1)-1]
            if len(self.temLinea1) >= self.CONSTANTE_NICK:
                self.temText1 = self.temLinea1[len(self.temLinea1)-self.CONSTANTE_NICK:len(self.temLinea1)-self.CONSTANTE_NICK+1] + self.temText1
        else:
            if len(self.temText1)>=self.CONSTANTE_NICK:
                self.temText1 = self.temText1[1:]
            self.temLinea1 += unichr(event.Text.Unicode)
            self.temText1 += unichr(event.Text.Unicode)
        self.msjNick.SetText(self.temText1)

    def EscrirMensajeIp(self,event):
        if event.Text.Unicode == 8:
            self.temLinea2 = self.temLinea2[:len(self.temLinea2)-1]
            self.temText2 = self.temText2[:len(self.temText2)-1]
            if len(self.temLinea2) >= self.CONSTANTE_IP:
                self.temText2 = self.temLinea2[len(self.temLinea2)-self.CONSTANTE_IP:len(self.temLinea2)-self.CONSTANTE_IP+1] + self.temText2
        else:
            if len(self.temText2)>=self.CONSTANTE_IP:
                self.temText2 = self.temText2[1:]
            self.temLinea2 += unichr(event.Text.Unicode)
            self.temText2 += unichr(event.Text.Unicode)
        self.msjIp.SetText(self.temText2)

    def EscrirMensajePort(self,event):
        if event.Text.Unicode == 8:
            self.temLinea3 = self.temLinea3[:len(self.temLinea3)-1]
            self.temText3 = self.temText3[:len(self.temText3)-1]
            if len(self.temLinea3) >= self.CONSTANTE_PORT:
                self.temText3 = self.temLinea3[len(self.temLinea3)-self.CONSTANTE_PORT:len(self.temLinea3)-self.CONSTANTE_PORT+1] + self.temText3
        else:
            if len(self.temText3)>=self.CONSTANTE_PORT:
                self.temText3 = self.temText3[1:]
            self.temLinea3 += unichr(event.Text.Unicode)
            self.temText3 += unichr(event.Text.Unicode)
        self.msjPort.SetText(self.temText3)
                                                     
    def DeterminarFocus(self,x,y):
        #NUM Nick
        if(x >= 98 and x <= 226):
            if(y >= 246 and y <= 285):
                self.FocusText1 = True
        if not (y >= 246 and y <= 285):
            self.FocusText1 = False
        #NUM Ip
        if(x >= 102 and x <= 269):
            if(y >= 299 and y <= 335):
                self.FocusText2 = True
        if not(y >= 299 and y <= 335):
            self.FocusText2 = False
        #NUM Port
        if(x >= 102 and x <= 269):
            if(y >= 349 and y <= 387):
                self.FocusText3 = True
        if not (y >= 349 and y <= 387):
            self.FocusText3 = False

        if(x >= 311 and x <= 397):
            if(y >= 296 and y <= 337):
                self.BotonConectar()

    def BotonConectar(self):
        self.client = SocketClient()
        
        
        tip = self.temLinea2
        tport = int(self.temLinea3)
        tnick = self.temLinea1
        
        waiting = Waiting()
        waiting.setClientSocket(self.client)
        
        self.client.setWait(waiting)
        self.client.__connect__(tip, int(tport),tnick )
        waiting.sonidos = self.sonidos
        Statics.SetClient(self.client)
        self.window.Close()
        waiting.Update()
        
    def Pintar(self):
        self.window.Draw(self.Fondo)          
        self.window.Draw(self.msjIp)
        self.window.Draw(self.msjPort)
        self.window.Draw(self.msjNick)

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

                if self.Evento.Type == sf.Event.MouseButtonPressed:
                    self.DeterminarFocus(x,y)
                    
                if self.Evento.Type == sf.Event.TextEntered:
                    if(self.FocusText1):
                        self.EscrirMensajeNick(self.Evento)
                    if(self.FocusText2):
                        self.EscrirMensajeIp(self.Evento)
                    if(self.FocusText3):
                        self.EscrirMensajePort(self.Evento)        
            self.window.Clear(self.blanco)
            self.Pintar()
            self.window.Display()            
        self.window.Close()

v = ClientForm()
v.Update()
