from Bomba import Bomba

class BombaNormal(Bomba):
    DIRECTORIO = "bombas/"
    def __init__(self, x, y, atrav):
        super(BombaNormal, self).__init__(self.DIRECTORIO+"listaBombas.png",x,y, atrav)

    def Update(self, gameTime):
        super(BombaNormal, self).Update(gameTime)


if __name__ == "__main__":
    b = BombaNormal()
    print b.spriteName
