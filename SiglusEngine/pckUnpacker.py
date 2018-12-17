# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from ctypes import *
import struct

class Header:
    def __init__(H,f):
        f.seek(0)
        H.indexOffset=32
        H.headerData=f.read(32)
        H.headerList=struct.unpack('8I',H.headerData)
        H.type=H.headerList[0]
        H.fileCount=H.headerList[1]
        H.dataOffset=H.headerList[2]+H.indexOffset
        H.sizeOffset=H.headerList[3]+H.indexOffset
        H.nameOffset=H.indexOffset+H.fileCount*4
        

if len(sys.argv)<2:
    print ("Usage: "+sys.argv[0]+" <pck file> [output folder\]")
    quit()

if len(sys.argv)<3:
    outF=sys.argv[1].replace(".pck","")+"\\"
else:
    outF=sys.argv[0][:sys.argv[0].rfind("\\")+1]+sys.argv[2]+"\\"

try:
    f=open(sys.argv[1],'rb')
    f.read()
    f.close()
except:
    quit()

size=os.path.getsize(sys.argv[1])
scene=open(sys.argv[1],'rb')
header=Header(scene)
if not header.type==1:
    print("NOT a pck data file!")
    quit()

if not os.path.exists(outF):
    os.makedirs(outF)

scene.seek(header.indexOffset)
nameLength=struct.unpack('%dI'%header.fileCount,scene.read(header.fileCount*4))
fileName=[]
for n in range(0,header.fileCount):
    fileName.append(scene.read(nameLength[n]))
    #print(fileName[n].decode("UTF-16"))
    
scene.seek(header.sizeOffset)
fileOffset=[]
fileLength=[]
for n in range(0,header.fileCount):
    fileOffset.append(struct.unpack('Q',scene.read(8))[0])
    fileLength.append(struct.unpack('Q',scene.read(8))[0])

scene.seek(header.dataOffset)
for n in range(0,header.fileCount):
    outFN=fileName[n].decode("UTF-16")
    scene.seek(fileOffset[n])
    print(outFN)
    fileData=scene.read(fileLength[n])
    output=open(outF+outFN,'wb')
    output.write(fileData)
    output.close()
scene.close()
