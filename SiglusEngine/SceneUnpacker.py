# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from io import BytesIO
import glob
import struct
import unicodedata

class Header:
    headerData=b''
    varInfoOffset=0
    varNameIndexOffset=0
    varNameOffset=0
    cmdInfoOffset=0
    cmdNameIndexOffset=0
    cmdNameOffset=0
    SceneNameIndexOffset=0
    SceneNameOffset=0
    SceneInfoOffset=0
    SceneDataOffset=0
    varInfoCount=0
    varNameIndexCount=0
    varNameCount=0
    cmdInfoCount=0
    cmdNameIndexCount=0
    cmdNameCount=0
    SceneNameIndexCount=0
    SceneNameCount=0
    SceneInfoCount=0
    SceneDataCount=0
    ExtraKeyUse=0
    SourceHeaderLength=0
    def __init__(H,f):
        f.seek(0)
        H.length=struct.unpack('I',f.read(4))[0]
        H.headerData=f.read(80)
        f.seek(4)
        H.varInfoOffset,H.varInfoCount=struct.unpack('2I',f.read(8))
        H.varNameIndexOffset,H.varNameIndexCount=struct.unpack('2I',f.read(8))
        H.varNameOffset,H.varNameCount=struct.unpack('2I',f.read(8))
        H.cmdInfoOffset,H.cmdInfoCount=struct.unpack('2I',f.read(8))
        H.cmdNameIndexOffset,H.cmdNameIndexCount=struct.unpack('2I',f.read(8))
        H.cmdNameOffset,H.cmdNameCount=struct.unpack('2I',f.read(8))
        H.SceneNameIndexOffset,H.SceneNameIndexCount=struct.unpack('2I',f.read(8))
        H.SceneNameOffset,H.SceneNameCount=struct.unpack('2I',f.read(8))
        H.SceneInfoOffset,H.SceneInfoCount=struct.unpack('2I',f.read(8))
        H.SceneDataOffset,H.SceneDataCount=struct.unpack('2I',f.read(8))
        H.ExtraKeyUse=struct.unpack('I',f.read(4))[0]
        H.SourceHeaderLength=struct.unpack('I',f.read(4))[0]

def Decrypt1(string):
    key=[0x2E, 0x4B, 0xDD, 0x2A, 0x7B, 0xB0, 0x0A, 0xBA,
         0xF8, 0x1A, 0xF9, 0x61, 0xB0, 0x18, 0x98, 0x5C]
    newString=b''
    for n in range(0,len(string)):
        newString+=bytes([string[n]^key[n&15]])
    return newString

def Decrypt2(string):
    key=[0x70,0xF8,0xA6,0xB0,0xA1,0xA5,0x28,0x4F,
         0xB5,0x2F,0x48,0xFA,0xE1,0xE9,0x4B,0xDE,
         0xB7,0x4F,0x62,0x95,0x8B,0xE0,0x03,0x80,
         0xE7,0xCF,0x0F,0x6B,0x92,0x01,0xEB,0xF8,
         0xA2,0x88,0xCE,0x63,0x04,0x38,0xD2,0x6D,
         0x8C,0xD2,0x88,0x76,0xA7,0x92,0x71,0x8F,
         0x4E,0xB6,0x8D,0x01,0x79,0x88,0x83,0x0A,
         0xF9,0xE9,0x2C,0xDB,0x67,0xDB,0x91,0x14,
         0xD5,0x9A,0x4E,0x79,0x17,0x23,0x08,0x96,
         0x0E,0x1D,0x15,0xF9,0xA5,0xA0,0x6F,0x58,
         0x17,0xC8,0xA9,0x46,0xDA,0x22,0xFF,0xFD,
         0x87,0x12,0x42,0xFB,0xA9,0xB8,0x67,0x6C,
         0x91,0x67,0x64,0xF9,0xD1,0x1E,0xE4,0x50,
         0x64,0x6F,0xF2,0x0B,0xDE,0x40,0xE7,0x47,
         0xF1,0x03,0xCC,0x2A,0xAD,0x7F,0x34,0x21,
         0xA0,0x64,0x26,0x98,0x6C,0xED,0x69,0xF4,
         0xB5,0x23,0x08,0x6E,0x7D,0x92,0xF6,0xEB,
         0x93,0xF0,0x7A,0x89,0x5E,0xF9,0xF8,0x7A,
         0xAF,0xE8,0xA9,0x48,0xC2,0xAC,0x11,0x6B,
         0x2B,0x33,0xA7,0x40,0x0D,0xDC,0x7D,0xA7,
         0x5B,0xCF,0xC8,0x31,0xD1,0x77,0x52,0x8D,
         0x82,0xAC,0x41,0xB8,0x73,0xA5,0x4F,0x26,
         0x7C,0x0F,0x39,0xDA,0x5B,0x37,0x4A,0xDE,
         0xA4,0x49,0x0B,0x7C,0x17,0xA3,0x43,0xAE,
         0x77,0x06,0x64,0x73,0xC0,0x43,0xA3,0x18,
         0x5A,0x0F,0x9F,0x02,0x4C,0x7E,0x8B,0x01,
         0x9F,0x2D,0xAE,0x72,0x54,0x13,0xFF,0x96,
         0xAE,0x0B,0x34,0x58,0xCF,0xE3,0x00,0x78,
         0xBE,0xE3,0xF5,0x61,0xE4,0x87,0x7C,0xFC,
         0x80,0xAF,0xC4,0x8D,0x46,0x3A,0x5D,0xD0,
         0x36,0xBC,0xE5,0x60,0x77,0x68,0x08,0x4F,
         0xBB,0xAB,0xE2,0x78,0x07,0xE8,0x73,0xBF]
    newString=b''
    for n in range(0,len(string)):
        newString+=bytes([string[n]^key[n&255]])
    return newString

def Decompress(string,size):
    count=0
    p=0
    print("Decompressing")
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
        if int(count/(size/100))>p:
            p+=1
            print("%.2d"%p)
    newString=output.getvalue()
    forDecomp.close()
    output.close()
    print('OK!')
    return newString



if len(sys.argv) < 2:
    print ("Usage: "+sys.argv[0]+" <Scene.pck> [Scene\]")
    quit()


if len(sys.argv) < 3:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+"Scene\\"
else:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+sys.argv[2]+"\\"

try:
    f=open(sys.argv[1],'rb')
    f.read()
    f.close()
except:
    quit()
    
if not os.path.exists(outF):
    os.makedirs(outF)


size=os.path.getsize(sys.argv[1])
scene=open(sys.argv[1],'rb')
header=Header(scene)

scene.seek(header.SceneNameIndexOffset)
SceneNameOffset=[]
SceneNameLength=[]
for n in range(0,header.SceneNameIndexCount):
    SceneNameOffset.append(struct.unpack('I',scene.read(4))[0])
    SceneNameLength.append(struct.unpack('I',scene.read(4))[0])
    
scene.seek(header.SceneNameOffset)
SceneNameString=[]
for n in range(0,header.SceneNameCount):
    SceneNameString.append(scene.read(SceneNameLength[n]*2))
    #print(SceneNameString[n].decode("UTF-16"))
    
scene.seek(header.SceneInfoOffset)
SceneDataOffset=[]
SceneDataLength=[]
for n in range(0,header.SceneInfoCount):
    SceneDataOffset.append(struct.unpack('I',scene.read(4))[0])
    SceneDataLength.append(struct.unpack('I',scene.read(4))[0])
    
scene.seek(header.SceneDataOffset)
SceneData=[]
for n in range(0,header.SceneDataCount):
    SceneData.append(scene.read(SceneDataLength[n]))
    
scene.close()

for n in range(0,header.SceneDataCount):
    fileName='%.3d.'%n+SceneNameString[n].decode("UTF-16")+'.ss'
    print(fileName)
    data=Decrypt2(Decrypt1(SceneData[n]))
    '''
    output=open(outF+fileName+'.undecompressed','wb')
    output.write(data)
    output.close()
    '''
    compSize,decompSize=struct.unpack('2I',data[:8])
    decompData=Decompress(data[8:],decompSize)
    output=open(outF+fileName,'wb')
    output.write(decompData)
    output.close()
