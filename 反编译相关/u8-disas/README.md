# u8-disas

nX-U8 反汇编器，取自 [CasioEmuNeo](https://github.com/qiufuyu123/CasioEmuNeo) 的 `disas/` 目录（GPL-3.0）。

`ROM/*/_disas.txt` 就是用它生成的，而不是 Ghidra 的产物——它实现了 sleigh 里没有的 `SWI`、`RTI`、`BRK`、`CR/CXR/ELR/ECSR/EPSW` 传送、`PUSH LR, EPSW, ELR`、`DSR<-` 等指令。

## 用法

```
u8-disas.exe <rom 文件> <起始地址> <长度> <输出文件>
```

三个数字参数支持十进制（无前缀）、十六进制（`0x` 前缀）、八进制（`0` 前缀）。

例（生成 fx-991CN X 的完整反汇编）：

```
u8-disas.exe rom.bin 0 0x40000 _disas.txt
```

输出为每行一条指令，格式 `地址  字节 助记符  操作数`，**CRLF 行尾**、6 位大写十六进制地址、覆盖整个读取范围。

## 校验

用本目录的 `u8-disas.exe` 反汇编 `ROM/fx991cnx-vC/rom.bin`，结果与仓库中原有的 `_disas.txt` **逐字节相同**：

- 大小 4,850,937 字节
- SHA-256 `82897a64125dbfb963e7b14d6eab19e59fe2a1c2e7b4ca721a4cb1cc943533df`

`ROM/fx991cnx-vF/_disas.txt` 即由同一程序对 VerF 固件生成（116,944 行，SHA-256 `25059ef0a99e257175d0911e517a413e4c383c03050596983f75dfda7fddddd3`）。

## 重新构建

上游用 Makefile + g++：`make` 会先编出生成器 `bin/main`，用它把 `nX-U8_is.txt` 与 `example.cpp` 合成 `temp.cpp`，再编译成 `bin/u8-disas`。

本机没有 MinGW/make，因此用 Visual Studio 2022 的 MSVC 完成，等价步骤：

```
call "D:\VS2022\VC\Auxiliary\Build\vcvars64.bat"
cl /nologo /O2 /EHsc /std:c++14 main.cpp lib.cpp /Fe:main.exe
main.exe nX-U8_is.txt temp.cpp
cl /nologo /O2 /EHsc /std:c++14 temp.cpp /Fe:u8-disas.exe
```

注意两点：

- 上游 README 提醒 `nX-U8*.txt`、`example.cpp`、`help.txt` 的行尾必须正确（生成器是按行读入的）。
- 行尾会影响产物：Windows 下 `ofstream` 以文本模式写出 CRLF，与现有 `_disas.txt` 一致；若在 Linux 下构建会得到 LF，文件会小 117010 字节。

`example.cpp` 是反汇编器的代码模板，`main.cpp` + `lib.cpp` 是代码生成器，`nX-U8_is.txt` 是指令集描述（`_split` 版本生成带分支的变体 `u8-disas-split`）。
