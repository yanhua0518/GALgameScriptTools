# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import openpyxl

def main(argv):
    
    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("/")+1:]+" <Excel folder\>")
        return False

    inF=argv[1]+"/"
    outXLS=argv[0][:argv[0].rfind("/")+1]+argv[1]+".xlsx"
    mixBook=openpyxl.Workbook()
    mixBook.remove(mixBook.active)
    for inFN in glob.glob(inF+"*.xlsx"):
        print(inFN)
        workBook=openpyxl.load_workbook(inFN)
        for sheet in workBook:
            workSheet=mixBook.create_sheet(sheet.title)
            for i,row in enumerate(sheet.iter_rows()):
                for j,cell in enumerate(row):
                    workSheet.cell(row=i+1,column=j+1,value=cell.value)
    moxBook.save(outXLS)
    return True

if __name__=="__main__":
    main(sys.argv)
