class Tableros:
    def __init__(self):
        self.index = -1
        self.tableros = []
        tableros = self.tableros        
        tableros.append("STAGE1_4")
        tableros.append("STAGE2_4")
        tableros.append("STAGE3_4")
        tableros.append("STAGE4_4")
        tableros.append("STAGE5_4")

    def GetSiguiente(self):
        self.index += 1

    def GetSiguiente(self):
        self.index += 1
        if self.index == len(self.tableros):
            self.index = -1

        return self.tableros[self.index]

    def GetAnterior(self):
        if self.index == 0:
            self.index = len(self.tableros)
        self.index -= 1
        return self.tableros[self.index]

    def GetFirst(self):
        self.index = 0
        return self.tableros[self.index]

