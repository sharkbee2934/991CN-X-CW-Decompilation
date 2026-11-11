# 卡西欧 ClassWiz 计算器研究资料

fx-991CN X / fx-991CN CW 的固件、反编译工程、ROP 开发资料与配套资源。

> **本仓库是归档镜像，不是原项目。**
> 原始材料来自 **[Physics365/991CN-X-CW-Decompilation](https://github.com/Physics365/991CN-X-CW-Decompilation)** 及其 LFS 镜像仓库，以 **GPL-3.0** 分发。
> 本镜像的内容经过 **ShakerPlace3912 与 AI 协作再整理**：补充了完整性校验表（逐文件 SHA-256）、上游 LFS 指针失效后的资源回补记录、VerF 版本支持说明与示例、"已知问题 / 待办"清单，并核对了文档与实际文件的差异。
> **固件（`ROM/*/rom.bin`）版权归卡西欧（CASIO Computer Co., Ltd.）所有**，此处仅为逆向研究用途留存，请勿用于商业分发。

## 来源与许可

- 主体内容来自 **<https://github.com/Physics365/991CN-X-CW-Decompilation>**，以 **GPL-3.0** 分发（见 [LICENSE](LICENSE)）。
- 本次归档由 **ShakerPlace3912** 主导、AI 协助完成整理与校验，公开镜像见 <https://github.com/sharkbee2934/991CN-X-CW-Decompilation>。
- Ghidra 处理器模块 `反编译相关/nxu8` 出自 **[EwTE_H](https://tieba.baidu.com/home/main?id=tb.1.ba0c2f47.avRm7aRqck4QgwYYgIf3eA) 的 [nX-U8_for_Ghidra](https://github.com/EwTE-H/nX-U8_for_Ghidra)**，已逐文件与上游 sha256 核对。
- 字体、字符表、真机 ROM、教程文档取自该项目的 LFS 镜像仓库 **`991CN-X-CW-Decompilation_Files`**（源仓库的 Git LFS 已关闭，`.zip` 等指针无法解析，故这类资源一律取自镜像仓库的直存文件）。

## 本文档的整理说明

上游仓库的部分文档与实际文件存在出入，本次整理据实核对后修正，供后续使用者参考：

| 项目 | 上游文档说法 | 实际情况 |
| --- | --- | --- |
| GBK 编码文件 | 「README.md 与 贪吃蛇/README.md 两处为 GBK」 | 仅 `ROP/复杂ROP程序/README.md` 为 GBK，`贪吃蛇/README.md` 已是 UTF-8 |
| `buildLanguage.xml` 字节数 | 1662 | 1667 |
| `__pycache__` | 未提及 | 为 cpython-314 字节码，与本地 Python 3.12 不兼容，已加入 `.gitignore` |

此外，仓库内共发现 5 组完全重复的文件（SHA-256 相同），保留未删以免破坏上游目录结构：

- `字体/显示字体/991CN X/README.pdf` 与 `字体/显示字体/991CN CW/README.pdf`
- `字体/显示字体/991CN X/README-math.pdf` 与 `字体/显示字体/991CN CW/README-math.pdf`
- `教程文档/教程前三章.pdf` 与 `ROP/教程/教程前三章(unfin).pdf`
- `ROM/fx991cnx-vC/model.lua` 与 `ROM/fx991cnx-vF/model.lua`
- `ROM/fx991cnx-vC/interface.png` 与 `ROM/fx991cnx-vF/interface.png`

## 目录

| 目录 | 内容 |
| --- | --- |
| [ROM](ROM) | 三套固件 + CasioEmuX 机型定义（`model.lua`、`interface.png`、`_disas.txt`、`mem-spans.txt` 内存区标注） |
| [反编译相关](反编译相关) | Ghidra 的 nX-U8 处理器模块 `nxu8`、nX-U8 资料、反编译产物（`反编译结果` 下按 VerC/VerF 分目录的 C 与汇编）、生成 `_disas.txt` 的 `u8-disas` 反汇编器 |
| [ROP](ROP) | ROP 汇编器 `asm.py` 与符号表（`sym.txt` 对应 vC，`sym_vF.txt` 对应 VerF）、示例、常用函数说明（`Labels`）、成品程序（`复杂ROP程序`）、教程 |
| [字符表](字符表) | fx-991CN X VerC 一/二级字符表 PDF |
| [字体](字体) | 按键字体（TTF + 键位图）与显示字体（OTF/TTF/WOFF2 + 字形说明） |
| [教程文档](教程文档) | 《991CN X 教程》Ver 2.0 / Ver 3.0 / 20240411 及分章 docx、Word 模板 |

## ROM 一览

| 目录 | 大小 | 版本串（0x3FFF0 处） | SHA-256 |
| --- | --- | --- | --- |
| `ROM/fx991cnx-vC` | 262144 | `-239C` | `8b6b6430f96858a8b3e765796e2d6f340bc7073ac9b0aa464775f15e53a10788` |
| `ROM/fx991cnx-vF` | 262144 | `-239F` | `444ff0c4d60dbb509b4682bbe32dc82d64d3b6311c2915e5b96409f91addeede` |
| `ROM/fx991cncw-vA` | 1048576 | — | `4ab4791609cc8686fc6b4d1be34b3e6d19b3eb700abe8c9e3edd91ff2813471f` |

`fx991cnx-vC` 与上游 `真机ROM/991CN X/rom.bin` 完全一致，是 VerC 官方 dump；`fx991cnx-vF` 是另一份独立 dump（与 vC 相差 104787 字节，`_start` 从 `0x093FE` 移到 `0x0946A`）。ROP 资料里的符号表地址均对应 **vC**。

每个 `ROM/*/` 目录下的 `_disas.txt` 由 [反编译相关/u8-disas](反编译相关/u8-disas) 生成（CasioEmuNeo 自带的反汇编器，实现了 sleigh 未包含的 `SWI`/`RTI`/`BRK`/`CR` 传送等指令，**不是 Ghidra 的输出**）：

| 文件 | 行数 | 大小 | SHA-256 |
| --- | --- | --- | --- |
| `fx991cnx-vC/_disas.txt` | 117010 | 4850937 | `82897a64125dbfb963e7b14d6eab19e59fe2a1c2e7b4ca721a4cb1cc943533df` |
| `fx991cnx-vF/_disas.txt` | 116944 | 4850490 | `25059ef0a99e257175d0911e517a413e4c383c03050596983f75dfda7fddddd3` |

## VerF 支持

`ROP/ROPCodes` 下的 `sym.txt` 只对应 vC。VerF 的地址另有 [sym_vF.txt](ROP/ROPCodes/sym_vF.txt)（由 `port_sym.py` 按反汇编指纹移植，99 项全部唯一命中），并附了三个 VerF 版示例：单行拼字 [VerF-Single-Line-Print.asm](ROP/ROPCodes/Examples/VerF-Single-Line-Print.asm)、循环翻页 [VerF-Loop.asm](ROP/ROPCodes/Examples/VerF-Loop.asm)（即教程《循环/汇编器》里那份）、条纹+拼字+延时+关机 [VerF-Stripe-Print-Off.asm](ROP/ROPCodes/Examples/VerF-Stripe-Print-Off.asm)，后两者已在 VerF 真机上跑通。`Examples/` 下 9 个程序在 VerF 表下全部编译通过，差异只落在地址字节上。`asm.py` 增加了 `-sym <文件>` 参数以便切换地址表，用法与校验见 [VerF.md](ROP/ROPCodes/VerF.md)。

另有人工整理的 VerF 常用地址表 [北冥表.md](ROP/ROPCodes/北冥表.md)（拼字/花式/刷新/内存/按键/循环/条件/寄存器赋值，均带 VerC 对应）。它与 `sym_vF.txt` 按 VerC 地址对齐后 16/18 项一致，两项差异经反汇编核对为原表笔误。

## 已知问题 / 待办

1. `ROP/复杂ROP程序/README.md` 与 `ROP/复杂ROP程序/fx991cnx/贪吃蛇/README.md` 为 GBK 编码，UTF-8 环境下显示为乱码。
2. `ROP/ROPCodes/Examples/Persistence/CodePersistence.md` 为空文件；`ROP/Labels/README.md` 仅一句占位。
3. `ROP/README.md` 称处理器为 "nX-u16"，与其余资料的 nX-U8 不一致。
4. `ROM/fx991cncw-vA` 只有 `rom.bin`，没有对应的 `model.lua` / `interface.png`，CasioEmuNeo 尚无法直接载入。
5. VerF 的 ROP 示例 [VerF-Single-Line-Print.asm](ROP/ROPCodes/Examples/VerF-Single-Line-Print.asm) 尚未在真机或模拟器上验证。
