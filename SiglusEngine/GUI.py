# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from ctypes import *
from tkinter import *
from tkinter.filedialog import *
from tkinter import messagebox
import struct

tool=["Unpack Scene","Pack Scene","Unpack Gameexe","Pack Gameexe",
        "Dump ss","Pack ss","Dump dbs","Pack dbs","Unpack pck","Pack pck"]
command=["SceneUnpacker.py","ScenePacker.py","GameexeUnpacker.py",
         "GameexePacker.py","ssDumper.py","ssPacker.py",
         "dbsDecrypt.py","dbsEncrypt.py","pckUnpacker.py","pckPacker.py"]

ENTRY_WIDTH=58
BUTTON_WIDTH=6
PAD=4
lastDir=os.getcwd()

def start():
    global lastSelect,option
    optionList.selection_set(lastSelect)
    cmdLine=command[lastSelect]+' '+option.format()
    print(cmdLine)
    try:
        os.system("python "+cmdLine)
    except:
        messagebox.showerror("Error!","Error!")
    else:
        messagebox.showinfo("Notice","Finished!")
    

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
    except:True
    try:
        name2.grid_forget()
        entry2.grid_forget()
        button2.grid_forget()
    except:True
    try:
        name3.grid_forget()
        entry3.grid_forget()
        button3.grid_forget()
    except:True
    try:
        buttonB.grid_forget()
    except:True
    try:
        nameC.grid_forget()
        entryC.grid_forget()
    except:True

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
    def format(self):
        cmd=value1.get()+' '+value2.get()
        return cmd

    
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
    def format(self):
        cmd=value1.get()+' '+value2.get()+' '+value3.get()
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
            cmd+=' -c '+str(comp)
        return cmd
        

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
    def format(self):
        cmd=value1.get()+' '+value2.get()
        return cmd

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
        value1.set("Gameeexe.ini")
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
    def format(self):
        cmd=value1.get()+' '+value2.get()+' '+value3.get()
        if valueB.get():
            cmd+='-p'
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
            cmd+=' -c '+str(comp)
        return cmd

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
    def format(self):
        cmd=value1.get()+' '+value2.get()
        return cmd

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
    def format(self):
        cmd=value1.get()+' '+value2.get()+' '+value3.get()
        return cmd

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
    def format(self):
        cmd=value1.get()
        return cmd

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
        button2=Button(inputFrame,text="Select",width=BUTTON_WIDTH,command=lambda:selectFolder(value2))
        button1.grid(row=1,column=1,padx=2)
        button2.grid(row=3,column=1,padx=2)
        valueC.set('17')
        nameC=Label(inputFrame,text="Compression Level(2-17, 0 for Fake Compression): ")
        nameC.grid(row=7,padx=2,pady=4,sticky='e')
        entryC=Entry(inputFrame,width=4,textvariable=valueC)
        entryC.grid(row=7,column=1,padx=2,pady=4)
    def format(self):
        cmd=value1.get()+' '+value2.get()
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
            cmd+=' -c '+str(comp)
        return cmd

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
    def format(self):
        cmd=value1.get()+' '+value2.get()
        return cmd
        
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
    def format(self):
        cmd=value1.get()+' '+value2.get()
        return cmd


root=Tk()
root.title("Siglus Tools")
root.geometry("640x260")
root.resizable(False,False)
lastSelect=0
optionFrame=Frame(root,padx=PAD,pady=PAD)
optionFrame.pack(side='left',fill='both')
rightFrame=Frame(root,padx=PAD,pady=PAD)
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

optionLabel=Label(optionFrame,text="Select option:")
optionLabel.pack(side='top',anchor='w')
optionVar=StringVar()
optionVar.set(tool)
optionList=Listbox(optionFrame,listvariable=optionVar,height=12)
optionList.selection_set(0)
title=Label(selectedFrame,text=tool[0],font=('Fixdsys 14 bold'))
title.pack()
option=UnpackScene()
optionList.bind('<ButtonRelease-1>',select)
optionList.pack(side='top',fill='y')

startButton=Button(rightFrame,text="Start",command=start,width=BUTTON_WIDTH)
startButton.pack(side='bottom',padx=2,pady=2,anchor='e')


root.mainloop()
