# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import glob
import struct
import unicodedata
import openpyxl
from Decryption import Decrypt

class ss:

    def __init__(H,fn):
        H.fileSize=os.path.getsize(fn)
        f=open(fn,'rb')
        H.headerLength=struct.unpack('I',f.read(4))[0]
        H.headerData=f.read(128)
        H.headerList=list(struct.unpack('32I',H.headerData))
        H.unknownOffset=H.headerList[0]
        H.unknownLength=H.headerList[1]
        H.index=H.headerList[2]
        H.count=H.headerList[3]
        H.dataOffset=H.headerList[4]
        H.dataCount=H.headerList[5]
        f.seek(H.index)
        H.offset=[]
        H.length=[]
        for n in range(0,H.count):
            H.offset.append(struct.unpack('I',f.read(4))[0])
            H.length.append(struct.unpack('I',f.read(4))[0])
        H.string=[]
        for x in range(0,H.count):
            if H.length[x]==0:
                H.string.append(b'')
                continue
            f.seek(H.dataOffset+H.offset[x]*2,0)
            H.string.append(f.read(H.length[x]*2))
        f.seek(H.unknownOffset)
        H.ssData=f.read()
        f.close()

    def write(H,fn):
        f=open(fn,'wb')
        f.write(struct.pack("I",H.headerLength))
        f.write(bytes(128))
        newOffset=0
        for n in range(0,H.count):
            f.write(struct.pack("I",newOffset))
            f.write(struct.pack("I",H.length[n]))
            newOffset+=H.length[n]
        offsetDev=H.unknownOffset-f.tell()
        f.write(H.ssData)
        for x in range(0,H.count):
            f.write(H.string[x])
        H.headerList[0]=H.unknownOffset-offsetDev
        H.headerList[4]=H.fileSize-offsetDev
        for i in range(6,32,2):
            H.headerList[i]=H.headerList[i]-offsetDev
        f.seek(4)
        f.write(struct.pack("32I",*H.headerList))
        f.close()

class ssOrg:
    def __init__(ss,fn):
        ss.lines=[]
        try:
            f=open(fn,'r',1,'UTF-8')
            ss.lines=f.readlines()
            f.close()
        except UnicodeDecodeError:
            try:
                f=open(fn,'r',1,"SHIFT-JIS")
                ss.lines=f.readlines()
                f.close()
            except:
                ss.lines=[]
        except Exception as e:
            ss.lines=[]
            
    def write(ss,fn):
        f=open(fn,'w',1,"UTF-8")
        for line in ss.lines:
            f.write(line)
        f.close()

def softIndex(i):
    l=i//1000000
    s=i%1000000//1000
    e=i%1000
    return l,s,e

def change(text):
    if len(text)<1:
        return text
    temp=text.replace('「','“').replace('」','”').replace("『","‘").replace("』","’")[::-1]
    if len(text)<2:
        return temp[::-1]
    if (temp[0]=="”" or temp[0]=="’" or temp[0]=="）") and temp[1]!="，" and temp[1]!="。" and temp[1]!="？" and temp[1]!="！" and temp[1]!="～" and temp[1]!="—" and temp[1]!="…" and temp[1]!=" ":
        temp=temp[0].replace("”","”。").replace("’","’。").replace("）","）。")+temp[1:]
    return temp[::-1]


def main(argv):
    
    def offPack(countError):
        for txtFN in glob.glob(txtF+"*.txt"):
            print(txtFN)
            inFN=inF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
            outFN=outF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
            SS=ssOrg(inFN)
            if not SS.lines:
                print("Input file error!")
                countError+=1
                continue
            try:
                txt=open(txtFN,'r',1,"UTF-8")
            except:
                print("Input file error!")
                countError+=1
                continue
            lastL=-1
            offset=0
            for line in txt.readlines():
                if not line[0]==u"●":
                    continue
                index=int(line[1:line.find("●",1)])
                l,s,e=softIndex(index)
                if l==lastL:
                    s+=offset
                    e+=offset
                else:
                    offset=0
                text=line[line.find("●",1)+1:].replace("\n","")
                if quotChange:
                    text=change(text)
                SS.lines[l]=SS.lines[l][:s]+text+SS.lines[l][e+1:]
                lastL=l
                offset+=len(text)-len(SS.lines[l][s:e+1])
            txt.close()
            try:
                SS.write(outFN)
            except Exception as e:
                countError+=1
                print("Output file error!\n"+str(e))

        if xlsxMode:
            for txtFN in glob.glob(txtF+"*.xlsx"):
                print(txtFN)
                try:
                    workBook=openpyxl.load_workbook(txtFN)
                except Exception as e:
                    countError+=1
                    print("Input file error!\n"+str(e))
                    continue
                for sheet in workBook:
                    name=sheet['D1'].value
                    if name==None or name=="" or len(sheet.title)<31:
                        name=sheet.title
                    print(name)
                    inFN=inF+name
                    outFN=outF+name
                    SS=ssOrg(inFN)
                    if not SS.lines:
                        print("Input file error!")
                        countError+=1
                        continue
                    try:
                        txt=open(txtFN,'r',1,"UTF-8")
                    except:
                        print("Input file error!")
                        countError+=1
                        continue
                    lastL=-1
                    offset=0
                    for a,b,c in zip(sheet['A'],sheet['B'],sheet['C']):
                        try:
                            index=int(a.value)
                        except:
                            continue
                        l,s,e=softIndex(index)
                        if l==lastL:
                            s+=offset
                            e+=offset
                        else:
                            offset=0
                        text=c.value
                        if text==None:
                            text=""
                        else:
                            text=str(text)
                        jp=str(b.value)
                        if dbLine and jp!=text and (len(text)>2 or len(jp)>2):
                            if quotChange:
                                text=change(text)+'#NEWLINE'+jp
                            else:
                                text=text+'#NEWLINE'+jp
                        elif quotChange:
                            text=change(text)
                        SS.lines[l]=SS.lines[l][:s]+text+SS.lines[l][e+1:]
                        lastL=l
                        offset+=len(text)-len(SS.lines[l][s:e+1])
                    try:
                        SS.write(outFN)
                    except Exception as e:
                        countError+=1
                        print("Output file error!\n"+str(e))
        return countError
    
    def orgPack(countError):
        for txtFN in glob.glob(txtF+"*.txt"):
            print(txtFN)
            inFN=inF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
            outFN=outF+txtFN[txtFN.rfind("\\")+1:].replace(".txt",".ss").replace(".ss.ss",".ss")
            try:
                SS=ss(inFN)
            except:
                print("ss file not found!")
                countError+=1
                continue
            try:
                txt=open(txtFN,'r',1,"UTF-8")
            except:
                print("Input file error!")
                countError+=1
                continue
            for line in txt.readlines():
                if not line[0]==u"●":
                    continue
                index=int(line[1:line.find("●",1)])
                text=line[line.find("●",1)+1:].replace("\n","")
                if quotChange:
                    text=change(text)
                SS.length[index]=len(text)
                SS.string[index]=Decrypt(text.encode("UTF-16")[2:],SS.length[index],index)
            txt.close()
            try:
                SS.write(outFN)
            except:
                countError+=1
                print("Output file error!")

        if xlsxMode:
            for txtFN in glob.glob(txtF+"*.xlsx"):
                print(txtFN)
                try:
                    workBook=openpyxl.load_workbook(txtFN)
                except Exception as e:
                    countError+=1
                    print("Input file error!\n"+str(e))
                    continue
                for sheet in workBook:
                    name=sheet['D1'].value
                    if name==None or name=="" or len(sheet.title)<31:
                        name=sheet.title
                    print(name)
                    inFN=inF+name
                    outFN=outF+name
                    try:
                        SS=ss(inFN)
                    except:
                        countError+=1
                        print("ss file not found!")
                        continue
                    for a,b,c in zip(sheet['A'],sheet['B'],sheet['C']):
                        try:
                            index=int(a.value)
                        except:
                            continue
                        text=c.value
                        if text==None:
                            text=""
                        else:
                            text=str(text)
                        jp=str(b.value)
                        if dbLine and jp!=text and (len(text)>2 or len(jp)>2):
                            if quotChange:
                                text=change(text)+'#NEWLINE'+jp
                            else:
                                text=text+'#NEWLINE'+jp
                        elif quotChange:
                            text=change(text)
                            
                        SS.length[index]=len(text)
                        SS.string[index]=Decrypt(text.encode("UTF-16")[2:],SS.length[index],index)
                    try:
                        SS.write(outFN)
                    except:
                        countError+=1
                        print("Output file error!")
        return countError
    
    if argv.count('-b')>0:
        dbLine=True
        argv.remove('-b')
    else:
        dbLine=False
    if argv.count('-q')>0:
        quotChange=True
        argv.remove('-q')
    else:
        quotChange=False
    if argv.count('-x')>0:
        xlsxMode=True
        argv.remove('-x')
    else:
        xlsxMode=False
    if argv.count('-o')>0:
        offMode=True
        argv.remove('-o')
        '''
        LINE=1000000
        CHAR=1000
        END=1
        '''
    else:
        offMode=False
    countError=0
    inF=argv[1]+"\\"
    txtF=argv[2]+"\\"
    if len(argv)<4 or argv[3]=='':
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[1][argv[1].rfind("\\")+1:]+"_packed\\"
    else:
        outF=argv[0][:argv[0].rfind("\\")+1]+argv[3]+"\\"
    if not os.path.exists(outF):
        os.makedirs(outF)
    if len(argv)<3 or argv[1]=='' or argv[2]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <Scene\> <Text\> [Scene_packed\] [-o] [-x [-b]] [-q]")
        return False
    if offMode:
        countError=offPack(countError)
    else:
        countError=orgPack(countError)
    if countError:
        return countError
    else:
        return True

if __name__=="__main__":
    main(sys.argv)
    
