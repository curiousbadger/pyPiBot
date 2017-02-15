'''
Created on Jul 19, 2016

@author: charper
'''
import socket
import threading
LISTEN_PORT = 6889
SERVER_IP = '10.0.0.9'
SERVER_ADDR = (SERVER_IP, LISTEN_PORT)
import tkinter as tk
MAX_ATTEMPTS = 5
s = None


def readData():
    return
    while True:
        data = s.recv(1024)
        if data:
            print('Received: ' + data.decode('utf-8'))


def sendData(data=None, updown='down'):
    global s
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            s.send(data.encode('utf-8'))
            return
        except Exception as e:
            attempts += 1
            print('Failed attempt:', attempts, e)
            if updown == 'down':
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(SERVER_ADDR)


class Application(tk.Frame):

    def __init__(self, master=None, rover=None):
        super().__init__(master, width=100, height=100)

        self.bind_all('<Key>', self.keyhandler)
        self.bind_all('<KeyRelease>', self.keyuphandler)

        #self.bind("<Button-1>", self.mouseclick)
        self.pack()
        self.create_widgets()
        self.rover = rover

    def mouseclick(self, event):
        pass

    def keyhandler(self, event):
        c = repr(event.char)
        sym = event.keysym
        #print('keyh', c, sym)

        if sym == 'Escape':
            sendData('stop')
            self.quit()

        sendData(sym)
        return sym

    def keyuphandler(self, event):
        c = str(repr(event.char))
        sym = event.keysym
        print('keyup', c, event.keysym, event)
        sendData('stop')

    def create_widgets(self):
        #self.hi_there = tk.Button(self)
        #self.hi_there["text"] = "Hello World\n(click me)"
        #self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                     command=root.destroy)
        # self.quit.pack(side="bottom")
        pass

    def say_hi(self):
        print("hi there, everyone!")


if __name__ == '__main__':

    root = tk.Tk()

    app = Application(master=root)
    # app.pack()
    # app.focus_set()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDR)

#     t1 = threading.Thread(target=readData)
#     t1.start()
#     t2 = threading.Thread(target=sendData)
#     t2.start()

    app.mainloop()

    exit(0)
