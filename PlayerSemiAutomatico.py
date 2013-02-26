from Player import Player

class PlayerSemiAutomatico(Player):
    direccion = "None"

    def __init__(self,nombre,vidas, posX, posY, sp):
        super(PlayerSemiAutomatico,self).__init__(nombre,vidas, posX, posY, sp)

    def Update(self, gameTime):
        #self.AutoMover(gameTime)
        super(PlayerSemiAutomatico, self).Update(gameTime)
        

if __name__ == "__main__":
    P = PlayerSemiAutomatico("a",2,3,2,"dfsd")
    P.AutoMover(1)
