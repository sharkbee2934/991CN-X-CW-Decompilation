;
; 名称: 单行拼字（VerF）
; 模式: 110an
;
; 本文件是 Examples/Single-Line-Print.asm 的 VerF 版：
; 唯一的区别是 line_print_col0 的地址取自 sym_vF.txt（0x2210A，而非 vC 的 0x220FE）。
; 编译方式：
;   python .\asm.py .\Examples\VerF-Single-Line-Print.asm -sym .\sym_vF.txt
;
; 注意：ROP 的触发方式（110an 下用栈溢出改写返回地址）沿用 vC 教程，
;       它依赖的是 RAM 布局而非固件地址，但本程序未在真机或模拟器上验证。

hex 6c 6f 76 65 20 79 6f 75 ; `love you`
hex 20 20 20 20 20 20 20 20 20 ; ' '*9
space 17
; total 34 bytes above

line_print_col0
; 注意，这个符号可以用 SHIFT+8 下 2 6 打出
