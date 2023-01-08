# SiglusEngie Tools
***
## Command line Usage:
```
SceneUnpacker.py <Scene.pck> [Scene\] [-n] [-d] / [-f]
 -n Export ss without decompress
 -d Use default key
 -f Find key only

ScenePacker.py <Scene.pck> <Scene\> [Scene.pck2] [-c [2~17]/-f] [-d]
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression
 -d Use default key

GameexeUnpacker.py <Gameexe.dat> [Gameexe.ini]

GameexePacker.py <Gameexe.ini> [Gameexe.dat2] [-p] [-c [2~17]/-f]
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression
 -p Double encryption

ssDumper.py <Scene\> [text\] [-d] [-a/-w] [-x [-s]]
 -d Copy text to translation line
 -a Export all text without dump
 -w Dump all text with half-width characters
 -x Save text as xlsx files
 -s Save all text in one xlsx file

ssPacker.py <Scene\> <text\> [output\] [-x [-b]] [-q]
 -x Import from xlsx file (Always import from txt files first)
 -b Import both orignal text and translated text (Bilingual display only effect in mobile version)
 -q Change quotation marks from Japanese custom to Chinese custom

dbsDecrypt.py <dbs file> [-a/-x]
 -a Export all data without dump
 -x Save all data as xlsx file （Compatible with official CSV2DBS.exe if save as csv file)
 
dbsEncrypt.py <dbs.out> [dbs.txt] [-c [2~17]/-f]
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression
 
dbsBuilder.py <xlsx folder\> [dbs folder\] [-u] [-c [2~17]/-f]
 -u Encrypt dbs file with Unicode (Default is GBK)
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression

pckUnpacker.py <pck file> [output folder\]
pckPacker.py <data folder\> [output file]

omvCuter.py <omv file> [output file]

siglusomv.exe <ogv file(must be YUV444p)> <omv file>

skf.exe (Just run it and start the game)
```

 
