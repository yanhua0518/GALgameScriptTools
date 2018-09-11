# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from ctypes import *
import struct

class Header:
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
    if header.ExtraKeyUse==0:
        return string
    # Change this key to your game's key.
    key=[0x2E, 0x4B, 0xDD, 0x2A, 0x7B, 0xB0, 0x0A, 0xBA,
         0xF8, 0x1A, 0xF9, 0x61, 0xB0, 0x18, 0x98, 0x5C]
    size=len(string)
    keyBuf=c_char_p(struct.pack('16B',*key))
    dll.decrypt1(string,size,keyBuf)
    return string

def Decrypt2(string):
    size=len(string)
    dll.decrypt2(string,size)
    return string

def Decompress(string,size):
    newString=bytes(size)
    dll.decompress(string,newString,size)
    return newString


if len(sys.argv)<2:
    print ("Usage: "+sys.argv[0]+" <Scene.pck> [Scene\]")
    quit()

if len(sys.argv)<3:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+"Scene\\"
else:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+sys.argv[2]+"\\"

try:
    f=open(sys.argv[1],'rb')
    f.read()
    f.close()
except:
    quit()

try:
    dll=CDLL('Decryption.dll')
except:
    print("Can't open Decryption.dll")
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
    fileName=SceneNameString[n].decode("UTF-16")+'.ss'
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
