# SiglusEngie Tools
## 功能说明
### Decryption Key
解包、封包`Scene.pck`和`Gameexe.dat`时所需的秘钥。格式为16进制逗号分割。  
- 下拉选项选择第一项时，解包、封包`Scene.pck`会尝试自动搜索秘钥。  
- 存在`KeyList.txt`时可以在下拉选项中选择已知的秘钥。  
### Find Key
用于通过启动游戏搜索秘钥。
- 未找到`skf.exe`时不会出现。  
- 启动游戏后，点击`Find Key`，等待一段时间以后会提示是否找到秘钥。  
- 找到的秘钥会保存在`Last use`。  
### Unpack Scene
解包`Scene.pck`文件。  
- 勾选`Find key only`后点`start`可以只搜索秘钥并保存在`Last use`。  
### Pack Scene
把`ss`文件打包进`Scene.pck`文件。  
- `Compression Level`为压缩等级，范围`2-17`，实际使用中速度差别不大，推荐`17`。输入`0`则使用伪压缩（文件会比压缩前更大）。  
### Decrypt Gameexe
解密`Gameexe.dat`文件。  
### Encrypt Gameexe
封装`Gameexe.dat`文件。  
- 勾选`Double Encryption`后秘钥才会生效，经过测试，基本无勾选必要。  
### Dump ss
从`ss`文件中导出文本。  
- Copy text：复制文本到译文行。  
- Export as xlsx：导出为`xlsx`文件。  
- Use single xlsx：将所有文本导出到一个`xlsx`文件中。  
- Count words：导出为单个`xlsx`文件时，添加一个字数统计表格。
- Special mode：从某种特殊格式的`ss`文件中导出。  
#### 过滤选项  
- No filter：不过滤任何文本。  
- Smart filter：只过滤掉只有半角字符的行。  
- Filter all：过滤掉所有包含半角字符的行。  
### Pack ss
将译文导入回ss文件中。  
- Have Excel text：从`xlsx`文件导入时需勾选此项。无论是否勾选都查找`txt`文档进行导入，两种文件都有时，`xlsx`文档导入后会覆盖`txt`文档导入的内容。  
- Bilingual display：双语显示。仅导入`xlsx`文件时可选，仅手机版可以生效双行显示。  
- Change quotation marks：把对话的日文引号替换为中文习惯。  
- Special mode：导入某种特殊格式的`ss`文件。  
### Dump dbs
导出`dbs`文件中的数据。  
- Export all data：不进行内容过滤。  
- Export as xlsx：导出所有数据到`xlsx`文件，表格格式兼容官方`CSVToDB.exe`。  
### Pack dbs
从`txt`文档导入数据回`dbs`文件。  
### Create dbs
将`xlsx`文件转为`dbs`文件。
- 推荐选择`Unicode`编码，但部分特殊文件可能无法识别。  
- 选择`ANSI`时可在下拉列表选择编码，也可以手动输入，如输入错误或留空将使用`GBK`编码。  
### Unpack pck / Pack pck
解包、封包手机版专用的`pck`文件。  
### Cut OMV header
删除`OMV`文件的文件头，转为`ogv`视频文件。  
- 有透明度的`OMV`视频无法用普通播放器正常播放。  
### Pack OMV
将`ogv`视频转换为`OMV`文件。`ogv`视频必须是`yuv444p`格式。
- 未找到`siglusomv.exe`时不会出现。    
***
# SiglusEngie Tools
## Instruction
### Decryption Key
Select secret keys for packing and unpacking `Scene.pck` and `Gameexe.dat`. The keys are comma-separated hexadecim numbers.
- The default option is to automaticly search secret keys with `Scene.pck`.
- Existing secret keys can be selected with the drop-down menu. These keys should be stored in `KeyList.txt`.
### Find Key
Search secret keys from memory when the game is running. To use this function, click the `Find Key` button after launched the game and wait for a moment.
- This function will be unavailable if `skf.exe` is not found.
- Found secret keys will be saved in `Last use`.
### Unpack Scene
Unpack the `Scene.pck` file.
- Click the `start` button with the `Find key only` box ticked to search for the secret key and save it in `Last use` only without unpacking the scene files.
### Pack Scene
Pack the `ss` file into `Scene.pck`.
- The `Compression Level` ranges from 2 to 17, 17 is recommended. Specially, Set the `Compression Level` 0 to use pseudo-compression (compressed files will be larger than original ones).
### Decrypt Gameexe
Decrypt the `Gameexe.dat` file.
### Encrypt Gameexe
Pack the `Gameexe.dat` file.
- The secret key will only applied with the `Double Encryption` box ticked. It is always not necessary to use this option.
### Dump ss
Export texts from `ss` file. The following are optional functions.
- Copy text: Copy the orignal texts to the translated part.
- Export as xlsx: Export as `xlsx` files.
- Use single xlsx: Export all the texts to one single `xlsx` file. Must use `Export as xlsx`.
- Count words: Add a word counting sheet while exporting as a single `xlsx` file. Must use `Use single xlsx`.
- Special mode: for special `ss` files.
#### Filter option:
- No filter: Do not filter any text.
- Smart filter: Filter out lines only consisting half-width characters.
- Full filter: Fillter out lines containing any half-width characters.
### Pack ss
Import the translated texts back into the `ss` file. The following are optional functions.
- Have Excel text: Tick this when importing from `xlsx` files. `txt` files will always be used regardless of using this or not. When both `txt` and `xlsx` files are found, the program will use the `xlsx` files.
- Bilingual display: Double language display. It is available with mobile version. The text should be imported from `xlsx` files.
- Change quotation marks: Replace the Japanese quotation marks in the dialogue with the Chinese quatation marks.
- Special mode: for special `ss` files.
### Dump dbs
Export data from `dbs` file. The following are optional functions.
- Export all data: Export all data without filter.
- Export as xlsx: Export all data to `xlsx` files. The table format is compatible with the official `CSVToDB.exe`.
### Pack dbs
Import data from `txt` files back to `dbs` files.
### Create dbs
Converts `xlsx` files to `dbs` files.
- Unicode encoding is recommended, but some special files may not be recognized.
- 
### Unpack pck / Pack pck
Unpack or pack the `pck` file used for the mobile version.
### Cut OMV header
Remove the file header of the `OMV` file and convert it to `ogv` video format.
- `OMV` videos with transparency cannot be played with ordinary players.
### Pack OMV
Convert `ogv` video to `OMV` file. `ogv` video must be in `yuv444p` format.
- This option will not appear when `siglusomv.exe` is not found.
***
## Command line Usage:
```
SceneUnpacker.py <Scene.pck> [Scene\] [-n] [-d] / [-f] / [-x]
 -n Export ss without decompression
 -d Use default key
 -f Find key only
 -x Remove original source

ScenePacker.py <Scene.pck> <Scene\> [Scene.pck2] [-c [2~17]/-f] [-d]
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression
 -d Use default key

GameexeUnpacker.py <Gameexe.dat> [Gameexe.ini]

GameexePacker.py <Gameexe.ini> [Gameexe.dat2] [-p] [-c [2~17]/-f]
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression
 -p Double encryption

ssDumper.py <Scene\> [text\] [-o] [-d] [-a/-w] [-x [-s [-c]]]
 -o Special mode
 -d Copy text to translation line
 -a Export all text without dump
 -w Dump all text with half-width characters
 -x Save text as xlsx files
 -s Save all text in one xlsx file
 -c Add a statistics sheet in single xlsx

ssPacker.py <Scene\> <text\> [output\] [-o] [-x [-b]] [-q]
 -o Special mode
 -x Import from xlsx file (Always import from txt files first)
 -b Import both orignal text and translated text (Bilingual display only effect in mobile version)
 -q Change quotation marks from Japanese custom to Chinese custom

dbsDecrypt.py <dbs file> [-a/-x]
 -a Export all data without dump
 -x Save all data as xlsx file （Compatible with official CSV2DBS.exe if save as csv file)
 
dbsEncrypt.py <dbs.out> [dbs.txt] [-c [2~17]/-f]
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression
 
dbsBuilder.py <xlsx folder\> [dbs folder\] [-e [text coding]] [-c [2~17]/-f]
 -e Encrypt dbs file with typed text coding (Default is unicode, use GBK if only input -e)
 -c 2~17 Compression level (Default level 2, level 17 if only input -c)
 -f Do fake compression

pckUnpacker.py <pck file> [output folder\]
pckPacker.py <data folder\> [output file]

omvCuter.py <omv file> [output file]

siglusomv.exe <ogv file(must be YUV444p)> <omv file>

skf.exe (Just run it and start the game)
```
