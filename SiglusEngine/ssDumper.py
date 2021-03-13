# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import struct
import unicodedata
from Decryption import Decrypt

class Header:
    headerData=b''
    headerList=[]
    length=0
    index=0
    count=0
    offset=0
    dataCount=0
    def __init__(H,f):
        f.seek(0)
        H.length=struct.unpack('I',f.read(4))[0]
        H.headerData=f.read(128)
        H.headerList=struct.unpack('32I',H.headerData)
        H.index=H.headerList[2]
        H.count=H.headerList[3]
        H.offset=H.headerList[4]
        H.dataCount=H.headerList[5]

def Check(scr):
    for char in scr:
        if unicodedata.east_asian_width(char)!='Na':
            return True
    return False

def main(argv):
    if argv.count('-a')>0:
        noDump=True
        argv.remove('-a')
    else:
        noDump=False
    if argv.count('-d')>0:
        copyLine=True
        argv.remove('-d')
    else:
        copyLine=False
    if argv.count('-x')>0:
        xlsxMode=True
        import openpyxl
        argv.remove('-x')
    else:
        xlsxMode=False
    if argv.count('-s')>0:
        singleXlsx=True
        argv.remove('-s')
    else:
        singleXlsx=False
    
    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene\> [Text\] [-a] [-c] [-x] [-s]")
        return False

    inF=argv[1]+"\\"
    if len(argv)<3 or argv[2]=='':
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[1][argv[1].rfind("\\")+1:]+"_out\\"
    else:
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[2]+"\\"

    if not singleXlsx and not os.path.exists(outF):
        os.makedirs(outF)
    if xlsxMode and singleXlsx:
        workBook=openpyxl.Workbook()
        outXLS=outF[:outF.rfind("\\")].replace(".xlsx","")+".xlsx"
    
    for inFN in glob.glob(inF+"*.ss"):
        print(inFN)
        if xlsxMode:
            name=inFN[inFN.rfind("\\")+1:]
            sheet=name[:31]
            if not singleXlsx:
                outXLS=outF+inFN[inFN.rfind("\\")+1:]+".xlsx"
                workBook=openpyxl.Workbook()
                workSheet=workBook.active
                workSheet.title=sheet
            else:
                workSheet=workBook.create_sheet(sheet)
            workSheet.column_dimensions['A'].width=8
            workSheet.column_dimensions['B'].width=64
            workSheet.column_dimensions['C'].width=64
            fillColor=openpyxl.styles.PatternFill(fill_type="solid", fgColor="F2F2F2")
            border=openpyxl.styles.Border(top=openpyxl.styles.Side(style='thin',color='D0D7E5'),left=openpyxl.styles.Side(style='thin',color='D0D7E5'),right=openpyxl.styles.Side(style='thin',color='D0D7E5'))
            if name!=sheet:
                tempName=name
            else:
                tempName=""
            workSheet.append(["Index","Text","Translation",tempName])
        else:
            outFN=outF+inFN[inFN.rfind("\\")+1:]+".txt"
            output=open(outFN,'w',1,"UTF-8")
        
        size=os.path.getsize(inFN)
        file=open(inFN,'rb')
        header=Header(file)
        file.seek(header.index)
        offset=[]
        length=[]
        for n in range(0,header.count):
            offset.append(struct.unpack('I',file.read(4))[0])
            length.append(struct.unpack('I',file.read(4))[0])
        
        for x in range(0,header.count):
            if length[x]==0:
                continue
            file.seek(header.offset+offset[x]*2,0)
            string=file.read(length[x]*2)
            text=Decrypt(string,length[x],x).decode("UTF-16")
            if not Check(text) and not noDump:
                continue
            if xlsxMode:
                if copyLine:
                    workSheet.append([x,text,text])
                else:
                    workSheet.append([x,text])
                workSheet.cell(workSheet.max_row,3).fill=fillColor
                workSheet.cell(workSheet.max_row,3).border=border
            else:
                if copyLine:
                    outLine="○"+'%.6d'%x+"○"+text+"\n●"+'%.6d'%x+"●"+text+"\n\n"
                else:
                    outLine="○"+'%.6d'%x+"○"+text+"\n●"+'%.6d'%x+"●\n\n"
                output.write(outLine)
        file.close()
        if xlsxMode:
            textLine=workSheet.max_row
            if textLine==1 and singleXlsx:
                workBook.remove(workSheet)
            elif textLine>1 and not singleXlsx:
                workBook.save(outXLS)
        else:
            output.close()
            if os.path.getsize(outFN)==0:
                os.remove(outFN)
    if singleXlsx:
        print("Saving xlsx file...")
        workBook.remove(workBook['Sheet'])
        workBook.save(outXLS)
    return True

if __name__=="__main__":
    main(sys.argv)
