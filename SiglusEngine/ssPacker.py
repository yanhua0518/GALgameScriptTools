# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import struct
import unicodedata

class Header:
    headerData=b''
    headerList=[]
    length=0
    index=0
    count=0
    offset=0
    dataCount=0
    def __init__(H,f):
        f.seek(0)
        H.length=struct.unpack('I',f.read(4))[0]
        H.headerData=f.read(128)
        H.headerList=struct.unpack('32I',H.headerData)
        H.index=H.headerList[2]
        H.count=H.headerList[3]
        H.offset=H.headerList[4]
        H.datacount=H.headerList[5]

def Decrypt(string,l,k):
    key=28807
    localKey=key*k%65536
    newString=b''
    for n in range(0,l):
        newString+=struct.pack('H',localKey^struct.unpack('H',string[n*2:n*2+2])[0])
    return newString

def Check(scr):
    for char in scr:
        if unicodedata.east_asian_width(char)!='Na':
            return True
    return False


if len(sys.argv) < 3:
    print ("Usage: "+sys.argv[0]+" <Scene\> <Text\> [Scene_packed\]")
    quit()

inF=sys.argv[1]+"\\"
txtF=sys.argv[2]+"\\"
if len(sys.argv) < 4:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+sys.argv[1][sys.argv[1].rfind("\\")+1:]+"_packed\\"
else:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+sys.argv[3]+"\\"

if not os.path.exists(outF):
    os.makedirs(outF)

for txtFN in glob.glob(txtF+"*.txt"):
    print(txtFN)
    inFN=inF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
    outFN=outF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
    size=os.path.getsize(inFN)
    file=open(inFN,'rb')
    header=Header(file)
    file.seek(header.index)
    offset=[]
    length=[]
    for n in range(0,header.count):
        offset.append(struct.unpack('I',file.read(4))[0])
        length.append(struct.unpack('I',file.read(4))[0])
    string=[]
    for x in range(0,header.count):
        if length[x]==0:
            string.append(b'')
            continue
        file.seek(header.offset+offset[x]*2,0)
        string.append(file.read(length[x]*2))
    file.seek(header.offset)
    ssData=file.read()
    file.close()
    txt=open(txtFN,'r',1,"UTF-8")
    for line in txt.readlines():
        if not line[0]==u"●":
            continue
        index=int(line[1:line.find("●",1)])
        text=line[line.find("●",1)+1:-1]
        length[index]=len(text)
        string[index]=Decrypt(text.encode("UTF-16")[2:],length[index],index)
    txt.close()
    output=open(outFN,'wb')
    output.write(struct.pack("I",header.length))
    output.write(header.headerData[:16])
    output.write(struct.pack("I",size))
    output.write(header.headerData[20:])
    newOffset=0
    for n in range(0,header.count):
        output.write(struct.pack("I",newOffset))
        output.write(struct.pack("I",length[n]))
        newOffset+=length[n]
    output.write(ssData)
    for x in range(0,header.count):
        output.write(string[x])
    output.close()
