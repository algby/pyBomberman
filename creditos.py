from PySFML import sf

class Creditos:
    blanco = None
    window = None
    Evento = None
    Fondo = None
    DIRECTORIO = "bgs/"
    
    def __init__(self):
        self.blanco = sf.Color(250, 250, 250)
        self.window = sf.RenderWindow(sf.VideoMode(700,400), "BOMBERMAN")
        self.Evento = sf.Event()
        self.PintarFondo()   
            
    def PintarFondo(self):
        image = sf.Image()
        image.LoadFromFile(self.DIRECTORIO+"Credits.png")
        self.Fondo = sf.Sprite(image)
        self.Fondo.Resize(700,400)
        self.Fondo.SetCenter(0, 0)
        self.Fondo.SetPosition(0,0)
    
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
            #print str(x) +"--"+ str(y)
            self.window.Clear(self.blanco)
            self.Pintar()
            self.window.Display()            
        self.window.Close()
