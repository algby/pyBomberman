from PySFML import sf
from chat import chat
from Cronometro import Cronometro
from XMLParser import XMLParser
from Entidades import Entidades
from Statics import Statics

class ventana:
    window = None
    Chat = None
    Cronometro = None
    Focus = False
    Evento = None
    Cliente = None
    Game = None
    heigth = 0
    width = 0
    posX_chat = 0
    posY_chat = 0
    heigth_C = 0.0
    width_C = 0.0
    heigth_V = 0.0
    width_V = 0.0
    # colores
    blanco = sf.Color(250, 250, 250)
    negro = sf.Color(0, 0, 0)

    def __init__(self,cliente):
        self.heigth = 680
        self.width = 1024
        self.heigth_C = 680.0
        self.width_C = 1024.0
        self.heigth_V = float(self.heigth)
        self.width_V = float(self.width)
        XMLP  = XMLParser()
        XMLP.setMapaFile("mapFile")
        XMLP.setPlayersFile("playersFile")
        self.Game = XMLP.reconstruirGame(cliente.nick)
        self.Game.mapa.escalaX = 680.0/520.0
        self.Game.mapa.escalaY = 680.0/520.0
        self.Game.PosicionarPlayer(680,680)
        self.Cliente = cliente
        self.Cliente.setWindow(self)
        self.posX_chat = (780.0/self.width_V)*self.width
        self.posY_chat = (350.0 /self.heigth_V)*self.heigth
        self.window = sf.RenderWindow(sf.VideoMode(self.width, self.heigth), "BOMBERMAN")
        self.Evento = sf.Event()      
        self.window.SetFramerateLimit(60)
        self.CrearChat()
        self.CrearCronometro()

    def CrearChat(self):
        self.Chat = chat(self.posX_chat + 5, self.posY_chat,self.width,self.heigth)
        self.Chat.SetCliente(self.Cliente)
        self.Cliente.setChat(self.Chat)        

    def CrearCronometro(self):
        self.Cronometro = Cronometro(0,0)
        self.Cronometro.setTime(self.Game.tiempo)
        self.Cronometro.setRectangule(self.posX_chat + 10,100,44,44)
        
    def VerificarFocus(self,x,y):
        if x >= self.posX_chat and x <= self.posX_chat + (240.0/self.width_V)* self.width_C :
            if y >= self.posY_chat and y <= self.posY_chat + (330.0/self.heigth_V)*self.heigth_C:
                return True
        if not x >= self.posX_chat and x <= self.posX_chat + (240.0/self.width_V)* self.width_C :
            if not y >= self.posY_chat and y <= self.posY_chat + (330.0/self.heigth_V)*self.heigth_C:
                return False

    def SubirText(self,x,y):
        if x >= self.posX_chat and x <= self.posX_chat + (240.0/self.width_V)* (self.width_C/2):
            if y >= self.posY_chat+((330.0/self.heigth_V)*self.heigth_C) - 60 and y <= self.posY_chat+(330.0/self.heigth_V)*self.heigth_C-30:
                return True

    def BajarText(self,x,y):
        if x >= self.posX_chat +(240.0/self.width_V)* (self.width_C/2)+10 and x <= self.posX_chat + (240.0/self.width_V)* self.width_C:
            if y >= self.posY_chat+((330.0/self.heigth_V)*self.heigth_C) - 60 and y <= self.posY_chat+(330.0/self.heigth_V)*self.heigth_C-30:
                return True
    def Send(self,x,y):
        if x >= self.posX_chat +(240.0/self.width_V)*self.width_C - 30 and x <= self.posX_chat + (240.0/self.width_V)* self.width_C:
            if y >= self.posY_chat+((330.0/self.heigth_V)*self.heigth_C) - 40 and y <= self.posY_chat+(330.0/self.heigth_V)*self.heigth_C:
                return True
            
    def MoverPlayer(self, direction, nick):
        self.Game.SetDirection(nick, direction)

    def DetenerPlayer(self, direction, nick, x, y):
        self.Game.SetDirection(nick, direction)
        self.Game.PosicionarPlayer2(nick, x, y)

    def PonerBomba(self, nick):
        self.Game.PonerBomba(nick, self.Cliente, False)

    def Run(self):
        self.Game.mapa.reproducirMusica()
        self.Cronometro.start()
        input = self.window.GetInput()
        self.Game.Update(self.window.GetFrameTime())
        quit = False
        nick = self.Cliente.nick
        Statics.SetClient(self.Cliente)
        while not quit:
            x = input.GetMouseX()
            y = input.GetMouseY()
            frameTime = self.window.GetFrameTime()
            self.Game.Update(frameTime)
            if self.window.GetEvent(self.Evento):
                if self.Evento.Type == sf.Event.Resized:
                    self.heigth_V = float(self.Evento.Size.Height)
                    self.width_V = float(self.Evento.Size.Width)
                    self.posX = (780.0/self.width_V)*self.width
                    self.posY = (373.0/self.heigth_V)*self.heigth

                if self.Evento.Type == sf.Event.KeyPressed:
                    if not self.Focus:
                        evento = self.Evento
                        if evento.Key.Code == sf.Key.Left:
                            self.Game.MoverPlayer(nick, "Izquierda", frameTime)
                            self.Cliente.__send__("MOVEPLAYER:Izquierda")
                        if evento.Key.Code == sf.Key.Right:
                            self.Game.MoverPlayer(nick, "Derecha", frameTime)
                            self.Cliente.__send__("MOVEPLAYER:Derecha")
                        if evento.Key.Code == sf.Key.Up:
                            self.Game.MoverPlayer(nick, "Arriba", frameTime)
                            self.Cliente.__send__("MOVEPLAYER:Arriba")
                        if evento.Key.Code == sf.Key.Down:
                            self.Game.MoverPlayer(nick, "Abajo", frameTime)
                            self.Cliente.__send__("MOVEPLAYER:Abajo")
                        if evento.Key.Code == sf.Key.Space:
                            self.Game.PonerBomba(nick, self.Cliente, True)

                if self.Evento.Type == sf.Event.KeyReleased:
                    if not self.Focus:
                        evento = self.Evento
                        if evento.Key.Code == sf.Key.Left or evento.Key.Code == sf.Key.Right or evento.Key.Code == sf.Key.Up or evento.Key.Code == sf.Key.Down:
                            pla = self.Game.PlayerPosition(nick)
                            self.Cliente.__send__("STOPPLAYER:"+nick+","+str(int(pla[0]))+","+str(int(pla[1])))
                            #self.Cliente.__send__("STOPPLAYER:"+nick)
                            self.Game.MoverPlayer(nick,"None",frameTime)
                
                if self.Evento.Type == sf.Event.Closed:
                    quit = True
                    
                if self.Evento.Type == sf.Event.MouseButtonPressed:
                    self.Focus = self.VerificarFocus(x,y)
                    if(self.Focus):
                        if(self.SubirText(x,y)):
                            self.Chat.SubirTexto()
                        if(self.BajarText(x,y)):
                            self.Chat.BajarTexto()
                        if(self.Send(x,y)):
                            self.Chat.Send()
                        
                if self.Evento.Type == sf.Event.TextEntered:
                    if self.Focus:                    
                        self.Chat.Update(self.Evento)
            self.window.Clear(self.negro)
            self.Chat.Draw(self.window)
            self.Game.Draw(self.window.GetFrameTime(),self.window)
            self.Cronometro.Draw(self.window)
            self.window.Display()
        self.Cliente.stop()
        self.window.Close()
        
