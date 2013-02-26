from PySFML import sf

class Sonidos:
    def __init__(self):
        self.ALL_SOUNDS = []
        self.POWERUP = "powerup"
        self.DIRECTORIO = "music/"
        self.EXPLOSION = "explosion"
        self.SCREEN_SERVER1 = "screen_server1"
        self.SCREEN_SERVER2 = "screen_server2"
        self.SCREEN_CLIENT1 = "screen_client1"
        self.SCREEN_CLIENT2 = "screen_client2"
        self.GAME_OVER = "gameover"

        self.sserver1 = None
        self.sserver2 = None
        self.sclient1 = None
        self.sclient2 = None
        self.gover = None
        
    def PlayExplosion(self):
        self.PlayParam(self.DIRECTORIO+self.EXPLOSION+".ogg", False)

    def PlayPowerUp(self):
        self.PlayParam(self.DIRECTORIO+self.POWERUP+".ogg", False)

    def PlayScreenServer1(self):
        self.sserver1 = self.PlayParam(self.DIRECTORIO+self.SCREEN_SERVER1+".ogg", True)

    def PlayScreenServer2(self):
        self.sserver2 = self.PlayParam(self.DIRECTORIO+self.SCREEN_SERVER2, True)

    def PlayScreenClient1(self):
        self.sclient1 = self.PlayParam(self.DIRECTORIO+self.SCREEN_CLIENT1+".ogg", True)

    def PlayGameOver(self):
        self.gover = self.PlayParam(self.DIRECTORIO+self.GAME_OVER, True)

    def StopGameOver(self):
        if self.gover != None:
            self.gover.Stop()

    def StopScreenServer1(self):
        if self.sserver1 != None:
            self.sserver1.Stop()

    def StopScreenServer2(self):
        if self.sserver2 != None:
            self.sserver2.Stop()

    def StopScreenClient1(self):
        if self.sclient1 != None:
            self.sclient1.Stop()
        
    def PlayParam(self, path, loop):
        exp = sf.Music()
        exp.OpenFromFile(path)
        exp.Initialize(2, 44100)
        exp.SetLoop(loop)
        self.ALL_SOUNDS.append(exp)
        exp.Play()
        return exp

    def StopAll(self):
        for sound in self.ALL_SOUNDS:
            sound.Stop()


        
