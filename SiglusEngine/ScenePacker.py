# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from ctypes import *
import struct

class Header:
    length=0
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

def FakeCompress(string):
    ssSize=len(string)
    dataSize=ssSize+int(ssSize/8)
    if not ssSize%8==0:
        dataSize+=1
    newString=bytes(dataSize)
    dll.fakeCompress(string,newString,ssSize)
    return struct.pack('2I',dataSize,ssSize)+newString

def Compress(string):
    length=len(string)
    size=c_int(0)
    p=Xmoe.CompressData(string,length,pointer(size),17)
    newString=string_at(p,size)
    return newString
    

argv=sys.argv
if argv.count('-c')>0:
    doComp=True
    argv.remove('-c')
else:
    doComp=False
    
if len(argv)<3:
    print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene.pck> <Scene\> [Scene.pck2] [-c]")
    quit()

if len(argv)<4:
    outFN="Scene.pck2"
else:
    outFN=argv[3]

inF=argv[0][:argv[0].rfind("\\")+1]+argv[2]+"\\"
try:
    f=open(argv[1],'rb')
    f.read()
    f.close()
except:
    quit()
    
try:
    dll=CDLL('Decryption.dll')
except:
    print("Can't open Decryption.dll")
    quit()
if doComp:
    try:
        Xmoe=CDLL('Compression.dll')
    except:
        print("Can't open Compression.dll")
        quit()

size=os.path.getsize(argv[1])
scene=open(argv[1],'rb')
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
    

for n in range(0,header.SceneDataCount):
    fileName=SceneNameString[n].decode("UTF-16")+'.ss'
    try:
        f=open(inF+fileName,'rb')
        f.read()
        f.close()
    except:
        continue
    print(fileName)
    ssFile=open(inF+fileName,'rb')
    data=ssFile.read()
    if doComp:
        compData=Compress(data)
    else:
        compData=FakeCompress(data)
    '''
    compFile=open(inF+fileName+'.compressed','wb')
    compFile.write(compData)
    compFile.close()
    '''
    SceneData[n]=Decrypt1(Decrypt2(compData))
    SceneDataLength[n]=len(compData)
    ssFile.close()
    

output=open(outFN,'wb')
'''
output.write(struct.pack('I',header.length))
output.write(header.headerData)
output.write(struct.pack('I',header.ExtraKeyUse))
output.write(struct.pack('I',header.SourceHeaderLength))
'''
scene.seek(0)
output.write(scene.read(header.SceneInfoOffset))
offset=0
for n in range(0,header.SceneInfoCount):
    output.write(struct.pack('2I',offset,SceneDataLength[n]))
    offset+=SceneDataLength[n]

for n in range(0,header.SceneDataCount):
    output.write(SceneData[n])
scene.close()
output.close()
