# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import struct
import unicodedata
from Decryption import Decrypt

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
        H.dataCount=H.headerList[5]

def Check(scr):
    for char in scr:
        if unicodedata.east_asian_width(char)!='Na':
            return True
    return False

def main(argv):
    if argv.count('-a')>0:
        noDump=True
        argv.remove('-a')
    else:
        noDump=False
    
    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene\> [Text\] [-a]")
        return False

    inF=argv[1]+"\\"
    if len(argv)<3 or argv[2]=='':
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[1][argv[1].rfind("\\")+1:]+"_out\\"
    else:
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[2]+"\\"

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
            if not Check(text) and not noDump:
                continue
            outLine="○"+'%.6d'%x+"○"+text+"\n●"+'%.6d'%x+"●"+text+"\n\n"
            output.write(outLine)
        file.close()
        output.close()
        if os.path.getsize(outFN)==0:
            os.remove(outFN)
    return True

if __name__=="__main__":
    main(sys.argv)
