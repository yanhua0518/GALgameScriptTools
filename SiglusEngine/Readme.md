# SiglusEngie Tools
## 功能说明
### Decryption Key
解包、封包Scene.pck和Gameexe.dat时所需的秘钥。格式为16进制逗号分割。  
下拉选项选择第一项时，解包、封包Scene.pck会尝试自动搜索秘钥。  
存在KeyList.txt时可以在下拉选项中选择已知的秘钥。  
### Find Key
用于通过启动游戏搜索秘钥。未找到skf.exe时不会出现。  
启动游戏后，点击Find Key，等待一段时间以后会提示是否找到秘钥。  
找到的秘钥会保存在Last use。  
### Unpack Scene
解包Scene.pck文件。  
勾选Find key only后点start可以只搜索秘钥并保存在Last use。  
### Pack Scene
把ss文件打包进Scene.pck文件。  
Compression Level为压缩等级，范围2-17，实际使用中速度差别不大，推荐17。输入0则使用伪压缩（文件会比压缩前更大）。  
### Decrypt Gameexe
解密Gameexe.dat文件。  
### Encrypt Gameexe
封装Gameexe.dat文件。  
勾选Double Encryption后秘钥才会生效，经过测试，基本无勾选必要。  
### Dump ss
从ss文件中导出文本。  
Copy text：复制文本到译文行。  
Export as xlsx：导出为Excel文件。  
Use single xlsx：将所有文本导出到一个Excel文件中。  
Count words：导出为单个Excel文件时，添加一个字数统计表格。
No dump：不过滤任何文本。  
Smart dump：只过滤掉纯英文的行。  
Full dump：过滤掉所有包含英文的行。  
### Pack ss
将译文导入回ss文件中。  
Have Excel text：从Excel文件导入时需勾选此项。  
无论是否勾选都查找文本文档进行导入，两种文件都有时，Excel的文本会覆盖文本文档的文本。  
Bilingual display：双语显示。仅导入Excel文件时可选，仅手机版可以生效双行显示。  
Change quotation marks：把对话的日文引号替换为中文习惯。  
### Dump dbs
导出dbs文件中的数据。  
Export all data：不进行内容过滤。  
Export as xlsx：导出所有数据到Excel文件，表格格式兼容官方CSV2DBS.exe。  
### Pack dbs
从文本文档导入数据回dbs文件。  
### Create dbs
将Excel文件转为dbs文件。推荐使用Unicode编码，但部分特殊文件可能无法识别。  
### Unpack pck / Pack pck
解包、封包手机版专用的pck文件。  
### Cut OMV header
删除OMV文件的文件头，转为ogv视频文件。有透明度的OMV视频无法用普通播放器正常播放。  
### Pack OMV
未找到siglusomv.exe时不会出现。  
将ogv视频转换为OMV文件。ogv视频必须是yuv444p格式。  
***
## Command line Usage:
```
SceneUnpacker.py <Scene.pck> [Scene\] [-n] [-d] / [-f]
 -n Export ss without decompression
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

ssDumper.py <Scene\> [text\] [-d] [-a/-w] [-x [-s [-c]]]
 -d Copy text to translation line
 -a Export all text without dump
 -w Dump all text with half-width characters
 -x Save text as xlsx files
 -s Save all text in one xlsx file
 -c Add a statistics sheet in single xlsx

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

 
