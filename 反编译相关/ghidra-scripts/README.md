# Ghidra 辅助脚本

配合 [反编译相关](../README.md) 里的 `nxu8` 处理器模块使用。把本目录加到 `analyzeHeadless` 的
`-scriptPath`，或直接抄到 `<Ghidra>/Ghidra/Features/Base/ghidra_scripts`。

| 脚本 | 用途 |
| --- | --- |
| `DisAll.java` | **前置脚本**。把整片 ROM 反汇编出来。裸二进制导入后没有任何入口点，不跑这一步自动分析会得到 0 个函数 |
| `ExportAll.java` | **后置脚本**。调用 `CppExporter` 导出反编译 C 代码、`AsciiExporter` 导出 Listing 文本 |
| `Dump.java` | 小工具。打印开头 12 条指令与 `_start` 附近 8 条，用于验证语言是否正常加载 |

## 生成 VerF 的反编译结果

```bat
set JAVA_HOME=<JDK 25 目录>
analyzeHeadless <项目目录> VerF ^
  -import ROM\fx991cnx-vF\rom.bin ^
  -processor nX-U8:LE:16:Casio ^
  -loader BinaryLoader -loader-baseAddr 0x0 ^
  -analysisTimeoutPerFile 1800 ^
  -scriptPath <本目录> ^
  -preScript DisAll.java ^
  -postScript ExportAll.java <输出路径前缀> ^
  -deleteProject
```

`ExportAll.java` 的参数是输出路径前缀，会生成 `<前缀>.c` 和 `<前缀>.txt`。

## 只做快速自检

```bat
analyzeHeadless <项目目录> T -import rom.bin -processor nX-U8:LE:16:Casio ^
  -loader BinaryLoader -loader-baseAddr 0x0 ^
  -scriptPath <本目录> -postScript Dump.java -noanalysis -deleteProject
```

正常时会输出 `language = nX-U8:LE:16:Casio`，以及 `000000 4 B 0x00946a` 这样的指令行。
