import sys
import string
from PySFML import sf
#hola
class chat:
    flechaT = None
    flechaB = None
    mensaje = None
    mensajeTotal = None
    chatfondo = None
    chatText = None
    text = None
    textTotal = None
    temporalText = None
    inlineText = None
    enters = None
    contador = None
    cliente = None
    Alto = None
    Ancho = None
    CONSTANTE = 20
    CONSTANTE_ENTERS = 20
    DIRECTORIO = "bgs/"

    def __init__(self,posX,posY,W,H):
        self.text = ''
        self.textTotal = ''
        self.temporalText = ''
        self.inlineText = ''
        self.Alto = H
        self.Ancho = W
        self.enters = 1
        self.contador = 1
        self.CrearMensaje(posX,posY)
        self.FondoChat(posX,posY)
        
    def SetCliente(self, client):
        self.cliente = client
    
    def CrearFlecha(self,path):
        #flecha arriba
        top = sf.Image()
        top.LoadFromFile(path)
        self.flechaT = sf.Sprite(arriba)
        self.flechaT.SetCenter(0,0)

        #flecha abajo
        bot = sf.Image()
        bot.LoadFromFile(path)
        self.flechaB = sf.Sprite(arriba)
        self.flechaB.SetCenter(0,0)

    def FondoChat(self,posX,posY):
        #ImagenChat
        fondoChat = sf.Image()
        fondoChat.LoadFromFile(self.DIRECTORIO+"fondoChat.png")
        self.chatfondo = sf.Sprite(fondoChat)
        self.chatfondo.SetCenter(0, 0)
        self.chatfondo.Resize((240.0/1024.0)* self.Ancho,(380.0/680.0)*self.Alto)
        self.chatfondo.SetPosition(posX,posY)
        
    def CrearMensaje(self,posX,posY):
        negro = sf.Color(0, 0, 0)
        #muestra todo el texto
        self.mensajeTotal = sf.String('')
        self.mensajeTotal.SetColor(negro)
        self.mensajeTotal.SetCenter(0,0)
        self.mensajeTotal.SetPosition(posX+5,posY)
        self.mensajeTotal.SetSize(17)

        #muestra el texto temporal
        self.mensaje = sf.String('')
        self.mensaje.SetColor(negro)
        self.mensaje.SetCenter(0,0)
        self.mensaje.SetPosition(posX+5,(posY+(380.0/680.0)*self.Alto)-20)
        self.mensaje.SetSize(17)

    def Draw(self,window):
        window.Draw(self.chatfondo)
        window.Draw(self.mensaje)
        window.Draw(self.mensajeTotal)

    def Update(self,event):
        self.VerificarTexto(event)

    def Append(self,text):
        leng = len(text)
        cant = leng/self.CONSTANTE
        newText = ""
        for i in range(cant+1):
            newText = text[:self.CONSTANTE]
            self.temporalText += newText+"\n"
            self.textTotal += newText+"\n"
            self.enters += 1
            if(self.enters >= self.CONSTANTE_ENTERS):
                tem = self.enters - self.CONSTANTE_ENTERS
                if(tem == 0):
                    self.temporalText = self.temporalText[string.find(self.temporalText,'\n')+1:]   
                else:
                    for c in range(tem):
                        self.temporalText = self.temporalText[string.find(self.temporalText,'\n')+1:]
                        self.enters = self.CONSTANTE_ENTERS
            text = text[self.CONSTANTE:]
        self.mensajeTotal.SetText(self.temporalText)

    def SubirTexto(self):
        index = string.find(self.textTotal,self.temporalText)
        temp = self.textTotal[:index]
        if not (string.find(temp,"\n") == -1):
            temp = self.textTotal[:index-1]
            line = temp[string.rfind(temp,"\n")+1:] + "\n"   
            self.temporalText = line + self.temporalText
            temp = self.temporalText[:string.rfind(self.temporalText,"\n")]
            self.temporalText = temp[:string.rfind(temp,"\n")+1]
            self.mensajeTotal.SetText(self.temporalText)

    def BajarTexto(self):
        index = string.find(self.textTotal, self.temporalText) + len(self.temporalText)
        temp = self.textTotal[index:]
        if not (index == len(self.textTotal)):
            line = temp[:string.find(temp,"\n")]
            self.temporalText += line + "\n"
            self.temporalText = self.temporalText[string.find(self.temporalText,'\n')+1:]
            self.mensajeTotal.SetText(self.temporalText)
        
    def Send(self):
        self.Append(self.inlineText)
        self.cliente.sendMessage(self.inlineText)
        self.text = ''
        self.inlineText = ''
        self.contador = 0
        self.mensaje.SetText(self.text)
        
    def VerificarTexto(self,event):
        try:
            if event.Text.Unicode == 13:
                self.Send()
            else:
                if event.Text.Unicode == 8:
                    self.contador -= 1
                    self.inlineText = self.inlineText[:len(self.inlineText)-1]
                    self.text = self.text[:len(self.text)-1]
                    if(len(self.inlineText)>=self.CONSTANTE):
                        self.text = self.inlineText[len(self.inlineText)-self.CONSTANTE:len(self.inlineText)-self.CONSTANTE+1] + self.text
                else:
                    if(len(self.text)>=self.CONSTANTE):
                        self.text = self.text[1:]
                        self.contador -= 1
                    self.inlineText += unichr(event.Text.Unicode)
                    self.text += unichr(event.Text.Unicode)
                    self.contador+=1

        except Exception as inst:
            print str(inst)
        self.mensaje.SetText(self.text)


        
        
        
    
    
        
        
