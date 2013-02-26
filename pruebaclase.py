import sys
import string
from ClientTesting import SocketClient
from chat import chat
from PySFML import sf

window = sf.RenderWindow(sf.VideoMode(640, 480), "Hola")
event = sf.Event()
window.SetFramerateLimit(60)
negro = sf.Color(0, 0, 0)
c  = chat(300,100)
s  = SocketClient()
s.__connect__("169.254.229.236",4345,"KIKE")
s.setChat(c)
c.SetCliente(s)

quit = False
while not quit:
    window.Clear(negro)
    
    while window.GetEvent(event):
        if event.Type == sf.Event.Closed:
            s.stop()
            quit = True
        if event.Type == sf.Event.TextEntered:
            c.Update(event)
    c.Draw(window)
    window.Display()
window.Close()
    
