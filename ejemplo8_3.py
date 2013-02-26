#! /usr/bin/env python
#-*- coding: utf-8 -*-

from PySFML import sf
import os
from ClientTesting import SocketClient

def area_to_tuple(area):
    left = area.Left
    top = area.Top
    right = area.Right
    bottom = area.Bottom
    width = area.GetWidth()
    height = area.GetHeight()
    return (left, top, right, bottom, width, height)

class MySprite(sf.Sprite):
    
    
    def __init__(self, rejilla, x, y, ventana, cora):
        self.cliente = SocketClient()
        # usamos la clase sf.Image para cargar una imagen dada por **rejilla**
        self.imagen    = sf.Image()
        self.imagen.LoadFromFile(rejilla)
        # hacemos el fondo transparente
        colorfondo     = self.imagen.GetPixel(0, 0)
        self.imagen.CreateMaskFromColor(colorfondo)
        # asignamos la imagen a nuestra clase MySprite
        sf.Sprite.__init__(self, self.imagen)
        # colocamos el sprite a la mitad de la pantalla
        self.SetX(x)
        self.SetY(y)
        # declaramos un par de atributos
        self.tiempo    = 0.0
        self.frame_pos = 0
        # el otro atributo para guardar las coordenadas de los sprites
        self.coord_frm = {}
        self.velocidad = 80
        self.visible = False
        self._create_collision_area()
        self.collision_ratio = cora
        self.center = (x, y)
        self.ventana = ventana

        
    def listframes(self, filas, columnas, ancho, alto):
        """ añade los frames recortados y enumerados a coord_frm. """
        # tomaremos la cantidad de filas y columnas para crear un bucle *for*
        # e iremos buscando y recortando los frames del sprite sheet. Esta es una
        # manera semi-automatica de preparar los frames de un sprite para usar en
        # su animacion, por eso es siempre conveniente tener un sprite sheet donde
        # cada uno de sus elementos tenga un ancho y una altura fija, en cada frame.
        frame = 1
        for fila in range(0, filas):
            for columna in range(0, columnas):
                # haciendo un poco de matematicas resolvemos el problema de
                # ubicar coordenas en el sprite sheet
                izq = columna       * ancho
                arr = fila          * alto
                der = (columna + 1) * ancho
                abj = (fila    + 1) * alto
                self.coord_frm[frame] = izq, arr, der, abj
                frame = frame  + 1
    
    def animar(self, ventana, orientacion, frames):
        """ Anima el sprite, no lo mueve (por el momento). """
        
        # revisamos si la cantidad de tiempo transcurrido es mayor o igual a 30
        # cuadros de animacion o 1/30. si es asi, pasamos al siguiente frame,
        # obtenemos de vuelta las coordenas del rectangulo correspondiente a ese
        # cuadro de la animacion para que luego sea dibujado en pantalla... 
        # asi sucesivamente.
        
        self.FlipX(orientacion)
        if self.tiempo > 5.0/60:
            self.frame_pos = self.frame_pos + 1
            try:
                coord = self.getframe(frames[self.frame_pos])
                # sf.IntRect no acepta tuplas, por eso este raro hack...
                self.SetSubRect(sf.IntRect(coord[0], coord[1],\
                                           coord[2], coord[3]))
            except IndexError:
                if self.tiempo > 3.0/60:
                    self.frame_pos = 0
            self.tiempo = 0.0
        else:
            self.tiempo = self.tiempo + ventana.GetFrameTime()
    
    def setframe(self, frame):
        """ establece un unico frame para el sprite. """
        
        coord = self.getframe(frame)
        # sf.IntRect no acepta tuplas, por eso este raro hack...
        self.SetSubRect(sf.IntRect(coord[0], coord[1],\
                                   coord[2], coord[3]))
    
    def getframe(self, frame):
        """ retorna las coordenadas de un frame dentro del sprite sheet. """
        try:
            return self.coord_frm[frame]
        except KeyError:
            raise KeyError, "No existe el frame {0}".format(frame)

    def setVelocidad(self, velocidad):
        self.velocidad = velocidad

    def autoMover(self, direccion, orientacion):
        if direccion == "Derecha":
            self.animar(self.ventana, orientacion, [48, 49, 50, 51, 52, 53])
            self.SetX(self.GetPosition()[0]+self.velocidad*self.ventana.GetFrameTime())
            self.post_update()
        if direccion == "Izquierda":
            self.animar(self.ventana, orientacion, [48, 49, 50, 51, 52, 53])
            self.SetX(self.GetPosition()[0]-self.velocidad*self.ventana.GetFrameTime())
            self.post_update()
        if direccion == "Arriba":
            self.animar(self.ventana, orientacion, [30, 31, 32, 33, 34, 35])
            self.SetY(self.GetPosition()[1]-self.velocidad*self.ventana.GetFrameTime())
            self.post_update()
        if direccion == "Abajo":
            self.animar(self.ventana, orientacion, [6, 7, 8, 9, 10, 11])
            self.SetY(self.GetPosition()[1]+self.velocidad*self.ventana.GetFrameTime())
            self.post_update()

    def _create_collision_area(self):
        self.collision_area = sf.IntRect(0, 0, 0, 0)

    def post_update(self):
        x, y = self.GetPosition()
        center_x, center_y = self.center
        #y-= center_y

        self.collision_area.Left = x - self.collision_ratio
        self.collision_area.Right = x + self.collision_ratio
        self.collision_area.Top = y - self.collision_ratio
        self.collision_area.Bottom = y + self.collision_ratio

    def collide_with(self, obj):
        area_to_tuple(self.collision_area)
        area_to_tuple(obj.collision_area)
        return self.collision_area.Intersects(obj.collision_area)
        

if __name__ == "__main__":
    # la sentencia de arriba previene que este codigo se ejecute cuando es
    # importado desde otro fichero de python por import
    
    # Como que me da mucha pereza usare los objetos de color de sf.Color,
    # Vamos a usar variables para esos objetos de color.
    #Black   = sf.Color.Black
    
    # creamos la ventana del juego
    ventana = sf.RenderWindow(sf.VideoMode(800, 500), "PySFML: Sprite Test")
    #ventana.SetFramerateLimit(60)
    
    # creamos una instancia de sf.Event para el manejo de los eventos en el juego
    evento  = sf.Event()
    
    # obtenemos el input de los eventos de la ventana creada, mira sf.Input para mas informacion
    # parece ser que no es necesario declarar este objeto dentro del loop para actualizar su estado...
    entrada = ventana.GetInput()
    
    # cargamos el SpriteSheet
    ryu = MySprite("ryu_spritesheet.png", 38, 27, ventana, 20)
    ryu.cliente.window = ventana
    ####ryu.cliente.__connect__("196.254.229.236", 1245, "nestor")

    bmb = MySprite("bomb_sheet2.png", 0, 0, ventana, 10)

    bot = MySprite("ryu_spritesheet.png", 398, 260, ventana, 20)
    
    #              filas, columnas, ancho, alto
    ryu.listframes(12,           6,    44,   49)
    bmb.listframes(3, 2, 52, 53)
    bot.listframes(12,6,44,49)
    # el sprite esta listo para ser animado.
    
    ryu.setframe(1)
    bmb.setframe(1)
    bot.setframe(1)

    
    # Preparando la musica
    musica = sf.Music()
    boom = sf.Music()
    step = sf.Music()
    musica.OpenFromFile("Pegasus_fantasy_8bit.ogg")
    boom.OpenFromFile("FlameMagic.ogg")
    step.OpenFromFile("Thip.ogg")

    musica.SetLoop(True)
    # antes de ponerlo en play debemos usar este metodo
    # 2 == estereo, 44100 samplerate del archivo
    musica.Initialize(2, 44100)
    boom.Initialize(2,44100)
    step.Initialize(2,44100)
    # finalmente, lo ponemos en play()
    musica.Play()
    
    # variable para terminar el bucle del juego
    salir = False

    # variable para contar bombas
    kick = 0

    fondo = sf.Image()
    fondo.LoadFromFile('Fondo1-01.png')
    fondue = sf.Sprite(fondo)

    exp = sf.Image()
    exp.LoadFromFile('B7.png')
    explosion = sf.Sprite(exp)

    # variables de control cantidad de bombas
    azules = 0

    mover_Derecha = False
    mover_Izquierda = False
    mover_Arriba = False
    mover_Abajo = False
    poner_Bomba = False
    explotar = False
    timer = sf.Clock()


    bot.post_update()
    # bucle principal del juego
    while not salir:
        if mover_Derecha:
            ryu.autoMover("Derecha", False)
            ryu.ventana.Draw(fondue)
            ryu.ventana.Draw(ryu)
            if poner_Bomba and bmb.visible:
                bmb.animar(ryu.ventana, False, [1, 2, 3, 4])
                bmb.post_update()
                ryu.ventana.Draw(bmb)
            if explotar:
                ryu.ventana.Draw(explosion)
            ryu.ventana.Draw(bot)
            ryu.ventana.Display()
        if mover_Izquierda:
            ryu.autoMover("Izquierda", True)
            ryu.ventana.Draw(fondue)
            ryu.ventana.Draw(ryu)
            if poner_Bomba and bmb.visible:
                bmb.animar(ryu.ventana, False, [1, 2, 3, 4])
                bmb.post_update()
                ryu.ventana.Draw(bmb)
            if explotar:
                ryu.ventana.Draw(explosion)
            ryu.ventana.Draw(bot)
            ryu.ventana.Display()
        if mover_Arriba:
            ryu.autoMover("Arriba", False)
            ryu.ventana.Draw(fondue)
            ryu.ventana.Draw(ryu)
            if poner_Bomba and bmb.visible:
                bmb.animar(ryu.ventana, False, [1, 2, 3, 4])
                bmb.post_update()
                ryu.ventana.Draw(bmb)
            if explotar:
                ryu.ventana.Draw(explosion)
            ryu.ventana.Draw(bot)
            ryu.ventana.Display()
        if mover_Abajo:
            ryu.autoMover("Abajo", False)
            ryu.ventana.Draw(fondue)
            ryu.ventana.Draw(ryu)
            if poner_Bomba and bmb.visible:
                bmb.animar(ryu.ventana, False, [1, 2, 3, 4])
                bmb.post_update()
                ryu.ventana.Draw(bmb)
            if explotar:
                ryu.ventana.Draw(explosion)
            ryu.ventana.Draw(bot)
            ryu.ventana.Display()
        if timer.GetElapsedTime() > 3.0 and poner_Bomba == True:
            poner_Bomba = False
            explotar = True
            bmb.visible = False
            timer = sf.Clock()
        if timer.GetElapsedTime() > 1.5:
            explotar = False
        if explotar == True:
            ryu.ventana.Draw(explosion)

        if bot.collide_with(bmb) and bmb.visible:
            print 'Bot choca con Bomba'

        if ryu.collide_with(bot):
            mover_Derecha = False
            mover_Izquierda = False
            mover_Arriba = False
            mover_Abajo = False

        while ventana.GetEvent(evento):
            
            if evento.Type == sf.Event.Closed:
                ryu.cliente.stop()
                salir = True
                musica.Stop()

            if evento.Type == sf.Event.MouseButtonPressed:
                pass
                
            if evento.Type == sf.Event.KeyPressed:
                msg = "MOVE:"+str(ryu.GetPosition()[0])+","+str(ryu.GetPosition()[1])
                tot = len(msg)
                tot = tot + len(str(tot)) + 2
                ########sent = ryu.cliente.__send__(msg)
                if evento.Key.Code == sf.Key.Escape:
                    salir = True
                    musica.Stop()
                #if evento.Key.Code == sf.Key.Right:                   
                if evento.Key.Code == sf.Key.Right:
                    mover_Arriba = False
                    mover_Abajo = False
                    mover_Izquierda = False
                    mover_Derecha = True
                #if evento.Key.Code == sf.Key.Left:
                if evento.Key.Code == sf.Key.Left:
                    mover_Arriba = False
                    mover_Abajo = False
                    mover_Derecha = False
                    mover_Izquierda = True
                #if evento.Key.Code == sf.Key.Up:
                if evento.Key.Code == sf.Key.Up:
                    mover_Abajo = False
                    mover_Derecha = False
                    mover_Izquierda = False
                    mover_Arriba = True
                #if evento.Key.Code == sf.Key.Down:
                if evento.Key.Code == sf.Key.S or evento.Key.Code == sf.Key.Down:
                    mover_Arriba = False
                    mover_Derecha = False
                    mover_Izquierda = False
                    mover_Abajo = True
                #if evento.Key.Code == sf.Key.Space:
                if evento.Key.Code == sf.Key.R:
                    mover_Arriba = False
                    mover_Derecha = False
                    mover_Izquierda = False
                    mover_Abajo = False
                if evento.Key.Code == sf.Key.U or evento.Key.Code == sf.Key.Space:
                    bmb.SetPosition(ryu.GetPosition()[0], ryu.GetPosition()[1])
                    explosion.SetPosition(bmb.GetPosition()[0],bmb.GetPosition()[1])
                    poner_Bomba = True
                    bmb.visible = True
                    timer = sf.Clock()
                if evento.Key.Code == sf.Key.Q:
                    ryu.velocidad = ryu.velocidad+2
                if evento.Key.Code == sf.Key.E:
                    ryu.velocidad = 5
                if evento.Key.Code == sf.Key.X:
                    print ryu.GetPosition()[0], ryu.GetPosition()[1]
            

            ventana.Draw(fondue)
            ventana.Draw(ryu)
            ventana.Draw(bot)
            ventana.Display()
            
    ventana.Close()
