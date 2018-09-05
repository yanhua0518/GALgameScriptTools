# SiglusEngie Tools

主体照着number201724的代码抄来的，解压代码抄的Xmoe的

Scene改用外挂C++来处理，速度得到了飞跃性的提升

Compression是Xmoe的压缩工具，直接借来用了，-c调用，否则使用伪压缩。

ss和dbs文件小没啥影响，就不改了

Dumper进行了文本过滤，过滤掉了纯英文的行，
dbsDecrypt过滤掉了空行和数字

***
## Usage:
```
SceneUnpacker.py <Scene.pck> [Scene\]
ScenePacker.py <Scene.pck> <Scene\> [Scene.pck2] [-c]
ssDumper.py <Scene\> [text\]
ssPacker.py <Scene\> <text\> [output\]
dbsDecrypt.py <dbs file>
dbsEncrypt.py <dbs.out> [dbs.txt]
```
