from PySFML import sf
import threading
import time

class Cronometro:
    W = 0
    H = 0
    mins = 0
    segs = 0
    posX = 0
    posY = 0    
    timer = None
    crono = None
    timeString = ""
    timeout = False
    

    def __init__(self, mins, segs):
        self.mins = mins
        self.segs = segs
        self.crono = sf.String('')
        self.crono.SetSize(18)

    def setTime(self, secs):
        self.mins = secs/60
        self.segs = secs%60

    def setRectangule(self, x, y, width, height):
        self.posX = x
        self.posY = y
        self.W = width
        self.H = height

    def formarString(self):
        if len(str(self.mins))==1:
            self.timeString = "0"+str(self.mins)
        else:
            self.timeString = str(self.mins)

        self.timeString += ":"
        
        if len(str(self.segs))==1:
            self.timeString += "0"+str(self.segs)
        else:
            self.timeString += str(self.segs)

    def start(self):
        t = threading.Thread(target = self.threadTickTock)
        t.start()
        

    def threadTickTock(self):
        self.timer = threading.Timer(1, self._tictoc_)
        self.timer.start()

    def _tictoc_(self):
        while self.mins>0 or self.segs>0:
            self.formarString()
            self.crono.SetText(self.timeString)
            if self.segs>=0:
                self.segs -= 1
                if self.segs <0:
                    self.mins -= 1
                    self.segs = 59
            else:
                pass
            time.sleep(1)
        self.timer.cancel()
        self.timeout = True

    def Draw(self, window):
        self.crono.SetPosition(self.posX, self.posY)
        window.Draw(self.crono)

