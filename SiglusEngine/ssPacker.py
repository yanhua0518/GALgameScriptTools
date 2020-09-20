# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import struct
import unicodedata
import openpyxl
from Decryption import Decrypt

class ss:

    def __init__(H,fn):
        H.fileSize=os.path.getsize(fn)
        f=open(fn,'rb')
        H.headerLength=struct.unpack('I',f.read(4))[0]
        H.headerData=f.read(128)
        H.headerList=list(struct.unpack('32I',H.headerData))
        H.unknownOffset=H.headerList[0]
        H.unknownLength=H.headerList[1]
        H.index=H.headerList[2]
        H.count=H.headerList[3]
        H.dataOffset=H.headerList[4]
        H.datacount=H.headerList[5]
        f.seek(H.index)
        H.offset=[]
        H.length=[]
        for n in range(0,H.count):
            H.offset.append(struct.unpack('I',f.read(4))[0])
            H.length.append(struct.unpack('I',f.read(4))[0])
        H.string=[]
        for x in range(0,H.count):
            if H.length[x]==0:
                H.string.append(b'')
                continue
            f.seek(H.dataOffset+H.offset[x]*2,0)
            H.string.append(f.read(H.length[x]*2))
        f.seek(H.unknownOffset)
        H.ssData=f.read()
        f.close()

    def write(H,fn):
        f=open(fn,'wb')
        f.write(struct.pack("I",H.headerLength))
        f.write(bytes(128))
        newOffset=0
        for n in range(0,H.count):
            f.write(struct.pack("I",newOffset))
            f.write(struct.pack("I",H.length[n]))
            newOffset+=H.length[n]
        offsetDev=H.unknownOffset-f.tell()
        f.write(H.ssData)
        for x in range(0,H.count):
            f.write(H.string[x])
        H.headerList[0]=H.unknownOffset-offsetDev
        H.headerList[4]=H.fileSize-offsetDev
        for i in range(6,32,2):
            H.headerList[i]=H.headerList[i]-offsetDev
        f.seek(4)
        f.write(struct.pack("32I",*H.headerList))
        f.close()

def Check(scr):
    for char in scr:
        if unicodedata.east_asian_width(char)!='Na':
            return True
    return False

def main(argv):
    if argv.count('-x')>0:
        xlsxMode=True
        argv.remove('-x')
    else:
        xlsxMode=False
        
    if len(argv)<3 or argv[1]=='' or argv[2]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene\> <Text\> [Scene_packed\] [-x]")
        return False

    inF=argv[1]+"\\"
    txtF=argv[2]+"\\"
    if len(argv)<4 or argv[3]=='':
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[1][argv[1].rfind("\\")+1:]+"_packed\\"
    else:
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[3]+"\\"

    if not os.path.exists(outF):
        os.makedirs(outF)

    for txtFN in glob.glob(txtF+"*.txt"):
        print(txtFN)
        inFN=inF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
        outFN=outF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
        SS=ss(inFN)
        txt=open(txtFN,'r',1,"UTF-8")
        for line in txt.readlines():
            if not line[0]==u"●":
                continue
            index=int(line[1:line.find("●",1)])
            text=line[line.find("●",1)+1:].replace("\n","").replace("~","～").replace("―","—").replace("－","—")
            SS.length[index]=len(text)
            SS.string[index]=Decrypt(text.encode("UTF-16")[2:],SS.length[index],index)
        txt.close()
        SS.write(outFN)

    if xlsxMode:
        for txtFN in glob.glob(txtF+"*.xlsx"):
            print(txtFN)
            workBook=openpyxl.load_workbook(txtFN)
            for sheet in workBook:
                name=sheet['D1'].value
                if name==None or name=="" or len(sheet.title)<31:
                    name=sheet.title
                print(name)
                inFN=inF+name
                outFN=outF+name
                SS=ss(inFN)
                for a,c in zip(sheet['A'],sheet['C']):
                    try:
                        index=int(a.value)
                    except:
                        continue
                    text=c.value
                    if text==None:
                        text=""
                    else:
                        text=text.replace("~","～").replace("―","—").replace("－","—")
                    SS.length[index]=len(text)
                    SS.string[index]=Decrypt(text.encode("UTF-16")[2:],SS.length[index],index)
                SS.write(outFN)
                
    return True

if __name__=="__main__":
    main(sys.argv)
    
