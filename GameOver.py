from PySFML import sf
from Sumary import Sumary
class GameOver:
    window = None
    negro = None
    blanco = None
    Evento = None
    Fondo = None
    coment = None
    teamScores = None
    DIRECTORIO = "bgs/"
    
    def __init__(self,com,Scores):
        self.coment = com
        print Scores
        self.teamScores = Scores
        self.blanco = sf.Color(250, 250, 250)
        self.negro =  sf.Color(0, 0, 0)
        self.window = sf.RenderWindow(sf.VideoMode(700, 400), "BOMBERMAN")
        self.Evento = sf.Event()
        self.PintarFondo()

    def PintarFondo(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+self.coment+"_Screen.png")
        self.Fondo = sf.Sprite(image)
        self.Fondo.Resize(700,400)
        self.Fondo.SetCenter(0, 0)
        self.Fondo.SetPosition(0,0)

    def DeterminarFocus(self,x,y):
        if(self.coment == "Draw"):
            if(x >= 60 and x < 260):
                if(y>=337 and y <364):
                    self.window.Close()
                    s = Sumary(self.teamScores)
                    s.Update()
                
        if(self.coment == "Victory"):
            if(x >= 118 and x < 318):
                if(y>=189 and y <213):
                    self.window.Close()
                    s = Sumary(self.teamScores)
                    s.Update()
                
        if(self.coment == "Defeat"):
           if(x >= 89 and x < 288):
                if(y>=182 and y <207):
                    self.window.Close()
                    s = Sumary(self.teamScores)
                    s.Update()
        
        
    def Pintar(self):
        self.window.Draw(self.Fondo)

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
                    self.DeterminarFocus(x,y)

            #print str(x) +"--"+str(y)
            self.window.Clear(self.blanco)
            self.Pintar()
            self.window.Display()            
        self.window.Close()

