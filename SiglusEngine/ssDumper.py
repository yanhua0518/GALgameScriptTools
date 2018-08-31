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


if len(sys.argv) < 2:
    print ("Usage: "+sys.argv[0]+" <Scene\> [Text\]")
    quit()

inF=sys.argv[1]+"\\"
if len(sys.argv) < 3:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+sys.argv[1][sys.argv[1].rfind("\\")+1:]+"_out\\"
else:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+sys.argv[2]+"\\"

if not os.path.exists(outF):
    os.makedirs(outF)

for inFN in glob.glob(inF+"*.ss"):
    print(inFN)
    outFN=outF+inFN[inFN.rfind("\\")+1:]+".txt"
    size=os.path.getsize(inFN)
    file=open(inFN,'rb')
    header=Header(file)
    file.seek(header.index)
    offset=[]
    length=[]
    for n in range(0,header.count):
        offset.append(struct.unpack('I',file.read(4))[0])
        length.append(struct.unpack('I',file.read(4))[0])
    output=open(outFN,'w',1,"UTF-8")
    for x in range(0,header.count):
        if length[x]==0:
            continue
        file.seek(header.offset+offset[x]*2,0)
        string=file.read(length[x]*2)
        text=Decrypt(string,length[x],x).decode("UTF-16")
        if not Check(text):
            continue
        outLine="○"+'%.6d'%x+"○"+text+"\n●"+'%.6d'%x+"●"+text+"\n\n"
        output.write(outLine)
    file.close()
    output.close()
    if os.path.getsize(outFN)==0:
        os.remove(outFN)

