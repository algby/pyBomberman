from MySprite import MySprite
from Entidades import Entidades
#ahilyn| ma jose
class Fuego(MySprite):
    def __init__(self, rejilla, x, y):
        directorio = "fuego/"
        super(Fuego, self).__init__(directorio+rejilla+".png", x, y, 0)
        self.ancho = 52.3077
        self.alto = 52.3077
        self.tiempo = 0
        self.cont = 0

    def animar(self, gameTime):
        if self.tiempo>=0.125:
            if self.cont == 0:
                self.visible = False
                self.cont = 1
            color = self.GetColor()
            if color.a>11:
                color.a /= 2
            self.SetColor(color)
            self.tiempo = 0
        else:
            self.tiempo += gameTime

class Explosion:
    def __init__(self, rango, i, j, atrav):        
        self.exp_abajo = []
        self.exp_arriba = []
        self.exp_derecha = []
        self.exp_izquierda = []

        self.exp_centro = None

        self.rango = rango
        self.i = i
        self.j = j
        self.atraviesa = atrav
        self.w = 52.3076923077
        self.crearExplosion()

    def setAtraviesa(self, a):
        self.atraviesa = a

    def Draw(self, gameTime, window):
        for b in self.exp_abajo:
            window.Draw(b)
        for r in self.exp_derecha:
            window.Draw(r)
        for t in self.exp_arriba:
            window.Draw(t)
        for l in self.exp_izquierda:
            window.Draw(l)
        window.Draw(self.centro)

    def endExplosion(self):
        for b in self.exp_abajo:
            Entidades.eliminarFuego(b)
        for r in self.exp_derecha:
            Entidades.eliminarFuego(r)
        for t in self.exp_arriba:
            Entidades.eliminarFuego(t)
        for l in self.exp_izquierda:
            Entidades.eliminarFuego(l)
        Entidades.eliminarFuego(self.centro)

    def Update(self, gameTime):
        for b in self.exp_abajo:
            b.animar(gameTime)
            b.post_update("Estatico")
        for r in self.exp_derecha:
            r.animar(gameTime)
            r.post_update("Estatico")
        for t in self.exp_arriba:
            t.animar(gameTime)
            t.post_update("Estatico")
        for l in self.exp_izquierda:
            l.animar(gameTime)
            l.post_update("Estatico")
        if self.centro != None:
            self.centro.animar(gameTime)
            self.centro.post_update("Estatico")

    def crearExplosion(self):
        scale = 1.05
        #scale = 0.844
        w = self.w
        self.centro = Fuego("centro", self.i, self.j)
        self.centro.SetScale(scale,scale)
        Entidades.agregarFuego(self.centro)
        i = 0
        indexI = int((self.i-self.w)/w)
        indexJ = int((self.j-self.w)/w)
        j = 0
        for i in range(self.rango-1):
            tupla = Entidades.existeBloque(indexI+i,indexJ)
            if (not tupla[0]) or (self.atraviesa and tupla[1]):
                newFuego = Fuego("Extension_Derecha",self.i+(i+1)*w,self.j)
                newFuego.SetScale(scale,scale)
                newFuego.ancho = 40
                newFuego.alto = 40
                x,y = newFuego.GetPosition()
                newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
                self.exp_derecha.append(newFuego)
                Entidades.agregarFuego(newFuego)
            else:
                j = 1
                break
        if self.rango-1 == i:
            tupla = Entidades.existeBloque(indexI+i,indexJ)
            if (not tupla[0]) or (self.atraviesa and tupla[1]):
                newFuego = Fuego("Terminal_Derecha",self.i+(i+1)*w,self.j)
                newFuego.SetScale(scale,scale)
                newFuego.ancho = 40
                newFuego.alto = 40
                x,y = newFuego.GetPosition()
                newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
                self.exp_derecha.append(newFuego)
                Entidades.agregarFuego(newFuego)
        if self.rango == 1 or j == 0:
            newFuego = Fuego("Terminal_Derecha", self.i+self.rango*w,self.j)
            newFuego.SetScale(scale,scale)
            newFuego.ancho = 40
            newFuego.alto = 40
            x,y = newFuego.GetPosition()
            newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
            self.exp_derecha.append(newFuego)
            Entidades.agregarFuego(newFuego)
        
        #----------------------------------------------------
        j = 0
        for i in range(self.rango-1):
            tupla = Entidades.existeBloque(indexI-i,indexJ)
            if (not tupla[0]) or (self.atraviesa and tupla[1]):
                newFuego = Fuego("Extension_Izquierda",self.i-(1+i)*w,self.j)
                newFuego.SetScale(scale,scale)
                newFuego.ancho = 40
                newFuego.alto = 40
                x,y = newFuego.GetPosition()
                newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
                self.exp_izquierda.append(newFuego)
                Entidades.agregarFuego(newFuego)
            else:
                j = 1
                break
        if self.rango == 1 or j == 0:
            newFuego = Fuego("Terminal_Izquierda",self.i-self.rango*w,self.j)
            newFuego.SetScale(scale,scale)
            newFuego.ancho = 40
            newFuego.alto = 40
            x,y = newFuego.GetPosition()
            newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
            self.exp_derecha.append(newFuego)
            Entidades.agregarFuego(newFuego)
        #----------------------------------------------------
        j = 0
        for i in range(self.rango-1):
            tupla = Entidades.existeBloque(indexI,indexJ+i)
            if (not tupla[0]) or (self.atraviesa and tupla[1]):
                newFuego = Fuego("Extension_Abajo",self.i,self.j+(1+i)*w)
                newFuego.SetScale(scale,scale)
                newFuego.alto = 40
                newFuego.ancho = 40
                x,y = newFuego.GetPosition()
                newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
                self.exp_abajo.append(newFuego)
                Entidades.agregarFuego(newFuego)
            else:
                j = 1
                break
        if j < 1 or self.rango == 1:
            newFuego = Fuego("Terminal_Abajo",self.i,self.j+self.rango*w)
            newFuego.SetScale(scale,scale)
            newFuego.alto = 40
            newFuego.ancho = 40
            x,y = newFuego.GetPosition()
            newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
            self.exp_derecha.append(newFuego)
            Entidades.agregarFuego(newFuego)
        #----------------------------------------------------
        j = 0
        for i in range(self.rango-1):
            tupla = Entidades.existeBloque(indexI, indexJ-i)
            if (not tupla[0]) or (self.atraviesa and tupla[1]):
                newFuego = Fuego("Extension_Arriba",self.i,self.j-(i+1)*w)
                newFuego.SetScale(scale,scale)
                newFuego.alto = 40
                newFuego.ancho = 40
                x,y = newFuego.GetPosition()
                newFuego._create_collision_area2(x+(w-40)/2,y,40,30)
                self.exp_arriba.append(newFuego)
                Entidades.agregarFuego(newFuego)
            else:
                j = 1
                break
        if j < 1 or self.rango == 1:
            newFuego = Fuego("Terminal_Arriba",self.i,self.j-self.rango*w)
            newFuego.SetScale(scale,scale)
            newFuego.alto = 40
            newFuego.ancho = 40
            x,y = newFuego.GetPosition()
            newFuego._create_collision_area2(x+(w-40)/2,y,40,40)
            self.exp_derecha.append(newFuego)
            Entidades.agregarFuego(newFuego)

if __name__ == "__main__":
    exp = Explosion(3,3,3)
