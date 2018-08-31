# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from io import BytesIO
import glob
import struct
import unicodedata


'''
def Decompress(string,size):
    count=0
    p=0
    #print("Decompressing")
    forDecomp=BytesIO(string)
    output=BytesIO(bytearray(size))
    while output.tell()<size:
        s=8
        char=struct.unpack('B',forDecomp.read(1))[0]
        while s>0 and output.tell()!=size:
            if char&1:
                output.write(forDecomp.read(1))
                count+=1
            else:
                data=struct.unpack('H',forDecomp.read(2))[0]
                tempLen=(data&15)+2
                data>>=4
                count+=tempLen
                offset=output.tell()-data
                #output.write(output.getvalue()[offset:offset+tempLen]) #wrong
                while tempLen>0:
                    output.write(output.getvalue()[offset:offset+1])
                    offset+=1
                    tempLen-=1
            s-=1
            char>>=1
        if int(count/(size/10))>p:
            p=int(count/(size/10))
            if p<10:
                print('%.d'%(p*10)+"%",flush=True,end=',')
            else:
                print('%.d'%(p*10)+"%!")
    newString=output.getvalue()
    forDecomp.close()
    output.close()
    return newString
'''

def Decompress(string,size):
    count=0
    p=0
    #print("Decompressing")
    inI=0
    newString=b''
    while len(newString)<size:
        s=8
        char=string[inI]
        inI+=1
        while s>0 and len(newString)!=size:
            if char&1:
                newString+=string[inI:inI+1]
                inI+=1
                count+=1
            else:
                data=struct.unpack('H',string[inI:inI+2])[0]
                inI+=2
                tempLen=(data&15)+2
                data>>=4
                count+=tempLen
                offset=len(newString)-data
                while tempLen>0:
                    newString+=newString[offset:offset+1]
                    offset+=1
                    tempLen-=1
            s-=1
            char>>=1
        if int(count/(size/10))>p:
            p=int(count/(size/10))
            if p<10:
                print('%.d'%(p*10)+"%",flush=True,end=',')
            else:
                print('%.d'%(p*10)+"%!")
    return newString


if len(sys.argv) < 3:
    print ("Usage: "+sys.argv[0]+" <ss.Undecompressed> <ss>")
    quit()

try:
    f=open(sys.argv[1],'rb')
    f.read()
    f.close()
except:
    quit()


ss=open(sys.argv[1],'rb')
compSize,decompSize=struct.unpack('2I',ss.read(8))
data=ss.read()
ss.close()
decompData=Decompress(data,decompSize)
output=open(sys.argv[2],'wb')
output.write(decompData)
output.close()
