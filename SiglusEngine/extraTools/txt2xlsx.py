# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import openpyxl


def main(argv):
    txtF='text/'
    xlsF='Excel_file/'

    if not os.path.exists(xlsF):
        os.makedirs(xlsF)
    for inFN in glob.glob(txtF+"*.txt"):
        print(inFN)
        outFN=xlsF+inFN[inFN.rfind('/'):].replace(".txt",".xlsx")
        try:
            txtFile=open(inFN,'r',1,"UTF-8")
            if txtFile.read(1)!="\ufeff":
                txtFile.seek(0)
        except:
            continue
        workBook=openpyxl.Workbook()
        workSheet=workBook.active
        workSheet.title=inFN[inFN.rfind('/')+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
        workSheet.append(["Index","Text","Translation"])
        workSheet.column_dimensions['A'].width=8
        workSheet.column_dimensions['B'].width=64
        workSheet.column_dimensions['C'].width=64
        index=0
        text=""
        trans=""
        for line in txtFile.readlines():
            if line[0]=="○":
                index=int(line[1:line.find("○",1)])
                text=line[line.find("○",1)+1:].replace("\n","")
            elif line[0]=="●":
                trans=line[line.find("●",1)+1:].replace("\n","")
                workSheet.append([index,text,trans])
        txtFile.close()
        workBook.save(outFN)
    return True

if __name__=="__main__":
    main(sys.argv)
