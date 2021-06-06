# SiglusEngie Tools

主体照着number201724的代码抄来的，压缩函数参照了Xmoe的代码。  
otherTools里是 https://github.com/marcussacana/SiglusSceneManager 的工具，
可以直接编辑ss和dbs（不推荐）。
主要的是用它来搜索Key。  
处理Scene和Gameexe需要把Decryption.py里面的key改成目标游戏的Key，默认的是“神待ちサナちゃん　DL版”。  
外挂了C++来处理，速度得到了飞跃性的提升（谜之声：那干嘛不直接用C写？——别闹，py才是灵魂啊！）  
ScenePacker用-c调用压缩函数，压缩等级2-17，默认为最高17（因为实际上速度差不了多一点）。不加-c使用伪压缩。  
GameexePacker同样支持-c，-p控制是否二次加密（大致测试并无影响）。  
dbs也用上了C++，-c压缩参数同上。  
增加用于移动端的pck封装文件的解包封包功能。  
Dumper进行了文本过滤，过滤掉了纯英文的行，
dbsDecrypt过滤掉了空行和数字。  
整体优化了代码， 现在可以用其他py调用。
调用函数main(argv,key)或main(argv)。
输入变量都是list。key为空list时使用默认Key。  
GUI基本完善，最后一次使用的Key会储存在SiglusKey.txt里，删除该文件恢复默认Key。  
GUI增加已知Key选择功能，如果存在KeyList.txt会读取其中的Key并以下拉列表形式出现。
选择了已知Key将不会保存SiglusKey.txt。  
在GUI中集成了 https://github.com/renanc1332/SiglusTranslationToolkit 的skf用于直接搜索Key，不再需要另开程序搜索。  
注意：必须进行过解包或封包操作才会保存当前Key。所以请注意手动保存新查找到的Key。  
在GUI中集成了 https://github.com/jansonseth/Summer-Pockets-Tools 的siglusomv用于封装omv。
顺便添加了砍掉omv的文件头变成ogv的功能。  
为导出ss和dbs添加了-a命令不进行文本过滤。  
增加把ss导出为excel文件的功能。
-x命令导出xlsx，使用-s导出为单个xlsx文件。
导入ss时加-x检测xlsx文件，先导入txt后导入xlsx，所以如果同时存在将会导入xlsx文件的内容。  
导出ss添加-d命令，不加-d不会在译文行填入原文。  
增加把dbs导出为excel文件的功能。
-x命令导出xlsx。导出为excel文件不会进行文本过滤，无需和-a同时使用。  
导出的excel文件转换为csv后兼容官方dbs封装工具。  
dbsEncrypt不能xlsx格式导入dbs文件。
需要使用dbsBuilder进行封装。  
dbsBuilder封装建议一定要加-u命令封装为Unicode编码。ANSI编码仅支持简体中文。
另外，同样有-c压缩参数。  
现在支持拖拽文件了！  
搜索Key大概不会再报错了……
另外顺便给导出Excel格式的文本加了表格背景色，便于批量替换。  
又加了点没什么用的功能。
***
## Usage:
```
SceneUnpacker.py <Scene.pck> [Scene\]
ScenePacker.py <Scene.pck> <Scene\> [Scene.pck2] [-c [2~17]]

GameexeUnpacker.py <Gameexe.dat> [Gameexe.ini]
GameexePacker.py <Gameexe.ini> [Gameexe.dat2] [-p] [-c [2~17]]

ssDumper.py <Scene\> [text\] [-a/-w] [-d] [-x [-s]]
ssPacker.py <Scene\> <text\> [output\] [-x [-db]] [-q]

dbsDecrypt.py <dbs file> [-a/-x]
dbsEncrypt.py <dbs.out> [dbs.txt] [-c [2~17]]
dbsBuilder.py <xlsx folder\> [dbs folder\] [-u] [-c [2~17]]

pckUnpacker.py <pck file> [output folder\]
pckPacker.py <data folder\> [output file]

omvCuter.py <omv file> [output file]

siglusomv.exe <ogv file(must be YUV444p)> <omv file>

skf.exe (Just run it and start the game)
```
