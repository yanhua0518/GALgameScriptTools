# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from io import BytesIO
import struct
from Decryption import Decrypt5,Decrypt3,FakeCompress,Compress

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

def main(argv):

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

    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <dbs.out> [dbs.txt] [-c [2~17]/-f]")
        return False
    elif len(argv) >2 and argv[2]:
        txtFN=argv[2]
    else:
        txtFN=argv[1].replace('.out','.txt')
    inFN=argv[1]
    if inFN[-8:]!='.dbs.out':
        print("Input file MUST be *.dbs.out")
        return False
    outFN=argv[1].replace('.out','.new')

    try:
        f=open(inFN,'rb')
        f.read()
        f.close()
    except:
        print("Input file error!")
        return False
    try:
        f=open(txtFN,'r',1,'UTF-16')
        f.read()
        f.close()
    except:
        print("Text file error!")
        return False

    txt=open(txtFN,'r',1,'UTF-16')
    head=txt.readline()
    if head=='ASCII\n':
        isUTF=False
    elif head=='Unicode\n':
        isUTF=True
    else:
        print("Text error!")
        txt.close()
        return False

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
    #dummy=file.read()
    file.close()

    index=0
    correctIndex=0
    count=0
    correctCount=0
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
            try:
                correctCount=dataIndex.index(count)
            except:
                continue
            lineData[correctIndex][correctCount]=int(line[line.find('>',1)+1:])
        elif line[0]=='●':
            count=int(line[1:line.find('●',1)])
            try:
                correctCount=dataIndex.index(count)
            except:
                continue
            lineData[correctIndex][correctCount]=line[line.find('●',1)+1:].replace('\n','')

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
    #dbs.write(dummy)
    dbs.write(bytes(64-dbsSize%64))
    dbsSize=dbs.tell()
    '''
    dbsFile=open(outFN.replace('.new','.ori'),'wb')
    dbsFile.write(dbs.getvalue())
    dbsFile.close()
    '''
    dataB=Decrypt3(dbs.getvalue())
    dbs.close()
    if comp:
        dataA=Compress(dataB,comp)
    else:
        dataA=FakeCompress(dataB)
    '''
    dbsFile=open(outFN.replace('.new','.cmp'),'wb')
    dbsFile.write(dataA)
    dbsFile.close()
    '''
    data=Decrypt5(dataA)
    try:
        output=open(outFN,'wb')
        if isUTF:
            output.write(b'\x01\x00\x00\x00')
        else:
            output.write(b'\x00\x00\x00\x00')
        output.write(data)
        output.close()
    except Exception as e:
        return e
    return True

if __name__=="__main__":
    main(sys.argv)
