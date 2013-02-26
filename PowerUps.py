import random
from PySFML import sf

class PowerUps:
    totalUsados = 0
    totalPowerUps = 0
    def __init__(self):
        self.powerUps = dict()
        self.directorio = 'powerups/'
        self.counting = dict()
        self.tipos = []
        self.tablaProbs = []
        self.__fillPowers__()
       
    def generarSiguiente(self):
        if self.totalUsados >= self.totalPowerUps:
            return (self.tipos[0], self.powerUps[self.tipos[0]][0])
        else:
            indexFloat = random.random()
            #index = random.randrange(0, len(self.tipos)-1)
            #index = int(round(indexFloat * len(self.tipos)))
            index = self.__getIndex__(indexFloat)
            
            if index is 0:
                return (self.tipos[0],self.powerUps[self.tipos[0]][0])

            if self.counting[self.tipos[index]] > self.__porcent__(index):
                return self.generarSiguiente()
            else:
                self.counting[self.tipos[index]] = self.counting[self.tipos[index]] + 1
                self.totalUsados += 1
                
                return (self.tipos[index],self.powerUps[self.tipos[index]][0])

    def __getIndex__(self, dec):
        tot = 0
        val = int(round(dec * 100))
        #print str(val)
        for i in range(len(self.tablaProbs)):
            if self.tablaProbs[i]>dec:
                return i-1
        return 0
      
    def __fillPowers__(self):
        self.tipos.append('ninguno')
        self.tipos.append('Bomb_Up')
        self.tipos.append('Fire')
        self.tipos.append('Skate')
        self.tipos.append('Sandal')
        self.tipos.append('Full_Fire')
        self.tipos.append('Pierce_Bomb')
        
        self.powerUps[self.tipos[0]] = ('ninguno',70)
        self.powerUps[self.tipos[1]] = (self.directorio+'Bomb_Up.png',20)
        self.powerUps[self.tipos[2]] = (self.directorio+'Fire.png',6)
        self.powerUps[self.tipos[3]] = (self.directorio+'Skate.png',2)
        self.powerUps[self.tipos[4]] = (self.directorio+'Sandal.png',1)
        self.powerUps[self.tipos[5]] = (self.directorio+'Full_Fire.png',1)
        self.powerUps[self.tipos[6]] = (self.directorio+'Pierce_Bomb.png',1)

        self.counting[self.tipos[0]] = 0
        self.counting[self.tipos[1]] = 0
        self.counting[self.tipos[2]] = 0
        self.counting[self.tipos[3]] = 0
        self.counting[self.tipos[4]] = 0
        self.counting[self.tipos[5]] = 0
        self.counting[self.tipos[6]] = 0

        #la probabilidad de aparicion del i-esimo elemento
        #es uno menos la del (i-1)-esimo termino
        self.tablaProbs.append(0.5)
        self.tablaProbs.append(0.7)
        self.tablaProbs.append(0.9)
        self.tablaProbs.append(0.92)
        self.tablaProbs.append(0.95)
        self.tablaProbs.append(0.97)
        self.tablaProbs.append(0.99)
        self.tablaProbs.append(1.0)

    def getSprite(self,tipo):
        imagen = sf.Image(self.powerUps[tipo][0])
        return sf.Sprite(imagen)
    
    def __porcent__(self, i):
        return int(round(self.totalPowerUps * (self.tablaProbs[i+1]-self.tablaProbs[i])))
  
