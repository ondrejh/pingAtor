from tkinter import *
from tkinter.ttk import *
import subprocess

class pingAtorApp:
    def __init__(self,master):
        root.title("PingAtor v0.1a")
        self.mainfrm = Frame(root,padding='3 3 3 3')
        self.mainfrm.pack(side=TOP,fill=BOTH)

        self.ipVar = StringVar()
        self.ipVar.set('192.168.1.177')
        self.ipEntry = Entry(self.mainfrm,textvariable=self.ipVar)
        self.ipEntry.pack()
        self.pingButton = Button(self.mainfrm,text='Ping',command=self.pingClick)
        self.pingButton.pack()

    def pingClick(self):
        hostname = self.ipVar.get()
        if self.ping(hostname):
            print('UP')
        else:
            print('Hovno')

    def ping(self,hostname):
        if subprocess.call(['ping','-n','1','-w','300',hostname],shell=True) == 0:
            return(True)
        else:
            return(False)


if __name__ == '__main__':

    root = Tk()
    pingator_gui = pingAtorApp(root)
    root.mainloop()
