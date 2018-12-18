# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
from io import BytesIO
import struct

'''
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
'''

def main(argv):
        
    if len(argv)<2:
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <folder\> [output file]")
        return

    inF=argv[1]+"\\"
    inList=glob.glob(inF+"*.*")
    fileCount=len(inList)
    if fileCount<1:
        print("No file to pack!")
        return
    
    if len(argv)<3:
        outFN=(argv[1]+".pck").replace("\\.",".").replace("/.",".")
    else:
        outFN=argv[2]

    indexOffset=32
    fileName=[]
    nameLength=[]
    fileSize=[]
    for inFN in inList:
        name=inFN[inFN.rfind("\\")+1:].encode("UTF-16").replace(b"\xff\xfe",b"")
        fileName.append(name)
        nameLength.append(len(name))
        size=os.path.getsize(inFN)
        fileSize.append(size)

    pck=BytesIO()
    pck.write(b'\x01\x00\x00\x00')
    pck.write(struct.pack('I',fileCount))
    pck.write(bytes(24))
    pck.write(struct.pack('%dI'%fileCount,*nameLength))
    for data in fileName:
        pck.write(data)
    sizeOffset=pck.tell()
    if sizeOffset%4:
        pck.write(bytes(4-sizeOffset%4))
        sizeOffset=pck.tell()
    dataOffset=sizeOffset+fileCount*16
    offset=dataOffset
    for size in fileSize:
        pck.write(struct.pack('2Q',offset,size))
        offset+=size
    pck.seek(8)
    pck.write(struct.pack('2I',dataOffset-indexOffset,sizeOffset-indexOffset))
    output=open(outFN,'wb')
    output.write(pck.getvalue())
    pck.close()
    for inFN in inList:
        print(inFN)
        file=open(inFN,'rb')
        output.write(file.read())
        file.close()
    output.close()

if __name__=="__main__":
    main(sys.argv)
