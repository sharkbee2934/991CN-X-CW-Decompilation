# 反编译结果

按固件版本分目录存放 Ghidra 的两种导出：Listing ASCII 文本（`.txt`）与反编译 C 代码（`.c`）。

| 目录 | 文件 | 大小 |
| --- | --- | --- |
| `VerC/` | `991CN X.c` | 1,521,236 |
| `VerC/` | `991CN X.txt` | 15,591,206 |
| `VerF/` | `991CN X VerF.c` | 1,353,866 |
| `VerF/` | `991CN X VerF.txt` | 15,408,054 |

## VerC/

上游 [991CN-X-CW-Decompilation](https://github.com/Physics365/991CN-X-CW-Decompilation) 仓库提供的成品，所用 Ghidra 版本未记录。

## VerF/

本仓库用 Ghidra 12.2 + `nxu8` 处理器模块自行生成。ROM：`ROM/fx991cnx-vF/rom.bin`。

```bat
analyzeHeadless <项目目录> VerF ^
  -import ROM\fx991cnx-vF\rom.bin ^
  -processor nX-U8:LE:16:Casio ^
  -loader BinaryLoader -loader-baseAddr 0x0 ^
  -analysisTimeoutPerFile 1800 ^
  -scriptPath <反编译相关目录>\ghidra-scripts ^
  -preScript DisAll.java ^
  -postScript ExportAll.java <输出路径前缀> ^
  -deleteProject
```

前置脚本 [DisAll.java](../ghidra-scripts/DisAll.java) 是必需的：裸二进制导入后没有任何入口点，
直接分析会得到 **0 个函数**；先把整片 ROM 反汇编出来，自动分析才建立函数。
导出脚本 [ExportAll.java](../ghidra-scripts/ExportAll.java) 分别调用 `CppExporter`（`.c`）与 `AsciiExporter`（`.txt`）。

本次运行统计：**74,125 条指令、1,279 个函数**，耗时约 1.4 分钟。

## 注意

- `nxu8.slaspec` 不含 `SWI`、`RTI`、`BRK`、`CR/CXR` 传送、`PUSH LR, EPSW, ELR` 等指令（可与
  `ROM/*/_disas.txt` 里 `u8-disas` 的输出对照）。遇到这些位置 Ghidra 会报
  `Unable to resolve constructor`，对应函数可能缺少分支。
- 两份 C 文件由不同 Ghidra 版本导出，开头 typedef 集合与全局变量排列略有差异，属正常。
- `.txt` 是 Ghidra 的 Listing ASCII 导出（每个字节一行，`??` 表示未被识别为指令的数据），
  与 `u8-disas` 生成的 `_disas.txt` 格式不同，不要混用。
