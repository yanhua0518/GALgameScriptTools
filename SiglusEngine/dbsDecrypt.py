# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct

'''
dbsHeader():
    fileSize I
    lineCount I
    dataCount I
    lineIndexOffset I
    dataFormatOffset I
    lineDataIndexOffset I
    textOffset I

lineIndex i
dataFormat():
    dataIndex I
    dataType I #0x53=string, 0x56=int

lineDataIndex[dataIndex] I
if dataType==0x56:
    lineData=lineDataIndex[dataIndex]
if dataType==0x53:
    lineDataOffset=lineDataIndex[dataIndex]
'''

class Header:
    fileSize=0
    headerData=b''
    fileSize=0
    lineCount=0
    dataCount=0
    lineIndexOffset=0
    dataFormatOffset=0
    lineDataIndexOffset=0
    textOffset=0
    def __init__(H,f):
        f.seek(0)
        H.fileSize=struct.unpack('I',f.read(4))[0]
        H.headerData=f.read(24)
        H.headerList=struct.unpack('6I',H.headerData)
        H.lineCount=H.headerList[0]
        H.dataCount=H.headerList[1]
        H.lineIndexOffset=H.headerList[2]
        H.dataFormatOffset=H.headerList[3]
        H.lineDataIndexOffset=H.headerList[4]
        H.textOffset=H.headerList[5]
        

def Decrypt1(string):
    key=[0x2D, 0x62, 0xF4, 0x89]
    newString=b''
    n=0
    for char in string:
        newString+=bytes([char^key[n]])
        n+=1
        n&=3
    
    return newString

def Decrypt2(string):
    key=[[0x0E, 0xC7, 0x90, 0x71],[0x35, 0xF1, 0x9B, 0x49]]
    r=[0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,
       1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,
       0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,
       1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,
       1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1]
    newString=b''
    n=0
    c=0
    for char in string:
        newString+=bytes([char^key[r[c]][n]])
        n+=1
        if n>3:
            n=0
            c+=1
            if c>79:
                c=0
    
    return newString

def Decompress(string,size):
    count=0
    #p=0
    #print("Decompressing")
    inI=0
    newString=b''
    while len(newString)<size:
        s=8
        char=string[inI]
        inI+=1
        while s>0 and len(newString)!=size:
            if char&1:
                newString+=string[inI:inI+1]
                inI+=1
                count+=1
            else:
                data=struct.unpack('H',string[inI:inI+2])[0]
                inI+=2
                tempLen=(data&15)+2
                data>>=4
                count+=tempLen
                offset=len(newString)-data
                while tempLen>0:
                    newString+=newString[offset:offset+1]
                    offset+=1
                    tempLen-=1
            s-=1
            char>>=1
        '''
        if int(count/(size/10))>p:
            p=int(count/(size/10))
            if p<10:
                print('%.d'%(p*10)+"%",flush=True,end=',')
            else:
                print('%.d'%(p*10)+"%!")
        '''
    return newString


if len(sys.argv) < 2:
    print ("Usage: "+sys.argv[0]+" <dbs file>")
    quit()


dbs=open(sys.argv[1],'rb')
header=dbs.read(4)
if header==b'\x00\x00\x00\x00':
    isUTF=False
else:
    isUTF=True
data=dbs.read()
dbs.close()
dataA=Decrypt1(data)
compSize,decompSize=struct.unpack('2I',dataA[:8])
dataB=Decompress(dataA[8:],decompSize)
dataC=Decrypt2(dataB)

output=open(sys.argv[1]+'.out','wb')
output.write(dataC)
output.close()

file=open(sys.argv[1]+'.out','rb')
header=Header(file)
file.seek(header.lineIndexOffset)
lineIndex=struct.unpack('%di'%header.lineCount,file.read(header.lineCount*4))

dataIndex=[]
dataType=[]
for n in range(0,header.dataCount):
    dataIndex.append(struct.unpack('I',file.read(4))[0])
    dataType.append(struct.unpack('I',file.read(4))[0])
lineData=[]
for m in range(0,header.lineCount):
    lineData.append([])
    for n in range(0,header.dataCount):
        tempData=struct.unpack('I',file.read(4))[0]
        if dataType[n]==0x53:
            tempTell=file.tell()
            file.seek(header.textOffset+tempData)
            tempString=b''
            if isUTF:
                tempChar=file.read(2)
                while tempChar!=b'\x00\x00' and tempChar!=b'':
                    tempString+=tempChar
                    tempChar=file.read(2)
                lineData[m].append(tempString.decode("UTF-16"))
            else:
                tempChar=file.read(1)
                while tempChar!=b'\x00' and tempChar!=b'':
                    tempString+=tempChar
                    tempChar=file.read(1)
                lineData[m].append(tempString.decode("Shift-JIS"))
            file.seek(tempTell)
        else:
            lineData[m].append(tempData)
file.seek(header.fileSize)
dummy=file.read()
file.close()

txt=open(sys.argv[1]+'.txt','w',1,"UTF-16")
if isUTF:
    txt.write('Unicode\n')
else:
    txt.write('ASCII\n')
for m in range(0,header.lineCount):
    txt.write('[%.4d]\n'%lineIndex[m])
    for n in range(0,header.dataCount):
        tempIndex=dataIndex[n]
        tempData=lineData[m][n]
        if dataType[n]==0x53 and tempData!='':
            txt.write('○%.2d○'%tempIndex+tempData+'\n●%.2d●'%tempIndex+lineData[m][n]+'\n\n')
        '''
        #int data:
        elif dataType[n]==0x56:
            txt.write('<%.2d>'%tempIndex+str(tempData)+'\n')
        '''
    txt.write('\n')
txt.close()
    





