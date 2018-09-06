# SiglusEngie Tools

主体照着number201724的代码抄来的，压缩函数参照了Xmoe的代码。

搜索Key和处理Gameexe别处有现成的工具很方便，不写了（搜索Key我也写不出来……）。

处理Scene需要把py里面的key改成目标游戏的Key，默认的是“神待ちサナちゃん　DL版”。

外挂了C++来处理，速度得到了飞跃性的提升（谜之声：那干嘛不直接用C写？——别闹，py才是灵魂啊！）

Packer用-c调用压缩函数，压缩等级2-17，默认为最高17（因为实际上速度差不了多一点）。不加-c使用伪压缩。

ss和dbs文件小对速度没啥影响，就不改了。

Dumper进行了文本过滤，过滤掉了纯英文的行，
dbsDecrypt过滤掉了空行和数字。

***
## Usage:
```
SceneUnpacker.py <Scene.pck> [Scene\]
ScenePacker.py <Scene.pck> <Scene\> [Scene.pck2] [-c [2~17]]

ssDumper.py <Scene\> [text\]
ssPacker.py <Scene\> <text\> [output\]

dbsDecrypt.py <dbs file>
dbsEncrypt.py <dbs.out> [dbs.txt]
```
