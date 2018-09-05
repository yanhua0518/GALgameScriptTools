# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from io import BytesIO
import struct

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

def Transcode(uni):
    tran=''
    for ch in uni:
        try:
            ch.encode("GBK")
        except:
            tran+=u"·"
        else:
            tran+=ch
    return tran.encode("GBK")

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

def Compress(string):
    length=len(string)
    newString=b''
    for n in range(0,int(length/8)):
        newString+=b'\xff'+string[n*8:n*8+8]
    if not length%8==0:
        last=string[(n+1)*8:]
        newString+=bytes([255>>(8-length%8)])+last
    return newString


if len(sys.argv) < 2:
    print ("Usage: "+sys.argv[0]+" <dbs.out> [dbs.txt]")
    quit()
elif len(sys.argv) >2:
    txtFN=sys.argv[2]
else:
    txtFN=sys.argv[1].replace('.out','.txt')
inFN=sys.argv[1]
if inFN[-8:]!='.dbs.out':
    print("Input file MUST be *.dbs.out")
    quit()
outFN=sys.argv[1].replace('.out','.new')
try:
    f=open(inFN,'rb')
    f.read()
    f.close()
except:
    print("Input file error!")
    quit()
try:
    f=open(txtFN,'r',1,'UTF-16')
    f.read()
    f.close()
except:
    print("Text file error!")
    quit()


txt=open(txtFN,'r',1,'UTF-16')
head=txt.readline()
if head=='ASCII\n':
    isUTF=False
elif head=='Unicode\n':
    isUTF=True
else:
    print("Text error!")
    txt.close()
    quit()

file=open(inFN,'rb')
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

index=0
correctIndex=0
count=0
for line in txt.readlines():
    if line=='':
        break
    if line[0]=='[':
        index=int(line[1:line.find(']',1)])
        try:
            correctIndex=lineIndex.index(index)
        except:
            continue
    elif line[0]=='<':
        count=int(line[1:line.find('>',1)])        
        lineData[correctIndex][count]=int(line[line.find('>',1)+1:])
    elif line[0]=='●':
        count=int(line[1:line.find('●',1)])
        lineData[correctIndex][count]=line[line.find('●',1)+1:].replace('\n','')

txt.close()
    
dbs=BytesIO()
dbs.write(bytes(4))
dbs.write(header.headerData)
dbs.write(struct.pack('%di'%header.lineCount,*lineIndex))
for n in range(0,header.dataCount):
    dbs.write(struct.pack('2I',dataIndex[n],dataType[n]))
textData=b''
textOffset=0
for m in range(0,header.lineCount):
    for n in range(0,header.dataCount):
        if dataType[n]==0x53:
            if isUTF:
                tempString=lineData[m][n].encode("UTF-16")[2:]+b'\x00\x00'
            else:
                tempString=Transcode(lineData[m][n])+b'\x00'
            dbs.write(struct.pack('I',textOffset))
            textData+=tempString
            textOffset+=len(tempString)
        else:
            dbs.write(struct.pack('I',lineData[m][n]))
'''
if dbs.tell()!=header.textOffset:
    tempOffset=dbs.tell()
    dbs.seek(24)
    dbs.write(struct.pack('I',tempOffset))
    dbs.seek(0,2)
'''
dbs.write(textData)
dbsSize=dbs.tell()
dbs.seek(0)
dbs.write(struct.pack('I',dbsSize))
dbs.seek(0,2)
dbs.write(dummy)
dbsSize=dbs.tell()
dataB=Decrypt2(dbs.getvalue())
'''
dbsFile=open(outFN.replace('.new','.ori'),'wb')
dbsFile.write(dbs.getvalue())
dbsFile.close()
'''
dbs.close()
#No compression yet, this is fake.
dataSize=dbsSize+int(dbsSize/8)+8
if not dbsSize%8==0:
    dataSize+=1
dataA=struct.pack('2I',dataSize,dbsSize)
dataA+=Compress(dataB)
data=Decrypt1(dataA)

output=open(outFN,'wb')
if isUTF:
    output.write(b'\x01\x00\x00\x00')
else:
    output.write(b'\x00\x00\x00\x00')
output.write(data)
output.close()



