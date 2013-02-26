import sys
import string
from PySFML import sf
from Mapa import Mapa
from Sonidos import Sonidos
from ServerTesting import SocketServer
from XMLMaker import XMLGenerator
from ServerFomLog import FormServidorLog
from Tableros import Tableros
from creditos import Creditos

class ServerForm:
    width = 0
    heigth = 0
    Evento = None
    window = None
    negro = None
    blanco = None
    BombermanB = None
    negro = None
    #para pintar
    Mapa =None
    Fondo = None
    #textbox
    msjNumPlayers = None
    msjNumTeams = None
    msjTiempo = None
    #focus text
    FocusText1 = False
    temText1 = None
    temLinea1 = None
    CONSTANTE_LEN_TEAMS = 3
    FocusText2 = False
    temText2 = None
    temLinea2 = None
    CONSTANTE_LEN_PLAYER = 3
    FocusText3 = False
    temText3 = None
    temLinea3 = None
    CONSTANTE_LEN_TIEMPO = 7
    DIRECTORIO = "bgs/"
    DIRECTORIO_MAPA = "tableros/"
    musica = None
    Tab = None
    current_mapa = ""
	
    def __init__(self):
        #self.musica = sf.Music()
        #self.musica.OpenFromFile("music/DBZ_8bit.ogg")
        #self.musica.SetLoop(True)
        #self.musica.Initialize(2, 44100)
        #self.musica.Play()
        self.temText1 = ''
        self.temLinea1 = ''
        self.temText2 = ''
        self.temLinea2 = ''
        self.temText3 = ''
        self.temLinea3 = ''
        self.width = 800
        self.heigth = 400
        self.blanco = sf.Color(250, 250, 250)
        self.negro =  sf.Color(0, 0, 0)
        self.window = sf.RenderWindow(sf.VideoMode(self.width, self.heigth), "BOMBERMAN SERVER")
        self.Evento = sf.Event()
        self.PintarFondo()
        self.PintarTextBox()
        self.Tab = Tableros()
        self.PintarMapas(self.Tab.GetFirst())
        self.window.SetFramerateLimit(60)
        self.sonidos = Sonidos()
        self.sonidos.PlayScreenServer1()


    def PintarFondo(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"main.jpg")
        self.Fondo = sf.Sprite(image)
        self.Fondo.Resize(800,400)
        self.Fondo.SetCenter(0, 0)
        self.Fondo.SetPosition(0,0)

    def PintarMapas(self,nombre):
        self.current_mapa = nombre
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO_MAPA+nombre+".png")
        if self.Mapa == None:
            self.Mapa = sf.Sprite(image)
        else:
            self.Mapa.SetImage(image)
        self.Mapa.Resize(294,167)
        self.Mapa.SetCenter(0, 0)
        self.Mapa.SetPosition(259,137)
        

        
    def PintarTextBox(self):
        #Texto del Textbox
        self.msjNumPlayers = sf.String('')
        self.msjNumPlayers.SetColor(self.blanco)
        self.msjNumPlayers.SetCenter(0,0)
        self.msjNumPlayers.SetPosition(750,35)
        self.msjNumPlayers.SetSize(15) 

        #Texto del Textbox 
        self.msjNumTeams = sf.String('')
        self.msjNumTeams.SetColor(self.blanco)
        self.msjNumTeams.SetCenter(0,0)
        self.msjNumTeams.SetPosition(100,34)
        self.msjNumTeams.SetSize(15) 

        #Texto del Textbox 
        self.msjTiempo = sf.String('')
        self.msjTiempo.SetColor(self.blanco)
        self.msjTiempo.SetCenter(0,0)
        self.msjTiempo.SetPosition(402,78)
        self.msjTiempo.SetSize(15) 

    def EscrirMensajeTeams(self,event):
        if event.Text.Unicode == 8:
            self.temLinea1 = self.temLinea1[:len(self.temLinea1)-1]
            self.temText1 = self.temText1[:len(self.temText1)-1]
            if len(self.temLinea1) >= self.CONSTANTE_LEN_TEAMS:
                self.temText1 = self.temLinea1[len(self.temLinea1)-self.CONSTANTE_LEN_TEAMS:len(self.temLinea1)-self.CONSTANTE_LEN_TEAMS+1] + self.temText1
        else:
            if len(self.temText1)>=self.CONSTANTE_LEN_TEAMS:
                self.temText1 = self.temText1[1:]
            self.temLinea1 += unichr(event.Text.Unicode)
            self.temText1 += unichr(event.Text.Unicode)
        self.msjNumTeams.SetText(self.temText1)

    def EscrirMensajePlayer(self,event):
        if event.Text.Unicode == 8:
            self.temLinea2 = self.temLinea2[:len(self.temLinea2)-1]
            self.temText2 = self.temText2[:len(self.temText2)-1]
            if len(self.temLinea2) >= self.CONSTANTE_LEN_PLAYER:
                self.temText2 = self.temLinea2[len(self.temLinea2)-self.CONSTANTE_LEN_PLAYER:len(self.temLinea2)-self.CONSTANTE_LEN_PLAYER+1] + self.temText2
        else:
            if len(self.temText2)>=self.CONSTANTE_LEN_PLAYER:
                self.temText2 = self.temText2[1:]
            self.temLinea2 += unichr(event.Text.Unicode)
            self.temText2 += unichr(event.Text.Unicode)
        self.msjNumPlayers.SetText(self.temText2)

    def EscrirMensajeTiempo(self,event):
        if event.Text.Unicode == 8:
            self.temLinea3 = self.temLinea3[:len(self.temLinea3)-1]
            self.temText3 = self.temText3[:len(self.temText3)-1]
            if len(self.temLinea3) >= self.CONSTANTE_LEN_TIEMPO:
                self.temText3 = self.temLinea3[len(self.temLinea3)-self.CONSTANTE_LEN_TIEMPO:len(self.temLinea3)-self.CONSTANTE_LEN_TIEMPO+1] + self.temText3
        else:
            if len(self.temText3)>=self.CONSTANTE_LEN_TIEMPO:
                self.temText3 = self.temText3[1:]
            self.temLinea3 += unichr(event.Text.Unicode)
            self.temText3 += unichr(event.Text.Unicode)
        self.msjTiempo.SetText(self.temText3)
        
    def BotonCancelar(self):
        self.window.Close()

    def BotonCrear(self):
        mapa  = Mapa(self.current_mapa)
        mapa.crearMapa()
        xml = XMLGenerator()
        xml.tiempo = int(self.temLinea3)
        xml.setMapa(mapa)
        xml.generarXMLGame()
        self.cambiarVentana()
        
        
    def cambiarVentana(self):
        tiempo = int(self.temLinea3)
        cantidad_jugadores = int(self.temLinea2)
        cantidad_equipos = int(self.temLinea1)
        F = FormServidorLog(cantidad_jugadores,cantidad_equipos,tiempo)
        F.sonidos = self.sonidos
        self.window.Close()
        F.Update()

    def BotonCreditos(self):
       c = Creditos()
       c.Update()
       self.Update()
    
    def DeterminarFocus(self,x,y):
        #NUM TEAMS
        if(x >= 100 and x <= 128):
            if(y >= 34 and y <= 47):
                self.FocusText1 = True
        if not (x >= 100 and x<= 128):
            self.FocusText1 = False
        #NUM JUGADORES
        if(x >= 748 and x <= 777):
            if(y >= 35 and y <= 48):
                self.FocusText2 = True
        if not(x >= 748 and x <= 777):
                self.FocusText2 = False
        #NUM TIEMPO
        if(x >= 399 and x <= 463):
            if(y >= 78 and y <= 93):
                self.FocusText3 = True;
        if not(x >= 399 and x <= 463):
                self.FocusText3 = False

        if(x >= 56 and x <= 187):
            if(y >= 266 and y <= 318):
                self.BotonCancelar()
        if(x >= 624 and x <= 754):
            if(y >= 265 and y <= 317):
                self.BotonCrear()
        if(x >= 328 and x <= 477):
            if(y >= 340 and y <= 374):
                self.BotonCreditos()
                
    def Pintar(self):
        self.window.Draw(self.Fondo)
        self.window.Draw(self.msjNumPlayers)
        self.window.Draw(self.msjNumTeams)
        self.window.Draw(self.msjTiempo)
        self.window.Draw(self.Mapa)

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
                        self.EscrirMensajeTeams(self.Evento)
                    if(self.FocusText2):
                        self.EscrirMensajePlayer(self.Evento)
                    if(self.FocusText3):
                        self.EscrirMensajeTiempo(self.Evento)
                        
                if self.Evento.Type == sf.Event.KeyPressed:
                    if self.Evento.Key.Code == sf.Key.Right:
                        self.PintarMapas(self.Tab.GetSiguiente())
                    if self.Evento.Key.Code == sf.Key.Left:
                        self.PintarMapas(self.Tab.GetAnterior())
                        
                        
            self.window.Clear(self.blanco)
            self.Pintar()
            self.window.Display()
        self.window.Close()

    
ven = ServerForm()
ven.Update() 
