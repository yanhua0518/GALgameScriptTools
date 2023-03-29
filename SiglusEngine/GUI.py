# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys,os,time,struct,threading,subprocess,signal,windnd
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import SceneUnpacker,ScenePacker,GameexeUnpacker,GameexePacker
import ssDumper,ssPacker,dbsDecrypt,dbsEncrypt,pckUnpacker,pckPacker,omvCuter
import dbsBuilder

tool=["Unpack Scene","Pack Scene","Decrypt Gameexe","Encrypt Gameexe",
      "Dump ss","Pack ss","Dump dbs","Pack dbs","Create dbs",
      "Unpack pck","Pack pck","Cut OMV header"]
command=["SceneUnpacker","ScenePacker","GameexeUnpacker","GameexePacker",
         "ssDumper","ssPacker","dbsDecrypt","dbsEncrypt","dbsBuilder",
         "pckUnpacker","pckPacker","omvCuter"]

ENTRY_WIDTH=58
BUTTON_WIDTH=6
PAD=4
lastDir=os.getcwd()
typedKey=True
hasSkf=False
singleProcess=False
DECRYPT_KEY=[]
KEY_FILE="SiglusKey.txt"
KEY_LIST="KeyList.txt"
cmdOutput=sys.stdout

def setKey(keyStr):
    keyHex=keyStr.split(',')
    key=[]
    for byte in keyHex:
        key.append(int(byte,16))
    return key
    
def loadKey():
    try:
        file=open(KEY_FILE,'r')
        keyStr=file.readline()
        file.close()
        key=setKey(keyStr)
    except:
        return []
    else:
        return key

def saveKey(key):
    keyStr=SceneUnpacker.stringKey(key)
    file=open(KEY_FILE,'w')
    file.write(keyStr)
    file.close()
    if cmdText['state']=='disabled':
        cmdText['state']='normal'
        print("Last key saved!")
        cmdText['state']='disabled'
    else:
        print("Last key saved!")
    return True

def selectKey(value):
    global typedKey
    typedKey=False
    keyVar.set(keyList[keySelect.current()])

def unlock(value):
    global typedKey
    typedKey=True

def start():
    global lastSelect,option,DECRYPT_KEY
    optionList.selection_set(lastSelect)
    try:
        if lastSelect<4 and keyEntry['state']=='normal':
            if keySelect.current()!=0:
                tempKey=setKey(keyVar.get())
                if tempKey:
                    DECRYPT_KEY=tempKey
            elif lastSelect>1:
                1/0
        check=option.run()
    except ZeroDivisionError:
        messagebox.showerror("Error!","Can't find key from Gameexe!")
    except Exception as e:
        messagebox.showerror("Error!","Error!\nKey is wrong?\n"+str(e))

class findKey(threading.Thread):
    def __init__(self):
        global DECRYPT_KEY,typedKey
        super(findKey,self).__init__()
        self.Daemon=True
        self.signal=threading.Event()
        self.signal.set()
    def stop(self):
        self.signal.clear()
    def run(self):
        try:
            f=subprocess.Popen(os.getcwd()+"/skf.exe",
                               creationflags=subprocess.CREATE_NO_WINDOW,
                               stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL)
        except Exception as e:
            messagebox.showerror("Error!","Can't start skf.exe!\n"+str(e))
        cmdText['state']='normal'
        print("Please start the game and wait for a moment...\n"+
              "Click the button again to stop.")
        cmdText['state']='disabled'
        n=1
        while f.poll()==None:
            kfButton['text']="Finding"+'.'*n
            n=n%3+1
            time.sleep(1)
            if not self.signal.isSet():
                f.kill()
                kfButton['text']="Find Key"
                return
        try:
            output=f.stdout.readlines()
            keyStr=output[0].decode()
            newKey=setKey(keyStr)
        except:
            if output[0]:
                messagebox.showwarning("Warning",
                                   "Can't find key!\nPlease try again.")
            else:
                messagebox.showerror("Error!","Can't start skf.exe!")
            kfButton['text']="Find Key"
            return
        else:
            messagebox.showinfo("Notice","Key Found!")
            DECRYPT_KEY=newKey
            typedKey=True
            keyVar.set(keyStr)
            keySelect.current(1)
            keyList[1]=SceneUnpacker.stringKey(DECRYPT_KEY)
            kfButton['text']="Find Key"
            saveKey(DECRYPT_KEY)

def clickFindKey():
    global finding
    if kfButton['text']=="Find Key":
        finding=findKey()
        finding.start()
    else:
        finding.stop()

def select(event):
    global lastSelect,option,title
    selected=optionList.curselection()[0]
    if selected==lastSelect:
        return
    else:
        lastSelect=selected
    option=eval("set"+command[selected]+"()")
    title.pack_forget()
    title=Label(selectedFrame,text=tool[selected],font=('Fixdsys 14 bold'))
    title.pack()
    if selected>2:
        keyEntry['state']='disabled'
        keySelect['state']='disabled'
        if hasSkf:
            if selected>3:
                kfButton['state']='disabled'
            else:
                kfButton['state']='normal'
    else:
        keyEntry['state']='normal'
        keySelect['state']='readonly'
        if hasSkf:
            kfButton['state']='normal'
        

def clear():
    global inputFrame
    inputFrame.pack_forget()
    inputFrame=Frame(rightFrame)
    inputFrame.pack(side='top')

def selectFile(v):
    global lastDir
    temp=askopenfilename(initialdir=lastDir)
    if temp:
        v.set(temp)
        lastDir=temp[:temp.rfind('/')]
def setFile(v):
    global lastDir
    temp=asksaveasfilename(initialdir=lastDir,initialfile=v.get())
    if temp:
        v.set(temp)
        lastDir=temp[:temp.rfind('/')]
def selectFolder(v):
    global lastDir
    temp=askdirectory(initialdir=lastDir)
    if temp:
        v.set(temp)
        lastDir=temp
        
def dropValue1(f):
    value1.set(f[0].decode("GBK"))
def dropValue2(f):
    value2.set(f[0].decode("GBK"))
def dropValue3(f):
    value3.set(f[0].decode("GBK"))

def getValue(v):
    return v.get().replace('"','').replace("'","")
    

def running(cmd,key):
    global typedKey,DECRYPT_KEY
    if key==None:
        code=cmd[0]+".main(cmd)"
    else:
        code=cmd[0]+".main(cmd,key)"
    cmdText['state']='normal'
    print('Running '+str(cmd)+' ...')
    if singleProcess:
        startButton['state']='disabled'
    try:
        check=eval(code)
    except Exception as e:
        messagebox.showerror("Error!","Error!\n"+str(e))
    else:
        if check:
            if check==True or isinstance(check,list):
                messagebox.showinfo("Notice","Finished!")
                if lastSelect==0 and isinstance(check,list):
                    DECRYPT_KEY=check
                    typedKey=True
                    keyList[1]=SceneUnpacker.stringKey(DECRYPT_KEY)
                    keySelect.current(1)
                    keyVar.set(keyList[1])
                if lastSelect<4 and typedKey:
                    saveKey(DECRYPT_KEY)
            elif isinstance(check,int):
                messagebox.showwarning("Warning","Finish,\nbut error occurred!")
            else:
                messagebox.showerror("Error!","Error!\n"+str(check))
        else:
            messagebox.showwarning("Warning","Input error!")
    cmdText['state']='disabled'
    startButton['state']='normal'


def runningExe(cmd):
    cmdText['state']='normal'
    if singleProcess:
        startButton['state']='disabled'
    print('Running "'+cmd[0:cmd.find('.exe')+4]+'"...')
    try:
        exe=subprocess.Popen(os.getcwd()+"/"+cmd,bufsize=1,
                             creationflags=subprocess.CREATE_NO_WINDOW,
                             stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,universal_newlines=True)
        for line in iter(exe.stdout.readline,''):
            print(line.replace('\n',''))
    except Exception as e:
        messagebox.showerror("Error!","Can't create process!\n"+str(e))
    else:
        if exe.stderr.readlines() or line==[]:
            messagebox.showerror("Error!","Failed!")
        else:
            if line[:5]=="error":
                messagebox.showwarning("Warning",line)
            else:
                messagebox.showinfo("Notice",line)
    cmdText['state']='disabled'
    startButton['state']='normal'

class setSceneUnpacker:
    def dropValue1(self,f):
        file=f[0].decode("GBK")
        value1.set(file)
        if (value2.get()=="Scene" or value2.get()=="") and file.find(".pck")>0:
            value2.set(file.replace('.pck',''))
    def __init__(self):
        
        def checkFind():
            if valueB.get():
                name2['state']='disabled'
                entry2['state']='disabled'
                button2['state']='disabled'
                keySelect['state']='disabled'
                keyEntry['state']='disabled'
            else:
                name2['state']='normal'
                entry2['state']='normal'
                button2['state']='normal'
                keySelect['state']='readonly'
                keyEntry['state']='normal'
                
        clear()
        name1=Label(inputFrame,text="Scene file:")
        name2=Label(inputFrame,text="Output folder:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("Scene.pck")
        value2.set("Scene")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        valueB.set(False)
        buttonB=Checkbutton(inputFrame,text="Find key only",command=checkFind,variable=valueB)
        buttonB.grid(row=4,padx=2,pady=4,sticky='e')
        windnd.hook_dropfiles(entry1,self.dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
    def run(self):
        cmd=["SceneUnpacker",getValue(value1)]
        if valueB.get():
            cmd.append("-f")
        else:
            cmd.append(getValue(value2))
        if keySelect.current()==0 or valueB.get():
            tempKey=[]
        else:
            tempKey=DECRYPT_KEY
        runPy=threading.Thread(target=running,args=(cmd,tempKey))
        runPy.Daemon=True
        runPy.start()
        return 

class setScenePacker:
    def dropValue1(self,f):
        file=f[0].decode("GBK")
        value1.set(file)
        if (value3.get()=="Scene.pck2" or value3.get()=="") and file.find(".pck")>0:
            value3.set(file+"2")
    def __init__(self):
        clear()
        name1=Label(inputFrame,text="Scene file:")
        name2=Label(inputFrame,text="Scene folder:")
        name3=Label(inputFrame,text="Output file:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        name3.grid(row=4,padx=2,sticky='w')
        value1.set("Scene.pck")
        value2.set("Scene")
        value3.set("Scene.pck2")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry3=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value3)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        entry3.grid(row=5,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value2))
        button3=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:setFile(value3))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        button3.grid(row=5,column=1,padx=2)
        windnd.hook_dropfiles(entry1,self.dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
        windnd.hook_dropfiles(entry3,dropValue3)
        valueC.set('17')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
    def run(self):
        cmd=["ScenePacker",getValue(value1),getValue(value2),getValue(value3)]
        try:
            comp=int(valueC.get())
        except:
            comp=0
        else:
            if comp<2:
                comp=0
            elif comp>17:
                comp=17
        if comp!=0:
            cmd.append("-c")
            cmd.append(str(comp))
        else:
            cmd.append("-f")
        if keySelect.current()==0:
            tempKey=[]
        else:
            tempKey=DECRYPT_KEY
        runPy=threading.Thread(target=running,args=(cmd,tempKey))
        runPy.Daemon=True
        runPy.start()
        return 
        
class setGameexeUnpacker:
    def dropValue1(self,f):
        file=f[0].decode("GBK")
        value1.set(file)
        if (value2.get()=="Gameexe.ini" or value2.get()=="") and file.lower().find("gameexe.dat")>0:
            value2.set(file.lower().replace("gameexe.dat","Gameexe.ini"))
    def __init__(self):
        clear()
        name1=Label(inputFrame,text="Gameexe:")
        name2=Label(inputFrame,text="Output file:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("Gameexe.dat")
        value2.set("Gameexe.ini")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:setFile(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,self.dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
    def run(self):
        cmd=["GameexeUnpacker",getValue(value1),getValue(value2)]
        runPy=threading.Thread(target=running,args=(cmd,DECRYPT_KEY))
        runPy.Daemon=True
        runPy.start()
        return 

class setGameexePacker:
    def dropValue1(self,f):
        file=f[0].decode("GBK")
        value1.set(file)
        if (value2.get()=="Gameexe.dat2" or value2.get()=="") and (file.lower().find("gameexe.ini")>0 or file.lower().find("gameexe.txt")>0):
            value2.set(file.lower().replace("gameexe.ini","Gameexe.dat2").replace("gameexe.txt","Gameexe.dat2"))
    def __init__(self):

        def checkDB():
            if valueB.get():
                keySelect['state']='readonly'
                keyEntry['state']='normal'
            else:
                keySelect['state']='disabled'
                keyEntry['state']='disabled'
                
        clear()
        name1=Label(inputFrame,text="Gameexe:")
        name2=Label(inputFrame,text="Output file:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("Gameexe.ini")
        value2.set("Gameexe.dat2")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:setFile(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,self.dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
        valueC.set('17')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
        valueB.set(False)
        buttonB=Checkbutton(inputFrame,text="Double Encryption(Useless)",command=checkDB,variable=valueB)
        buttonB.grid(row=8,padx=2,pady=4,sticky='e')
    def run(self):
        cmd=["GameexePacker",getValue(value1),getValue(value2),getValue(value3)]
        if valueB.get():
            cmd.append("-p")
        try:
            comp=int(valueC.get())
        except:
            comp=0
        else:
            if comp<2:
                comp=0
            elif comp>17:
                comp=17
        if comp!=0:
            cmd.append("-c")
            cmd.append(str(comp))
        else:
            cmd.append("-f")
        runPy=threading.Thread(target=running,args=(cmd,DECRYPT_KEY))
        runPy.Daemon=True
        runPy.start()
        return 

class setssDumper:
    def dropValue1(self,f):
        file=f[0].decode("GBK")
        value1.set(file)
        if (value2.get()=="Text" or value2.get()=="") and file[file.rfind("\\"):].find(".")<0:
            if valueB2.get():
                value2.set(file+".xlsx")
            else:
                value2.set(file+"_text")
    def __init__(self):
        
        def checkEnable():
            if valueB1.get():
                buttonB2['state']='normal'
            else:
                valueB2.set(False)
                checkName()
                buttonB2['state']='disabled'
        def checkName():
            if valueB2.get():
                name2['text']='Output file:'
                buttonB3['state']='normal'
            else:
                name2['text']="Output folder:"
                valueB3.set(False)
                buttonB3['state']='disabled'
        def outSelect():
            if valueB2.get():
                setFile(value2)
            else:
                selectFolder(value2)
                
        clear()
        name1=Label(inputFrame,text="Ss folder:")
        name2=Label(inputFrame,text="Output folder:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("Scene")
        value2.set("Text")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=outSelect)
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,self.dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
        valueB.set(True)
        valueB1.set(False)
        valueB2.set(False)
        valueB3.set(False)
        valueB4.set(False)
        valueI.set(1)
        buttonB=Frame(inputFrame)
        buttonB.grid(row=6,column=0,padx=2,pady=4,sticky='w')
        buttonB0=Checkbutton(buttonB,text="Copy text",variable=valueB)
        buttonB1=Checkbutton(buttonB,text="Export as xlsx",command=checkEnable,variable=valueB1)
        buttonB2=Checkbutton(buttonB,text="Use single xlsx",state='disabled',command=checkName,variable=valueB2)
        buttonB3=Checkbutton(buttonB,text="Count words",state='disabled',variable=valueB3)
        buttonR1=Radiobutton(buttonB,text="No filter",variable=valueI,value=0)
        buttonR2=Radiobutton(buttonB,text="Smart filter",variable=valueI,value=1)
        buttonR3=Radiobutton(buttonB,text="Filter all",variable=valueI,value=2)
        buttonB4=Checkbutton(buttonB,text="Special mode",variable=valueB4)
        buttonB0.grid(row=0,column=0,sticky='w')
        buttonB1.grid(row=0,column=1,sticky='w')
        buttonB2.grid(row=0,column=2,sticky='w')
        buttonB3.grid(row=0,column=3,sticky='w')
        buttonR1.grid(row=1,column=0,sticky='w')
        buttonR2.grid(row=1,column=1,sticky='w')
        buttonR3.grid(row=1,column=2,sticky='w')
        buttonB4.grid(row=1,column=3,sticky='e')
    def run(self):
        cmd=["ssDumper",getValue(value1),getValue(value2)]
        if valueI.get()==0:
            cmd.append("-a")
        elif valueI.get()==2:
            cmd.append("-w")
        if valueB.get():
            cmd.append("-d")
        if valueB1.get():
            cmd.append("-x")
            if valueB2.get():
                cmd.append("-s")
                if valueB3.get():
                    cmd.append("-c")
        if valueB4.get():
            cmd.append("-o")
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 

class setssPacker:
    def dropValue1(self,f):
        file=f[0].decode("GBK")
        value1.set(file)
        if (value3.get()=="Output" or value3.get()=="") and file[file.rfind("\\"):].find(".")<0:
            value3.set(file+"_packed")
    def __init__(self):
        def checkEnable():
            if valueB.get():
                buttonB1['state']='normal'
            else:
                valueB1.set(False)
                buttonB1['state']='disabled'
        clear()
        name1=Label(inputFrame,text="Ss folder:")
        name2=Label(inputFrame,text="Text folder:")
        name3=Label(inputFrame,text="Output folder:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        name3.grid(row=4,padx=2,sticky='w')
        value1.set("Scene")
        value2.set("Text")
        value3.set("Output")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry3=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value3)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        entry3.grid(row=5,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value2))
        button3=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value3))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        button3.grid(row=5,column=1,padx=2)
        windnd.hook_dropfiles(entry1,self.dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
        windnd.hook_dropfiles(entry3,dropValue3)
        valueB.set(True)
        valueB1.set(False)
        valueB2.set(False)
        valueB4.set(False)
        buttonB=Frame(inputFrame)
        buttonB.grid(row=8,padx=2,pady=4,sticky='w')
        buttonB0=Checkbutton(buttonB,text="Have Excel text",command=checkEnable,variable=valueB)
        buttonB1=Checkbutton(buttonB,text="Bilingual display (For mobile only)",variable=valueB1)
        buttonB2=Checkbutton(buttonB,text="Change quotation marks",variable=valueB2)
        buttonB3=Checkbutton(buttonB,text="Special mode",variable=valueB4)
        buttonB0.grid(row=0,column=0,sticky='w')
        buttonB1.grid(row=0,column=1,sticky='w')
        buttonB2.grid(row=1,column=0,sticky='w')
        buttonB3.grid(row=1,column=1,sticky='e')
    def run(self):
        cmd=["ssPacker",getValue(value1),getValue(value2),getValue(value3)]
        if valueB.get():
            cmd.append("-x")
            if valueB1.get():
                cmd.append("-b")
        if valueB2.get():
            cmd.append("-q")
        if valueB4.get():
            cmd.append("-o")
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 

class setdbsDecrypt:
    def __init__(self):
        def checkEnable():
            if valueB2.get():
                valueB1.set(True)
                buttonB1['state']='disabled'
            else:
                buttonB1['state']='normal'
        
        clear()
        name1=Label(inputFrame,text="Dbs file:")
        name1.grid(row=0,padx=2,sticky='w')
        value1.set("*.dbs")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry1.grid(row=1,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button1.grid(row=1,column=1,padx=2)
        windnd.hook_dropfiles(entry1,dropValue1)
        valueB1.set(False)
        valueB2.set(False)
        buttonB=Frame(inputFrame)
        buttonB.grid(row=6,column=0,padx=2,pady=4,sticky='e')
        buttonB1=Checkbutton(buttonB,text="Export all data",variable=valueB1)
        buttonB2=Checkbutton(buttonB,text="Export as xlsx",command=checkEnable,variable=valueB2)
        buttonB1.grid(row=0,column=0,sticky='w')
        buttonB2.grid(row=0,column=1,sticky='e')
    def run(self):
        cmd=["dbsDecrypt",getValue(value1)]
        if valueB2.get():
            cmd.append("-x")
        elif valueB1.get():
            cmd.append("-a")
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 

class setdbsEncrypt:
    def __init__(self):
        clear()
        name1=Label(inputFrame,text="Dbs.out file:")
        name2=Label(inputFrame,text="Dbs.txt file:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("*.dbs.out")
        value2.set("")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
        valueC.set('17')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
    def run(self):
        cmd=["dbsEncrypt",getValue(value1),getValue(value2)]
        try:
            comp=int(valueC.get())
        except:
            comp=0
        else:
            if comp<2:
                comp=0
            elif comp>17:
                comp=17
        if comp!=0:
            cmd.append("-c")
            cmd.append(str(comp))
        else:
            cmd.append("-f")
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 

class setdbsBuilder:
    def __init__(self):
        def checkANSI():
            if valueB.get():
                buttonB3['state']='disabled'
            else:
                buttonB3['state']='normal'
        clear()
        name1=Label(inputFrame,text="Xlsx folder:")
        name2=Label(inputFrame,text="Dbs folder:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("dbsData")
        value2.set("")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
        valueB.set(True)
        value3.set("GBK")
        buttonB=Frame(inputFrame)
        buttonB.grid(row=6,column=0,padx=2,pady=4,sticky='e')
        buttonB1=Radiobutton(buttonB,text="Unicode",command=checkANSI,variable=valueB,value=True)
        buttonB2=Radiobutton(buttonB,text="ANSI",command=checkANSI,variable=valueB,value=False)
        buttonB3=Combobox(buttonB,state='disabled',width=8,textvariable=value3,value=["GBK","Shift-JIS","Big5","Korean"])
        buttonB3.current(0)
        buttonB1.grid(row=8,column=1,sticky='w')
        buttonB2.grid(row=8,column=2,sticky='w')
        buttonB3.grid(row=8,column=3,padx=8,sticky='e')
        valueC.set('17')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
    def run(self):
        cmd=["dbsBuilder",getValue(value1),getValue(value2)]
        if not valueB.get():
            cmd.append("-e")
            if getValue(value3):
                cmd.append(getValue(value3))
        try:
            comp=int(valueC.get())
        except:
            comp=0
        else:
            if comp<2:
                comp=0
            elif comp>17:
                comp=17
        if comp!=0:
            cmd.append("-c")
            cmd.append(str(comp))
        else:
            cmd.append("-f")
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 

class setpckUnpacker:
    def __init__(self):
        clear()
        name1=Label(inputFrame,text="Pck file:")
        name2=Label(inputFrame,text="Output folder:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("*.pck")
        value2.set("")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
    def run(self):
        cmd=["pckUnpacker",getValue(value1),getValue(value2)]
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 
        
class setpckPacker:
    def __init__(self):
        clear()
        name1=Label(inputFrame,text="Folder to pack:")
        name2=Label(inputFrame,text="Output file:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("")
        value2.set("")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:setFile(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
    def run(self):
        cmd=["pckPacker",getValue(value1),getValue(value2)]
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 

class setomvCuter:
    def __init__(self):
        clear()
        name1=Label(inputFrame,text="OMV file:")
        name1.grid(row=0,padx=2,sticky='w')
        value1.set("*.omv")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry1.grid(row=1,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button1.grid(row=1,column=1,padx=2)
        windnd.hook_dropfiles(entry1,dropValue1)
    def run(self):
        cmd=["omvCuter",getValue(value1)]
        runPy=threading.Thread(target=running,args=(cmd,None))
        runPy.Daemon=True
        runPy.start()
        return 

class setsiglusOmv:
    def dropValue1(self,f):
        file=f[0].decode("GBK")
        value1.set(file)
        if file.lower()[file.rfind("\\"):].find(".ogv")>0:
            value2.set(file.lower().replace('.ogv','.omv'))
    def __init__(self):
        clear()
        name1=Label(inputFrame,text="ogv file(Must be YUV444p):")
        name2=Label(inputFrame,text="OMV file:")
        name1.grid(row=0,padx=2,sticky='w')
        name2.grid(row=2,padx=2,sticky='w')
        value1.set("*.ogv")
        value2.set("")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry2=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value2)
        entry1.grid(row=1,column=0,padx=2)
        entry2.grid(row=3,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        windnd.hook_dropfiles(entry1,self.dropValue1)
        windnd.hook_dropfiles(entry2,dropValue2)
    def run(self):
        cmd='siglusomv.exe "'+getValue(value1)+'" "'
        if not getValue(value2):
            cmd+=getValue(value1).replace('.ogv','.omv')+'"'
        else:
            cmd+=getValue(value2)+'"'
        runExe=threading.Thread(target=runningExe,args=(cmd.replace("*",""),))
        runExe.Daemon=True
        runExe.start()
        return 

class StdoutRedirector(object):

    def __init__(self, text_area):
        self.text_area = text_area

    def write(self, str):
        self.text_area.insert(END, str)
        self.text_area.see(END)

root=Tk()
root.title("Siglus Tools")
root.geometry("640x480")
#root.resizable(False,False)
lastSelect=0

try:
    f=subprocess.Popen(os.getcwd()+"/siglusomv.exe")
    f.kill()
except:pass
else:
    tool.append("Pack OMV")
    command.append("siglusOmv")

cmdFrame=Frame(root)
cmdFrame.pack(side='bottom',fill='both',padx=PAD,pady=PAD)
cmdScroll=Scrollbar(cmdFrame,bd=2)
cmdScroll.pack(side='right',fill='y',padx=PAD,pady=PAD)
cmdText=Text(cmdFrame,wrap='word',state='disabled',
             yscrollcommand=cmdScroll.set,
             width=86,height=22-len(command),bd=2)
sys.stdout=StdoutRedirector(cmdText)
cmdText.pack(side='left',fill='x')
cmdScroll.config(command=cmdText.yview)

keyFrame=Frame(root)
keyFrame.pack(side='bottom',fill='x')
mainFrame=Frame(root)
mainFrame.pack(side='top',fill='x')
optionFrame=Frame(mainFrame,padx=PAD,pady=PAD)
optionFrame.pack(side='left',fill='both')
rightFrame=Frame(mainFrame,padx=PAD,pady=PAD)
rightFrame.pack(side='right',fill='both')
selectedFrame=Frame(rightFrame)
selectedFrame.pack(side='top')
inputFrame=Frame(rightFrame)
inputFrame.pack(side='top')

value1=StringVar()
value2=StringVar()
value3=StringVar()
valueB=BooleanVar()
valueB1=BooleanVar()
valueB2=BooleanVar()
valueB3=BooleanVar()
valueB4=BooleanVar()
valueI=IntVar()
valueC=StringVar()

keyVar=StringVar()
tempKey=loadKey()

keyInfo=Frame(keyFrame)
keyInfo.pack(side='top',anchor='w',fill='x')
startButton=Button(keyFrame,text="Start",command=start,width=7)
startButton.pack(side='right',padx=PAD,pady=PAD,anchor='e')

if tempKey:
    DECRYPT_KEY=tempKey
    #keyVar.set(SceneUnpacker.stringKey(DECRYPT_KEY))
keyEntry=Entry(keyFrame,width=80,textvariable=keyVar)
keyEntry.bind("<Control-Key-v>",unlock)
keyEntry.pack(side='left',padx=PAD,pady=PAD,anchor='w')

try:
    f=subprocess.Popen(os.getcwd()+"/skf.exe")
    f.kill()
except:
    hasSkf=False
else:
    hasSkf=True
    kfButton=Button(keyInfo,text="Find Key",command=clickFindKey,width=8)
    kfButton.pack(side='right',padx=PAD,pady=PAD,anchor='e')

keyLabel=Label(keyInfo,text='Decryption Key(Hex separate by ","):')
keyLabel.pack(side='left',anchor='w')

try:
    listFile=open(KEY_LIST,'r',1,'UTF-8')
except:
    keyList=["",SceneUnpacker.stringKey(DECRYPT_KEY)]
    keyName=["Try to find key when working on Scene","Last use"]
else:
    keyList=["",SceneUnpacker.stringKey(DECRYPT_KEY)]
    keyName=["Try to find key when working on Scene","Last use"]
    for line in listFile.readlines():
        if line[-2:]=='：\n':
            keyName.append(line[:-2])
        elif line!='\n':
            keyList.append(line[:-1])
    listFile.close()
if hasSkf:
    listWidth=46
else:
    listWidth=56
keySelect=Combobox(keyInfo,width=listWidth,state='readonly',value=keyName)
keySelect.bind("<<ComboboxSelected>>",selectKey)
keySelect.current(0)
keySelect.pack(side='left',anchor='e')

optionLabel=Label(optionFrame,text="Select option:")
optionLabel.pack(side='top',anchor='w')
optionVar=StringVar()
optionVar.set(tool)
optionList=Listbox(optionFrame,listvariable=optionVar,height=len(command))
optionList.selection_set(0)
title=Label(selectedFrame,text=tool[0],font=('Fixdsys 14 bold'))
title.pack()
option=setSceneUnpacker()
optionList.bind('<ButtonRelease-1>',select)
optionList.pack(side='top',fill='y')

root.mainloop()
sys.stdout=cmdOutput
