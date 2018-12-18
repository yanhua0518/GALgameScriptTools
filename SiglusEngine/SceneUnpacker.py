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

def main(argv):
    
    if len(argv)<2:
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene.pck> [Scene\]")
        return

    if len(argv)<3:
        outF=argv[0][:argv[0].rfind("\\")+1]+"Scene\\"
    else:
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[2]+"\\"

    try:
        f=open(argv[1],'rb')
        f.read()
        f.close()
    except:
        return
    
    if not os.path.exists(outF):
        os.makedirs(outF)

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
        
    scene.close()

    for n in range(0,header.SceneDataCount):
        fileName=SceneNameString[n].decode("UTF-16")+'.ss'
        print(fileName)
        if header.ExtraKeyUse:
            data=Decrypt2(Decrypt1(SceneData[n]))
        else:
            data=Decrypt2(SceneData[n])
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

if __name__=="__main__":
    main(sys.argv)
