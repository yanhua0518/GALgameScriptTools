# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
from Decryption import Decrypt1,Decrypt2,Decompress

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

def stringKey(key):
    keyHex=[]
    for byte in key:
        keyHex.append(hex(byte))
    keyStr=str(keyHex).replace("[","").replace("]","").replace("'","")
    return keyStr

def searchKey(data):
    key=[]
    size=len(data)
    sizeDec=struct.pack('I',size)
    sizeEnc=data[:4]
    for n in range(0,4):
        key.append(sizeDec[n]^sizeEnc[n])
    ptr=0
    check=bytes([key[0],key[1],key[2]^31,key[3]])
    while data[ptr:ptr+4]!=check:
        ptr+=16
        if ptr>size-36:
            return []
    check=[[],[],[]]
    x=0
    for n in range(0,3):
        x^=31
        for byte in data[ptr+4:ptr+16]:
            check[n].append(byte^x)
            x^=31
        ptr+=16
        #print(check[n])
    if check[0]==check[1]:
        key.extend(check[0])
    elif check[1]==check[2]:
        key.extend(check[1])
    else:
        return []
    return key


def main(argv,key):
    if argv.count('-n')>0:
        undecomp=True
        argv.remove('-n')
    else:
        undecomp=False
    if argv.count('-f')>0:
        keyOnly=True
        argv.remove('-f')
    else:
        keyOnly=False
    if argv.count('-d')>0:
        dftKey=True
        argv.remove('-d')
    else:
        dftKey=False
    
    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene.pck> [Scene\] 「-n] [-d] / [-f]")
        return False

    if not keyOnly:
        if len(argv)<3 or argv[2]=='':
            outF=argv[0][:argv[0].rfind("\\")+1]+"Scene\\"
        else:
            outF=argv[0][:argv[0].rfind("\\")+1]+argv[2]+"\\"
        if not os.path.exists(outF):
            os.makedirs(outF)
            
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
        scene.seek(header.SceneDataOffset+SceneDataOffset[n])
        SceneData.append(Decrypt2(scene.read(SceneDataLength[n])))
        
    scene.close()
    
    if (header.ExtraKeyUse and key==[] and not dftKey) or keyOnly:
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
            if keyOnly:
                return key
        else:
            print("Key not found!")
            return False
    
    if dftKey:
        print("Use default key.")
        #key=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for n in range(0,header.SceneDataCount):
        fileName=SceneNameString[n].decode("UTF-16")+'.ss'
        print(fileName)
        if header.ExtraKeyUse:
            data=Decrypt1(SceneData[n],key)
        else:
            data=SceneData[n]
        if undecomp:
            output=open(outF+fileName+'.undecompressed','wb')
            output.write(data)
            output.close()
        else:
            compSize,decompSize=struct.unpack('2I',data[:8])
            decompData=Decompress(data[8:],decompSize)
            output=open(outF+fileName,'wb')
            output.write(decompData)
            output.close()
    return True

if __name__=="__main__":
    main(sys.argv,[])
