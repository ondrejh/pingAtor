from tkinter import *
from tkinter.ttk import *
from tkinter import Entry,Button
import subprocess

addIcon = None
delIcon = None
pingIcon = None

def ping(hostname,timeout=300):
    if subprocess.call(['ping','-n','1','-w','{}'.format(timeout),hostname],shell=True) == 0:
        return True
    return False


class adrFrame:
    def __init__(self,master,name,ip):
        self.frame = Frame(master,padding='3 3 3 3')
        #self.frame.pack(side=TOP,fill=X)
        self.button = Button(self.frame,text='Ping',command=self.ping,image=pingIcon,relief=FLAT)
        self.button.pack(side=LEFT)
        self.ipVar = StringVar()
        self.ipVar.set(ip)
        self.ipEntry = Entry(self.frame,textvariable=self.ipVar,font=("Courier", 18),justify=CENTER,width=17)
        self.ipEntry.pack(side=LEFT)
        self.dflCol = self.ipEntry.cget('background')
        self.nameLabel = Label(self.frame,padding='5 0 0 0',font=("Times", 14))
        self.nameLabel.pack(side=LEFT)
        self.delete = Button(self.frame,text='Delete',command=self.deactivate,image=delIcon,relief=FLAT)
        self.delete.pack(side=RIGHT)
        self.active = False
        self.activate(name)
        
    def activate(self,name):
        self.frame.pack(side=TOP,fill=X)
        self.nameLabel['text']=name
        self.active = True
            
    def deactivate(self):
        self.ipEntry['background'] = self.dflCol
        self.frame.pack_forget()
        self.active = False
        
    def ping(self):
        self.ipEntry['background'] = self.dflCol
        root.update_idletasks()
        hostip = self.ipVar.get()
        if ping(hostip):
            self.ipEntry['background'] = 'lightgreen'
            #print('{} UP'.format(hostip))
        else:
            self.ipEntry['background'] = 'red'
            #print('{} Hovno'.format(hostip))
        root.update_idletasks()
        

class pingAtorApp:
    def __init__(self,master):
        root.protocol('WM_DELETE_WINDOW',self.onexit)
        root.title("PingAtor v0.1a")

        self.mainfrm = Frame(root,padding='3 3 3 3')
        self.mainfrm.pack(side=TOP,fill=BOTH)

        self.addfrm = LabelFrame(self.mainfrm,text='Add IP',padding='3 3 3 3')
        self.addfrm.pack(side=TOP,fill=X)
        self.labName = Label(self.addfrm,text='Name:',justify=RIGHT)
        self.labName.pack(side=LEFT,padx=10)
        self.nameVar = StringVar()
        self.nameVar.set('Address 1')
        self.nameEntry = Entry(self.addfrm,textvariable=self.nameVar)
        self.nameEntry.pack(side=LEFT)
        self.labIp = Label(self.addfrm,text='IP:',justify=RIGHT)
        self.labIp.pack(side=LEFT,padx=10)
        self.ipVar = StringVar()
        self.ipVar.set('192.168.1.1')
        self.ipEntry = Entry(self.addfrm,textvariable=self.ipVar)
        self.ipEntry.pack(side=LEFT)
        self.addButton = Button(self.addfrm,text='Add',command=self.addAdrClick,image=addIcon,relief=FLAT)
        self.addButton.pack(side=RIGHT)

        self.addresses = LabelFrame(self.mainfrm,text='Ping')
        self.addresses.pack(side=TOP,fill=X)
        self.adr = []
        self.cnt = 0

        self.loadSetup()

        root.after(100,self.testClick)

    def testClick(self):
        if len(self.adr)==0:
            self.cnt=0
        else:
            if self.cnt>=len(self.adr):
                self.cnt=0
            if self.adr[self.cnt].active:
                self.adr[self.cnt].ping()
            self.cnt += 1

        root.after(1000 if self.cnt == len(self.adr) else 100,self.testClick)

    def saveSetup(self):
        cfgFile = open('config.ini','w')
        cfgFile.write('[add]\n')
        cfgFile.write('{} = {}\n'.format(self.nameVar.get(),self.ipVar.get()))
        cfgFile.write('[ping]\n')
        for a in self.adr:
            if a.active:
                cfgFile.write('{} = {}\n'.format(a.nameLabel['text'],a.ipVar.get()))
        cfgFile.close()

    def loadSetup(self):
        group = None
        name = 'Address 1'
        ip = '192.168.1.1'
        try:
            for line in open('config.ini'):
                line = line.strip()
                if (line[0]=='[') and (line[-1]==']'):
                    group = line[1:-1]
                else:
                    if group=='add':
                        line=line.split('=')
                        name = line[0].strip()
                        ip = line[1].strip()
                    elif group=='ping':
                        line=line.split('=')
                        self.nameVar.set(line[0].strip())
                        self.ipVar.set(line[1].strip())
                        self.addAdrClick()
        except:
            pass
        self.ipVar.set(ip)
        self.nameVar.set(name)
    
    def addAdrClick(self):
        hostname = self.nameVar.get()
        hostip = self.ipVar.get()
        activated = False
        for a in self.adr:
            if a.ipVar.get()==hostip:
                a.activate(hostname)
                activated = True
                break

        if not activated:
            self.adr.append(adrFrame(self.addresses,hostname,hostip))

        try:
            hostip=hostip.split('.')
            hostip[-1]=str(int(hostip[-1])+1)
            newhostip = ''
            for i in hostip:
                if newhostip=='':
                    newhostip=str(i)
                else:
                    newhostip = '{}.{}'.format(newhostip,i)
            self.ipVar.set(newhostip)
        except:
            pass

        try:
            hostname=hostname.split(' ')
            hostname[-1]=str(int(hostname[-1])+1)
            newhostname = ''
            for i in hostname:
                if newhostname == '':
                    newhostname = str(i)
                else:
                    newhostname = '{} {}'.format(newhostname,i)
            self.nameVar.set(newhostname)
        except:
            pass

    def onexit(self):
        self.saveSetup()
        root.destroy()


if __name__ == '__main__':

    root = Tk()

    addIcon = PhotoImage(file='add.png')
    delIcon = PhotoImage(file='delete.png')
    pingIcon = PhotoImage(file='ping.png')

    pingator_gui = pingAtorApp(root)
    root.mainloop()
