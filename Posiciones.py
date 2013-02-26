posiciones_x_tablero =  dict()

class Posiciones:
    
    tablero = "STAGE1_4"
    @staticmethod
    def init():
        posiciones_x_tablero["STAGE1_4"] = dict()
        posiciones_x_tablero["STAGE1_4"]["escala"] = 1.307692307692308
        escala = posiciones_x_tablero["STAGE1_4"]["escala"]
        posiciones_x_tablero["STAGE1_4"][(0,0)] = (40*escala,40*escala)
        posiciones_x_tablero["STAGE1_4"][(0,1)] = (520*escala,40*escala)
        posiciones_x_tablero["STAGE1_4"][(1,0)] = (40*escala,440*escala)
        posiciones_x_tablero["STAGE1_4"][(1,1)] = (520*escala,440*escala)

        posiciones_x_tablero["STAGE2_4"] = dict()
        posiciones_x_tablero["STAGE2_4"]["escala"] = 1.307692307692308
        escala = posiciones_x_tablero["STAGE2_4"]["escala"]
        posiciones_x_tablero["STAGE2_4"][(0,0)] = (40*escala,40*escala)
        posiciones_x_tablero["STAGE2_4"][(0,1)] = (520*escala,40*escala)
        posiciones_x_tablero["STAGE2_4"][(1,0)] = (40*escala,440*escala)
        posiciones_x_tablero["STAGE2_4"][(1,1)] = (520*escala,440*escala)

        posiciones_x_tablero["STAGE3_4"] = dict()
        posiciones_x_tablero["STAGE3_4"]["escala"] = 1.307692307692308
        escala = posiciones_x_tablero["STAGE3_4"]["escala"]
        posiciones_x_tablero["STAGE3_4"][(0,0)] = (40*escala,40*escala)
        posiciones_x_tablero["STAGE3_4"][(0,1)] = (520*escala,40*escala)
        posiciones_x_tablero["STAGE3_4"][(1,0)] = (40*escala,440*escala)
        posiciones_x_tablero["STAGE3_4"][(1,1)] = (520*escala,440*escala)

        posiciones_x_tablero["STAGE4_4"] = dict()
        posiciones_x_tablero["STAGE4_4"]["escala"] = 1.307692307692308
        escala = posiciones_x_tablero["STAGE4_4"]["escala"]
        posiciones_x_tablero["STAGE4_4"][(0,0)] = (40*escala,40*escala)
        posiciones_x_tablero["STAGE4_4"][(0,1)] = (520*escala,40*escala)
        posiciones_x_tablero["STAGE4_4"][(1,0)] = (40*escala,440*escala)
        posiciones_x_tablero["STAGE4_4"][(1,1)] = (520*escala,440*escala)

        posiciones_x_tablero["STAGE5_4"] = dict()
        posiciones_x_tablero["STAGE5_4"]["escala"] = 1.307692307692308
        escala = posiciones_x_tablero["STAGE5_4"]["escala"]
        posiciones_x_tablero["STAGE5_4"][(0,0)] = (40*escala,40*escala)
        posiciones_x_tablero["STAGE5_4"][(0,1)] = (520*escala,40*escala)
        posiciones_x_tablero["STAGE5_4"][(1,0)] = (40*escala,440*escala)
        posiciones_x_tablero["STAGE5_4"][(1,1)] = (520*escala,440*escala)

    @staticmethod
    def setTablero(tab):
        Posiciones.tablero = tab

    @staticmethod
    def getPosicion(x, y):
        print Posiciones.tablero
        if posiciones_x_tablero.has_key(Posiciones.tablero):
            return posiciones_x_tablero[Posiciones.tablero][(x,y)]
        else:
            return (0,0)
        

if __name__ == "__main__":
    Posiciones.init()
    Posiciones.setTablero("Hola")
    print Posiciones.getPosicion(0,0)
    Posiciones.setTablero("STAGE1_4")
    print Posiciones.getPosicion(0,0)
