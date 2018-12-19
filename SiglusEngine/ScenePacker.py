# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
from Decryption import Decrypt1,Decrypt2,FakeCompress,Compress

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

def main(argv,key):
    
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
        
    if len(argv)<3 or argv[1]=='' or argv[2]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene.pck> <Scene\> [Scene.pck2] [-c [2~17]]")
        return False

    if len(argv)<4 or argv[3]=='':
        outFN="Scene.pck2"
    else:
        outFN=argv[3]

    inF=argv[0][:argv[0].rfind("\\")+1]+argv[2]+"\\"
    try:
        f=open(argv[1],'rb')
        f.read()
        f.close()
    except:
        return False
        
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
        if comp:
            compData=Compress(data,comp)
        else:
            compData=FakeCompress(data)
        '''
        compFile=open(inF+fileName+'.compressed','wb')
        compFile.write(compData)
        compFile.close()
        '''
        if header.ExtraKeyUse:
            SceneData[n]=Decrypt2(Decrypt1(compData,key))
        else:
            SceneData[n]=Decrypt2(compData)
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
    return True

if __name__=="__main__":
    main(sys.argv,[])
