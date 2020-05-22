# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import time
import threading
import subprocess
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import struct
import SceneUnpacker,ScenePacker,GameexeUnpacker,GameexePacker
import ssDumper,ssPacker,dbsDecrypt,dbsEncrypt,pckUnpacker,pckPacker


tool=["Unpack Scene","Pack Scene","Decrypt Gameexe","Encrypt Gameexe",
        "Dump ss","Pack ss","Dump dbs","Pack dbs","Unpack pck","Pack pck"]
command=["SceneUnpacker.py","ScenePacker.py","GameexeUnpacker.py",
         "GameexePacker.py","ssDumper.py","ssPacker.py",
         "dbsDecrypt.py","dbsEncrypt.py","pckUnpacker.py","pckPacker.py"]

ENTRY_WIDTH=58
BUTTON_WIDTH=6
PAD=4
lastDir=os.getcwd()
typedKey=True
hasList=False
hasSkf=False
DECRYPT_KEY=[0x2E, 0x4B, 0xDD, 0x2A, 0x7B, 0xB0, 0x0A, 0xBA,
             0xF8, 0x1A, 0xF9, 0x61, 0xB0, 0x18, 0x98, 0x5C]
KEY_FILE="SiglusKey.txt"
KEY_LIST="KeyList.txt"


def stringKey(key):
    keyHex=[]
    for byte in key:
        keyHex.append(hex(byte))
    keyStr=str(keyHex).replace("[","").replace("]","").replace("'","")
    return keyStr

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

def saveKey():
    keyStr=stringKey(DECRYPT_KEY)
    file=open(KEY_FILE,'w')
    file.write(keyStr)
    file.close()
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
        if lastSelect<4:
            tempKey=setKey(keyVar.get())
            if tempKey:
                DECRYPT_KEY=tempKey
        check=option.run()
    except:
        messagebox.showerror("Error!","Error!\nKey is wrong?")
    else:
        if check:
            messagebox.showinfo("Notice","Finished!")
            if lastSelect<4 and typedKey:
                saveKey()
        else:
            messagebox.showwarning("Warning","Input error!")

class findKey(threading.Thread):
    def __init__(self):
        global DECRYPT_KEY,typedKey,kfButton
        super(findKey,self).__init__()
        self.setDaemon(True)
        self.signal=threading.Event()
        self.signal.set()
    def stop(self):
        self.signal.clear()
    def run(self):
        f=subprocess.Popen(os.getcwd()+"\\skf.exe",shell=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
            
        kfButton['text']="Finding..."
        while f.poll()==None:
            time.sleep(1)
            if not self.signal.isSet():
                f.kill()
                kfButton['text']="Find Key"
                return
        try:
            output=f.stdout.readlines()
            #print(output)
            keyIndex=output.index(b'Keys found:\n')+1
            keyStr=output[keyIndex].decode()
            newKey=setKey(keyStr)
        except:
            if output[0][:6]==b'Please':
                messagebox.showwarning("Warning",
                                   "Can't find key!\nPlease try again.")
            else:
                messagebox.showerror("Error!","Error!\nCan't start skf.exe")
            kfButton['text']="Find Key"
            return
        else:
            messagebox.showinfo("Notice","Key Found!")
            DECRYPT_KEY=newKey
            typedKey=True
            keyVar.set(keyStr)
            if hasList:
                keySelect.current(0)
                keyList[0]=stringKey(DECRYPT_KEY)
            kfButton['text']="Find Key"

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
    if selected==0:
        option=UnpackScene()
    elif selected==1:
        option=PackScene()
    elif selected==2:
        option=UnpackGameexe()
    elif selected==3:
        option=PackGameexe()
    elif selected==4:
        option=DumpSs()
    elif selected==5:
        option=PackSs()
    elif selected==6:
        option=DumpDbs()
    elif selected==7:
        option=PackDbs()
    elif selected==8:
        option=UnpackPck()
    elif selected==9:
        option=PackPck()
    title.pack_forget()
    title=Label(selectedFrame,text=tool[selected],font=('Fixdsys 14 bold'))
    title.pack()

def clear():
    try:
        name1.grid_forget()
        entry1.grid_forget()
        button1.grid_forget()
    except:pass
    try:
        name2.grid_forget()
        entry2.grid_forget()
        button2.grid_forget()
    except:pass
    try:
        name3.grid_forget()
        entry3.grid_forget()
        button3.grid_forget()
    except:pass
    try:
        buttonB.grid_forget()
    except:pass
    try:
        nameC.grid_forget()
        entryC.grid_forget()
    except:pass

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


class UnpackScene:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
    def run(self):
        cmd=["SceneUnpacker",value1.get(),value2.get()]
        return SceneUnpacker.main(cmd,DECRYPT_KEY)

class PackScene:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
        valueC.set('17')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
    def run(self):
        cmd=["ScenePacker",value1.get(),value2.get(),value3.get()]
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
        return ScenePacker.main(cmd,DECRYPT_KEY)
        
class UnpackGameexe:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
    def run(self):
        cmd=["GameexeUnpacker",value1.get(),value2.get()]
        return GameexeUnpacker.main(cmd,DECRYPT_KEY)

class PackGameexe:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
        valueC.set('0')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
        valueB.set(False)
        buttonB=Checkbutton(inputFrame,text="Double Encryption(Useless)",variable=valueB)
        buttonB.grid(row=8,padx=2,pady=4,sticky='e')
    def run(self):
        cmd=["GameexePacker",value1.get(),value2.get(),value3.get()]
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
        return GameexePacker.main(cmd,DECRYPT_KEY)

class DumpSs:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
    def run(self):
        cmd=["ssDumper",value1.get(),value2.get()]
        return ssDumper.main(cmd)

class PackSs:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
    def run(self):
        cmd=["ssPacker",value1.get(),value2.get(),value3.get()]
        return ssPacker.main(cmd)

class DumpDbs:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
        clear()
        name1=Label(inputFrame,text="Dbs file:")
        name1.grid(row=0,padx=2,sticky='w')
        value1.set("*.dbs")
        entry1=Entry(inputFrame,width=ENTRY_WIDTH,textvariable=value1)
        entry1.grid(row=1,column=0,padx=2)
        button1=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFile(value1))
        button1.grid(row=1,column=1,padx=2)
    def run(self):
        cmd=["dbsDecrypt",value1.get()]
        return dbsDecrypt.main(cmd)

class PackDbs:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
        valueC.set('17')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
    def run(self):
        cmd=["dbsEncrypt",value1.get(),value2.get()]
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
        return dbsEncrypt.main(cmd)

class UnpackPck:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
    def run(self):
        cmd=["pckUnpacker",value1.get(),value2.get()]
        return pckUnpacker.main(cmd)
        
class PackPck:
    def __init__(self):
        global name1,name2,name3,entry1,entry2,entry3,button1,button2,button3
        global buttonB,nameC,entryC
        global value1,value2,value3,valueB,valueC
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
    def run(self):
        cmd=["pckPacker",value1.get(),value2.get()]
        return pckPacker.main(cmd)


root=Tk()
root.title("Siglus Tools")
root.geometry("640x320")
#root.resizable(False,False)
lastSelect=0
keyFrame=Frame(root,padx=PAD,pady=PAD)
keyFrame.pack(side='bottom',fill='x')
mainFrame=Frame(root,padx=PAD,pady=PAD)
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
valueC=StringVar()
keyVar=StringVar()
tempKey=loadKey()

keyInfo=Frame(keyFrame)
keyInfo.pack(side='top',anchor='w',fill='x')
startButton=Button(keyFrame,text="Start",command=start,width=6)
startButton.pack(side='right',padx=PAD,pady=PAD,anchor='e')

if tempKey:
    DECRYPT_KEY=tempKey
keyVar.set(stringKey(DECRYPT_KEY))
keyEntry=Entry(keyFrame,width=80,textvariable=keyVar)
keyEntry.bind("<Control-Key-v>",unlock)
keyEntry.pack(side='left',padx=PAD,pady=PAD,anchor='w')

try:
    f=subprocess.Popen(os.getcwd()+"\\skf.exe")
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
    hasList=False
else:
    hasList=True
    keyList=[stringKey(DECRYPT_KEY)]
    keyName=[""]
    for line in listFile.readlines():
        if line[-2:]=='：\n':
            keyName.append(line[:-2])
        elif line!='\n':
            keyList.append(line[:-1])
    listFile.close()
    if hasSkf:
        listWidth=45
    else:
        listWidth=55
    keySelect=Combobox(keyInfo,width=listWidth,state='readonly',value=keyName)
    keySelect.bind("<<ComboboxSelected>>",selectKey)
    keySelect.current(0)
    keySelect.pack(side='left',anchor='e')

optionLabel=Label(optionFrame,text="Select option:")
optionLabel.pack(side='top',anchor='w')
optionVar=StringVar()
optionVar.set(tool)
optionList=Listbox(optionFrame,listvariable=optionVar,height=10)
optionList.selection_set(0)
title=Label(selectedFrame,text=tool[0],font=('Fixdsys 14 bold'))
title.pack()
option=UnpackScene()
optionList.bind('<ButtonRelease-1>',select)
optionList.pack(side='top',fill='y')

root.mainloop()
