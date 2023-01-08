# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
from Decryption import Decrypt1,Decrypt4,Decompress

def main(argv,key):

    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Gameexe.dat> [Gameexe.ini]")
        return False

    if len(argv)<3 or argv[2]=='':
        outFN="Gameexe.ini"
    else:
        outFN=argv[2]

    try:
        f=open(argv[1],'rb')
        f.read()
        f.close()
    except:
        return False

    gameexe=open(argv[1],'rb')
    header=gameexe.read(4)
    needKey=gameexe.read(4)
    data=Decrypt4(gameexe.read())
    if needKey==b'\x01\x00\x00\x00':
        data=Decrypt1(data,key)
    compSize,decompSize=struct.unpack('2I',data[:8])
    try:
        data=Decompress(data[8:],decompSize)
        output=open(outFN,'wb')
        output.write(b'\xff\xfe'+data)
        output.close()
    except Exception as e:
        return e
    return True

if __name__=="__main__":
    main(sys.argv,[])
