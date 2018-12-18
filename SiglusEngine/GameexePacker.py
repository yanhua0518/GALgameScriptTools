# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
from Decryption import Decrypt1,Decrypt4,FakeCompress,Compress

def main(argv):

    if argv.count('-p')>0:
        needKey=True
        argv.remove('-p')
    else:
        needKey=False

    if argv.count('-c')>0:
        try:
            comp=int(argv[argv.index('-c')+1])
        except:
            comp=17
        else:
            argv.pop(argv.index('-c')+1)
        if comp<2:
            comp=2
        elif comp>17:
            comp=17
        argv.remove('-c')
    else:
        comp=0

    if len(argv)<2:
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Gameexe.ini> [Gameexe.dat2] [-p] [-c]")
        return

    if len(argv)<3:
        outFN="Gameexe.dat2"
    else:
        outFN=argv[2]
    try:
        ini=open(argv[1],'rb')
        ini.read(2)
    except:
        return

    data=ini.read()
    ini.close()
    size=len(data)
    if comp:
        compData=Compress(data,comp)
    else:
        compSize=size+int(size/8)+8
        if not size%8==0:
            compSize+=1
        compData=struct.pack('2I',compSize,size)+FakeCompress(data)
    if needKey:
        outData=b'\x00\x00\x00\x00\x01\x00\x00\x00'+Decrypt4(Decrypt1(compData))
    else:
        outData=b'\x00\x00\x00\x00\x00\x00\x00\x00'+Decrypt4(compData)

    output=open(outFN,'wb')
    output.write(outData)
    output.close()

if __name__=="__main__":
    main(sys.argv)
