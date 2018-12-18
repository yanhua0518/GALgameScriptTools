# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
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

def main(argv):
        
    if len(argv)<2:
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <pck file> [output folder\]")
        return

    if len(argv)<3:
        outF=argv[1].replace(".pck","")+"\\"
    else:
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[2]+"\\"

    try:
        f=open(argv[1],'rb')
        f.read()
        f.close()
    except:
        return

    size=os.path.getsize(argv[1])
    scene=open(argv[1],'rb')
    header=Header(scene)
    if not header.type==1:
        print("NOT a pck data file!")
        return

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

if __name__=="__main__":
    main(sys.argv)
