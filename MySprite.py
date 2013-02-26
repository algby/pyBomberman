from PySFML import sf
from Utilerias import Utilerias

class MySprite(sf.Sprite):

    def __init__(self, rejilla, x, y, cora):
        self.imagen    = sf.Image()
        self.imagen.LoadFromFile(rejilla)
        colorfondo     = self.imagen.GetPixel(0, 0)
        self.imagen.CreateMaskFromColor(colorfondo)
        sf.Sprite.__init__(self, self.imagen)
        self.SetX(x)
        self.SetY(y)
        self.tiempo    = 0.0
        self.frame_pos = 0
        self.coord_frm = {}
        self.visible = True
        self._create_collision_area()
        self.collision_ratio = cora
        self.center = (x, y)
        self.t = 5.0
        self.ancho = 0
        self.alto = 0
        self.related = ""
        self.destruible = True
        self.pasedOnce = False
        self.i = self.j = 0

    def setRelated(self, rel):
        self.related = rel

    def setPosCuadricula(self, i, j):
        self.i = i
        self.j = j
        
    def listframes(self, filas, columnas, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        frame = 1
        for fila in range(0, filas):
            for columna in range(0, columnas):
                izq = columna       * ancho
                arr = fila          * alto
                der = (columna + 1) * ancho
                abj = (fila    + 1) * alto
                self.coord_frm[frame] = izq, arr, der, abj
                frame = frame  + 1
    
    def animar(self, orientacion, frames, gameTime):
        self.FlipX(orientacion)
        if self.tiempo > self.t/60:
            self.frame_pos = self.frame_pos + 1
            try:
                coord = self.getframe(frames[self.frame_pos])
                self.SetSubRect(sf.IntRect(coord[0], coord[1],\
                                           coord[2], coord[3]))
            except IndexError:
                if self.tiempo > self.t/60:
                    self.frame_pos = 0
            self.tiempo = 0.0
        else:
            self.tiempo = self.tiempo + gameTime
    
    def setframe(self, frame):
        coord = self.getframe(frame)
        self.SetSubRect(sf.IntRect(coord[0], coord[1],\
                                   coord[2], coord[3]))
    
    def getframe(self, frame):
        try:
            return self.coord_frm[frame]
        except KeyError:
            raise KeyError, "No existe el frame {0}".format(frame)
            

    def autoMover(self, direccion, orientacion, gameTime):
        if direccion == "Derecha":
            self.animar(orientacion, [16, 15, 13, 14], gameTime)
            self.post_update(direccion)
        if direccion == "Izquierda":
            self.animar(orientacion, [16, 15, 13, 14], gameTime)
            self.post_update(direccion)
        if direccion == "Arriba":
            self.animar(orientacion, [8, 7, 5, 6], gameTime)
            self.post_update(direccion)
        if direccion == "Abajo":
            self.animar(orientacion, [4, 3, 1, 2], gameTime)
            self.post_update(direccion)
        if direccion == "None":
            self.setframe(2)

    def mover(self, direccion, gameTime):
        if direccion == "Izquierda":
            self.autoMover(direccion, True, gameTime)
        else:
            self.autoMover(direccion, False, gameTime)
    
    def _create_collision_area(self):
        x, y = self.GetPosition()
        self.collision_area = sf.IntRect(int(x), int(y), 40, 40)

    def _create_collision_area2(self,x,y,w,h):
        self.collision_area = sf.IntRect(int(x),int(y),int(w),int(h))

    def post_update(self, direccion):
        x, y = self.GetPosition()
        #center_x, center_y = self.center
        #y-= center_y
        if direccion == "Derecha":
            self.collision_area.Left = x + 10
            self.collision_area.Right = x + self.ancho -10
        elif direccion == "Izquierda":
            self.collision_area.Left = x + 10
            self.collision_area.Right = x + self.ancho -  10
        elif direccion == "Abajo":
            self.collision_area.Top = y + self.alto - 10
            self.collision_area.Bottom = y + self.alto
        elif direccion == "Arriba":
            self.collision_area.Top = y + self.alto - 10
            self.collision_area.Bottom = y + self.alto
        elif direccion == "Estatico":
            self.collision_area.Top = y
            self.collision_area.Left = x
            self.collision_area.Right = x + self.ancho*self.GetScale()[0]
            self.collision_area.Bottom = y + self.alto*self.GetScale()[1]
            

    def printCollisionArea(self):
        print "TOP: " + str(self.collision_area.Top)
        print "LEFT: " + str(self.collision_area.Left)
        print "BOTTOM: " + str(self.collision_area.Bottom)
        print "RIGTH: " + str(self.collision_area.Right)
        print "------------------------------------------"
        

    def collide_with(self, obj):
        Utilerias.area_to_tuple(self.collision_area)
        Utilerias.area_to_tuple(obj.collision_area)
        return (self.collision_area.Intersects(obj.collision_area) and self.visible and obj.visible)
