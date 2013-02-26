powerups = []
players = []
bloques = []
bombas = []
fuego = []
walls = []

cantidad = 1.0

class Entidades:

    @staticmethod
    def existeBloque(i, j):
        for ii in bloques:
            if (ii.i==i) and (ii.j==j) and ii.visible:
                return (True, ii.destruible)
        return (False, True)

    @staticmethod
    def cantPlayers():
        return cantidad

    @staticmethod
    def setCantidad(cant):
        cantidad = cant

    @staticmethod
    def agregarPlayer(player):
        players.append(player)

    @staticmethod
    def eliminarPlayer(player):
        Entidades.eliminar(player, players)

    @staticmethod
    def agregarBomba(bomba):
        bombas.append(bomba)

    @staticmethod
    def eliminarBomba(bomba):
        Entidades.eliminar(bomba, bombas)

    @staticmethod
    def agregarBloque(bloque):
        bloques.append(bloque)

    @staticmethod
    def agregarPowerUp(power):
        powerups.append(power)

    @staticmethod
    def eliminarBloque(bloque):
        Entidades.eliminar(bloque, bloques)

    @staticmethod
    def eliminarPowerUp(power):
        Entidades.eliminar(power, powerups)

    @staticmethod
    def agregarFuego(fire):
        fuego.append(fire)

    @staticmethod
    def eliminarFuego(fire):
        Entidades.eliminar(fire, fuego)

    @staticmethod
    def agregarMuro(muro):
        walls.append(muro)

    @staticmethod
    def eliminarMuro(muro):
        Entidades.eliminar(muro, walls)

    @staticmethod
    def eliminar(item, items):
        for i in range(len(items)):
            if items[i] == item:
                del items[i]
                break
    
    @staticmethod
    def colisionesBomba_Player():
        return Entidades.colisionan(bombas, players)

    @staticmethod
    def colisionesBloque_Player():
        return Entidades.colisionan(bloques, players)

    @staticmethod
    def colisionesBomba_Bloque():
        return Entidades.colisionan(bombas, bloques)

    @staticmethod
    def colisionesFuego_Bloques():
        return Entidades.colisionan(fuego, bloques)
        """colisiones = []
        for itemA in fuego:
            itemA.printCollisionArea()
            for itemB in bloques:
                if itemA.collide_with(itemB):
                    colisiones.append((itemA, itemB))
        return colisiones"""

    @staticmethod
    def colisionesFuego_PowerUps():
        return Entidades.colisionan(fuego, powerups)

    @staticmethod
    def colisionesPlayer_PowerUps(player):
        colisiones = []
        for i in powerups:
            if player.collide_with(i):
                colisiones.append((player,i))
        return colisiones
        

    @staticmethod
    def colisionesPlayer_Fuego(player):
        colisiones = []
        for i in fuego:
            if player.collide_with(i):
                colisiones.append((player,i))
        return colisiones

    @staticmethod
    def colisionesPlayer_Players(player):
        colisiones = []
        for i in players:
            if i != player:
                if player.collide_with(i):
                    colisiones.append((player,i))
        return colisiones

    @staticmethod
    def colisionesPlayer_Bloques(player):
        colisiones = []
        for i in bloques:
            if player.collide_with(i):
                colisiones.append((player,i))
        return colisiones

    @staticmethod
    def colisionesPlayer_Bombas(player):
        colisiones = []
        for i in bombas:
            if player.collide_with(i):
                colisiones.append((player,i))
        return colisiones

    @staticmethod
    def colisionesPlayer_Muros(player):
        colisiones = []
        for i in walls:
            if player.collide_with(i):
                colisiones.append((player,i))
        return colisiones

    @staticmethod
    def colisionan(grupoA, grupoB):
        colisiones = []
        for itemA in grupoA:
            for itemB in grupoB:
                if itemA.collide_with(itemB):
                    colisiones.append((itemA, itemB))
        return colisiones


if __name__ == "__main__":
    Entidades.agregarBomba(1)
    Entidades.agregarBomba(2)
    Entidades.eliminarBomba(2)
    Entidades.agregarBomba(4)
