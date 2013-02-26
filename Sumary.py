from PySFML import sf
class Sumary:
    blanco = None
    negro = None
    window = None
    Evento = None
    teamScores = None
    Fondo = None
    DIRECTORIO = "bgs/"

    Rojo = None
    Verde = None
    Azul = None
    Amarillo = None
    
    def __init__(self,sumary):
        self.teamScores = sumary
        self.blanco = sf.Color(250, 250, 250)
        self.negro =  sf.Color(0, 0, 0)
        self.window = sf.RenderWindow(sf.VideoMode(700,400), "BOMBERMAN")
        self.Evento = sf.Event()
        self.PintarFondo()
        self.VerificarTeams(sumary)
        
    def VerificarTeams(self,sumary):
        if sumary.has_key('red'):
            r = sumary['red']
            self.PintarRojo(r[0],r[1])
        else:
            self.PintarRojo("_","_")
            
        if sumary.has_key('blue'):
            b = sumary['blue']
            self.PintarAzul(b[0],b[1])
        else:
            self.PintarAzul("_","_")
            
        if sumary.has_key('yellow'):
            y = sumary['yellow']
            self.PintarAmarillo(y[0],y[1])
        else:
            self.PintarAmarillo("_","_")
            
        if sumary.has_key('green'):
            g = sumary['green']
            self.PintarVerde(g[0],g[1])
        else:
            self.PintarVerde("_","_")
            
    def PintarFondo(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"Game_Summary.png")
        self.Fondo = sf.Sprite(image)
        self.Fondo.Resize(700,400)
        self.Fondo.SetCenter(0, 0)
        self.Fondo.SetPosition(0,0)

    def PintarRojo(self,death,score):
        self.RojoDeath = sf.String(str(death))
        self.RojoDeath.SetColor(self.negro)
        self.RojoDeath.SetCenter(0,0)
        self.RojoDeath.SetPosition(192+(346-197)/2,108)
        self.RojoDeath.SetSize(20)

        self.RojoScore = sf.String(str(score))
        self.RojoScore.SetColor(self.negro)
        self.RojoScore.SetCenter(0,0)
        self.RojoScore.SetPosition(390 + (543-394)/2,108)
        self.RojoScore.SetSize(20)
    
    def PintarVerde(self,death,score):
        self.VerdeDeath = sf.String(str(death))
        self.VerdeDeath.SetColor(self.negro)
        self.VerdeDeath.SetCenter(0,0)
        self.VerdeDeath.SetPosition(192+(346-197)/2,318)
        self.VerdeDeath.SetSize(20)

        self.VerdeScore = sf.String(str(score))
        self.VerdeScore.SetColor(self.negro)
        self.VerdeScore.SetCenter(0,0)
        self.VerdeScore.SetPosition(390 + (543-394)/2,318)
        self.VerdeScore.SetSize(20)
    
    def PintarAzul(self,death,score):
        self.AzulDeath = sf.String(str(death))
        self.AzulDeath.SetColor(self.negro)
        self.AzulDeath.SetCenter(0,0)
        self.AzulDeath.SetPosition(192+(346-197)/2,178)
        self.AzulDeath.SetSize(20)

        self.AzulScore = sf.String(str(score))
        self.AzulScore.SetColor(self.negro)
        self.AzulScore.SetCenter(0,0)
        self.AzulScore.SetPosition(390 + (543-394)/2,178)
        self.AzulScore.SetSize(20)
    
    def PintarAmarillo(self,death,score):
        self.AmarilloDeath = sf.String(str(death))
        self.AmarilloDeath.SetColor(self.negro)
        self.AmarilloDeath.SetCenter(0,0)
        self.AmarilloDeath.SetPosition(192+(346-197)/2,248)
        self.AmarilloDeath.SetSize(20)

        self.AmarilloScore = sf.String(str(score))
        self.AmarilloScore.SetColor(self.negro)
        self.AmarilloScore.SetCenter(0,0)
        self.AmarilloScore.SetPosition(390 + (543-394)/2,248)
        self.AmarilloScore.SetSize(20)
    
    def Pintar(self):
        self.window.Draw(self.Fondo)
        self.window.Draw(self.RojoDeath)
        self.window.Draw(self.RojoScore)
        self.window.Draw(self.VerdeDeath)
        self.window.Draw(self.VerdeScore)
        self.window.Draw(self.AzulDeath)
        self.window.Draw(self.AzulScore)
        self.window.Draw(self.AmarilloDeath)
        self.window.Draw(self.AmarilloScore)
        

    def Update(self):
        input = self.window.GetInput()
        quit = False 
        while not quit:
            x = input.GetMouseX()
            y = input.GetMouseY()     
            while self.window.GetEvent(self.Evento):
                if self.Evento.Type == sf.Event.Closed:
                        quit = True
            #print str(x) +"--"+ str(y)
            self.window.Clear(self.blanco)
            self.Pintar()
            self.window.Display()            
        self.window.Close()
