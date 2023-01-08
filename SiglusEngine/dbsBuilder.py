# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import struct
import openpyxl
from io import BytesIO
from Decryption import Decrypt5,Decrypt3,FakeCompress,Compress
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
'''
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
    if argv.count('-u')>0:
        isUTF=True
        argv.remove('-u')
    else:
        isUTF=False
    
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
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <xlsx folder\> [output folder\] [-u] [-c [2~17]/-f]")
        return False

    inF=argv[1]+'\\'
    if len(argv)<3 or argv[2]=='':
        outF=argv[1]+"_dbs\\"
    else:
        outF=argv[2]+"\\"
    if not os.path.exists(outF):
        os.makedirs(outF)
    countError=0
    for inFN in glob.glob(inF+"*.xlsx"):
        print(inFN)
        outFN=outF+inFN[inFN.rfind("\\")+1:].replace('.xlsx','.dbs').replace('.dbs.dbs','.dbs')
        try:
            workBook=openpyxl.load_workbook(inFN)
        except:
            print("Input file error!")
            countError+=1
            continue
        workSheet=workBook.active
        for cell in workSheet['A']:
            if cell.value=="#DATANO":
                dataIndexRow=cell.row
            elif cell.value=="#DATATYPE":
                dataTypeRow=cell.row
        if not dataIndexRow or not dataTypeRow:
            print("Data format error!")
            continue
        dataIndex=[]
        dataIndexColumn=[]
        dataType=[]
        dataTypeColumn=[]
        for indexCell,typeCell in zip(workSheet[dataIndexRow],workSheet[dataTypeRow]):
            try:
                tempIndex=int(indexCell.value)
            except:
                continue
            if typeCell.value=="S" or typeCell.value=="V":
                dataIndex.append(tempIndex)
                dataIndexColumn.append(indexCell.column)
                if typeCell.value=="S":
                    dataType.append(0x53)
                else:
                    dataType.append(0x56)
                dataTypeColumn.append(typeCell.value)
        if not dataIndex:
            print("Data format error!")
            continue

        lineIndex=[]
        lineIndexRow=[]
        for indexCell in workSheet['A'][dataTypeRow:]:
            try:
                tempIndex=int(indexCell.value)
            except:
                continue
            lineIndex.append(tempIndex)
            lineIndexRow.append(indexCell.row)
        if not lineIndex:
            print("Data format error!")
            continue
        
        lineIndexOffset=0x1C
        dataCount=len(dataIndex)
        lineCount=len(lineIndex)
        dataFormatOffset=lineIndexOffset+lineCount*4
        lineDataIndexOffset=dataFormatOffset+dataCount*8
        textOffset=lineDataIndexOffset+lineCount*dataCount*4

        lineData=[]
        for l in range(lineCount):
            tempLine=[]
            for d in range(dataCount):
                tempData=workSheet.cell(row=lineIndexRow[l],column=dataIndexColumn[d]).value
                if dataType[d]==0x56:
                    try:
                        int(tempData)
                    except:
                        tempData=0
                    else:
                        tempData=int(tempData)
                else:
                    if tempData==None:
                        tempData=''
                tempLine.append(tempData)
            lineData.append(tempLine)


        if lineCount>100:
            print('Formating...')
        dbs=BytesIO()
        dbs.write(bytes(4))
        dbs.write(struct.pack('2I',lineCount,dataCount))
        dbs.write(struct.pack('2I',lineIndexOffset,dataFormatOffset))
        dbs.write(struct.pack('2I',lineDataIndexOffset,textOffset))
        dbs.write(struct.pack('%di'%lineCount,*lineIndex))
        for n in range(0,dataCount):
            dbs.write(struct.pack('2I',dataIndex[n],dataType[n]))
        textData=b''
        textOffset=0
        for m in range(0,lineCount):
            for n in range(0,dataCount):
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
        dbs.write(textData)
        dbsSize=dbs.tell()
        dbs.seek(0)
        dbs.write(struct.pack('I',dbsSize))
        dbs.seek(0,2)
        dbs.write(bytes(64-dbsSize%64))
        dbsSize=dbs.tell()
        '''
        dbsFile=open(outFN+'.ori','wb')
        dbsFile.write(dbs.getvalue())
        dbsFile.close()
        '''
        if lineCount>100:
            print('Compressing...')
        dataB=Decrypt3(dbs.getvalue())
        dbs.close()
        if comp:
            dataA=Compress(dataB,comp)
        else:
            dataA=FakeCompress(dataB)
        '''
        dbsFile=open(outFN+'.cmp','wb')
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
            if lineCount>100:
                print("Done!")
        except Exception as e:
            return e
    return True
if __name__=="__main__":
    main(sys.argv)
