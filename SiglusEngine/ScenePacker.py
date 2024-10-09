# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
from Decryption import Decrypt1,Decrypt2,FakeCompress,Compress
from SceneUnpacker import Header,stringKey,searchKey

def sourceRemove(file):
    try:
        scene=open(file,'rb')
        header=Header(scene)
        scene.seek(header.SceneInfoOffset)
        SceneDataLength=[]
        for n in range(0,header.SceneInfoCount):
            SceneDataLength.append(struct.unpack('2I',scene.read(8))[1])
        size=header.SceneDataOffset+sum(SceneDataLength)
        output=open(file+'.new','wb')
        scene.seek(0)
        output.write(scene.read(size))
        output.write(b'\x00')
        output.seek(88)
        output.write(b'\x01\x00\x00\x00')
        scene.close()
        output.close()
    except Exception as e:
        return e
    return True

def main(argv,key):
    if argv.count('-d')>0:
        dftKey=True
        argv.remove('-d')
    else:
        dftKey=False
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
        try:
            argv.remove('-f')
        except:
            pass
    elif argv.count('-f')>0:
        comp=0
        argv.remove('-f')
    else:
        comp=2
        
    if len(argv)<3 or argv[1]=='' or argv[2]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene.pck> <Scene\> [Scene.pck2] [-c [2~17]/-f] [-d]")
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
        SceneData.append(Decrypt2(scene.read(SceneDataLength[n])))
        
    if header.ExtraKeyUse and key==[] and not dftKey:
        print("Searching key...")
        try:
            startIndex=SceneNameString.index(b'_\x00s\x00t\x00a\x00r\x00t\x00')
        except:
            pass
        else:
            print('_start')
            startData=SceneData[startIndex]
            key=searchKey(startData)
        if not key:
            for n in range(0,header.SceneDataCount):
                print(SceneNameString[n].decode("UTF-16"))
                startData=SceneData[n]
                key=searchKey(startData)
                if key:
                    break
        if key:
            print("Key found!")
            print(stringKey(key))
        else:
            print("Key not found!")
    
    if dftKey:
        print("Use default key.")
        #key=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
            SceneData[n]=Decrypt1(compData,key)
        else:
            SceneData[n]=compData
        SceneDataLength[n]=len(compData)
        ssFile.close()
        
    try:
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
            output.write(Decrypt2(SceneData[n]))
        scene.close()
        output.write(b'\00')
        output.seek(88)
        output.write(b'\x01\x00\x00\x00')
        
        output.close()
    except Exception as e:
        return e
    return True

if __name__=="__main__":
    main(sys.argv,[])
