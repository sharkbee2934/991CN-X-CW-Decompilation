# 反编译相关

本目录下存储了使用 Ghidra 反编译计算器 ROM 所需的资源与工程文件，以及 nX-U8 CPU 的补充资料。

## 用 Ghidra 反编译

0. 装 **JDK 25**。Ghidra 12.2 的 `Ghidra/application.properties` 写的是 `application.java.min=25`，
   JDK 21/22 会在启动时被直接拒绝；实测 Microsoft Build of OpenJDK 25.0.1 可用。
1. 前往 [Ghidra 的发布页](https://github.com/NationalSecurityAgency/ghidra/releases)下载并解压 Ghidra；
2. 把本目录下的 `nxu8` 文件夹整个复制到 `<你的 Ghidra 目录>\Ghidra\Processors\nxu8`
   （目录布局已经按 Ghidra 要求放成 `data/languages`，不必再改）；
3. 阅读[《用 Ghidra 分析卡西欧源代码》](https://tieba.baidu.com/p/8938265174)来开始反编译之旅。

此外这里也附带了反编译所得的结果，见「反编译结果」文件夹。

## nxu8 处理器模块

`nxu8` 是 nX-U8 的 Ghidra 处理器模块，源自 <https://github.com/EwTE-H/nX-U8_for_Ghidra>（分支 `master`）。

上游那份**在新版 Ghidra 下装不进去**——会报 `Unsupported language: nxu8:LE:16:Casio`。
本仓库对上游做了三处修正，改完才能被识别：

| 问题 | 修正 |
| --- | --- |
| 缺 `Module.manifest` | 补一个 0 字节的（Ghidra 内置的 6502/68000 等模块都有） |
| 语言文件放在 `languages/` | 移到 `data/languages/`（Ghidra 只扫描这个路径） |
| `nxu8.ldefs` 里 `id="nxu8"` | 改成完整 LanguageID `id="nX-U8:LE:16:Casio"`（对照 `6502.ldefs` 的 `id="6502:LE:16:default"`） |

另外补上了编译产物 `nxu8.sla`，解压即用：

| 文件 | 字节数 | 说明 |
| --- | --- | --- |
| `Module.manifest` | 0 | 模块标记 |
| `buildLanguage.xml` | 1662 | Ant 构建脚本（源码原件） |
| `sleighArgs.txt` | 235 | sleigh 编译参数（`-u`） |
| `data/languages/nxu8.slaspec` | 19371 | 指令集描述（CRLF 行尾，源码原件） |
| `data/languages/nxu8.ldefs` | 480 | 唯一的改动是 `id` 属性 |
| `data/languages/nxu8.pspec` | 114 | 程序计数器 `_PC` |
| `data/languages/nxu8.cspec` | 1578 | 调用约定（ER0/ER2 传参、ER0 返回、`_LR` 返回地址） |
| `data/languages/nxu8.sla` | 29479 | **编译产物**，由 Ghidra 12.2 的 sleigh 编译 |

`nxu8.sla` 与 sleigh 编译器版本相关，换用别的 Ghidra 版本时需要重新编译（见下）。

## 已验证

- sleigh 编译：`1 languages successfully compiled`；
- headless 导入 VerF 的 `rom.bin`：
  `analyzeHeadless <proj> <name> -import rom.bin -processor nX-U8:LE:16:Casio -loader BinaryLoader -loader-baseAddr 0x0` 成功；
- Ghidra 的反汇编与 `u8-disas` 生成的 `_disas.txt` 一致：
  `000000  B 0x00946a`（对应 `B 00h:0946Ah`）、`00946A  BC AL,0x00946e`（对应 `BC AL, 00946Eh`）。

## 重新编译 nxu8.sla

```bat
set JAVA_HOME=<JDK 25 的目录>
cd <Ghidra 目录>\Ghidra\Processors\nxu8
..\..\..\support\sleigh.bat -i sleighArgs.txt -a .\data\languages
```

也可以在 Eclipse 里对 `buildLanguage.xml` 跑 Ant 的 `sleighCompile` 目标。

## 分发包

`Ghidra 的 nX-U8 语言.zip` 是上述 `nxu8` 文件夹的压缩包，解压得到一个可直接放进
`Ghidra/Processors` 的 `nxu8` 目录。`Ghidra 的 nX-U8 语言.zip.origin-lfs-pointer.txt`
是上游仓库留下的 Git LFS 指针文本（原 zip 走 LFS 存储，克隆时未拉取实体），仅作记录，可删除。

## nX-U8 处理器附加资料

本仓库所关注的计算器均使用 nX-U8 CPU，如果你想了解其指令集等技术信息，请前往「nX-U8 处理器」文件夹。
