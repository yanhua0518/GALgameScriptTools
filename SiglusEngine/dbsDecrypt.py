# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
from io import BytesIO
from Decryption import Decrypt5,Decrypt3,Decompress

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
        
def main(argv):
    if argv.count('-a')>0:
        noDump=True
        argv.remove('-a')
    else:
        noDump=False
    if argv.count('-x')>0:
        xlsxMode=True
        import openpyxl
        argv.remove('-x')
    else:
        xlsxMode=False

    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <dbs file> [-a/-x]")
        return False

    try:
        f=open(argv[1],'rb')
        f.read()
        f.close()
    except:
        return False
    
    dbs=open(argv[1],'rb')
    head=dbs.read(4)
    if head==b'\x00\x00\x00\x00':
        isUTF=False
    else:
        isUTF=True
    data=dbs.read()
    dbs.close()
    dataA=Decrypt5(data)
    '''
    output=open(argv[1]+'.dec','wb')
    output.write(dataA)
    output.close()
    '''
    compSize,decompSize=struct.unpack('2I',dataA[:8])
    dataB=Decompress(dataA[8:],decompSize)
    dataC=Decrypt3(dataB)
    
    if xlsxMode:
        file=BytesIO(dataC)
    else:
        try:
            output=open(argv[1]+'.out','wb')
            output.write(dataC)
            output.close()
            file=open(argv[1]+'.out','rb')
        except Exception as e:
            return e

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
    
    if xlsxMode:
        xls=argv[1]+".xlsx"
        workBook=openpyxl.Workbook()
        workSheet=workBook.active
        workSheet.title="Translation"
        workSheet.column_dimensions['A'].width=10
        tempIndex=["#DATANO"]
        tempType=["#DATATYPE"]
        for i,j in zip(dataIndex,dataType):
            tempIndex.append(i)
            if j==0x53:
                tempType.append("S")
            else:
                tempType.append("V")
        workSheet.append(tempIndex)
        workSheet.append(tempType)
        for l in range(0,header.lineCount):
            tempLine=[lineIndex[l],*lineData[l]]
            workSheet.append(tempLine)
        workSheetCopy=workBook.copy_worksheet(workSheet)
        workSheetCopy.title="Text"
        try:
            workBook.save(xls)
        except Exception as e:
            return e
    else:
        try:
            txt=open(argv[1]+'.txt','w',1,"UTF-16")
        except Exception as e:
            return e
        if isUTF:
            txt.write('Unicode\n')
        else:
            txt.write('ASCII\n')
        for m in range(0,header.lineCount):
            txt.write('[%.4d]\n'%lineIndex[m])
            for n in range(0,header.dataCount):
                tempIndex=dataIndex[n]
                tempData=lineData[m][n]
                if dataType[n]==0x53 and (tempData!='' or noDump):
                    txt.write('○%.2d○'%tempIndex+tempData+'\n●%.2d●'%tempIndex+lineData[m][n]+'\n\n')
                
                #int data:
                elif dataType[n]==0x56 and noDump:
                    txt.write('{%.2d}'%tempIndex+str(tempData)+'\n<%.2d>'%tempIndex+str(tempData)+'\n\n')
                
            txt.write('\n')
        txt.close()
        
    return True
        
if __name__=="__main__":
    main(sys.argv)
