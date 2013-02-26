from MySprite import MySprite
from PySFML import sf

class Wall(MySprite):
    def __init__(self, x, y, w, h):
        super(Wall, self).__init__("bloques/spriteI.png",x,y,10)
        self.crearPared(x, y, w, h)

    def crearPared(self, x, y, w, h):
        self.ancho = w
        self.alto = h
        self._create_collision_area2(x,y,w,h)
        self.post_update("Estatico")


if __name__  == "__main__":
    a = Wall(1,2,3,4)
