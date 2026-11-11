;
; 名称: 循环 / 按键翻页（VerF）
;
; 本文件是 Examples/Loop.asm 的 VerF 版，对应知乎
; 《「循环/汇编器」991cnx：利用 rop 漏洞执行任意代码》里的示例。
; 与 vC 版**代码完全相同**，只是用 -sym 换成 VerF 的地址表：
;   python .\asm.py .\Examples\VerF-Loop.asm -sym .\sym_vF.txt
;
; 效果：
;   1. 显示 love you
;   2. 等待按键（SHIFT）
;   3. 显示 forever
;   4. 等待按键（SHIFT）
;   5. 回到 1
;
; 循环结构三步：执行循环体 → smart_strcpy 把输入区拷回栈底 → 重置 er14 再跳回开头
; 依赖的符号（VerF 地址）：
;   pop qr0 0130E2 / printline 0221B8 / waitkey 0221D0
;   smart_strcpy 0203C8 / pop ER14 020D72 / jpop qr80 02238E

; mode: 126an（原 124an + 2）
;   教程《进阶篇》「b. 构造你想要的栈偏移」给的规律：ROP 从输入缓冲区第 (n-76) 个字节开始执行，
;   且必须落在偶数偏移上，即「(76+n) bytes + an」。原来 16 字节前缀对应你实测可用的那个 n，
;   现在前缀改成 18 字节（8 字符 + 10 空格），所以 n 也要 +2。
;   （若严格按 n = 76 + 前缀，则应为 94an。）

hex 6c 6f 76 65 20 79 6f 75 ; `love you`
hex 20 20 20 20 20 20 20 20 20 20 ; 10 个空格占位：凑到 18 字节，让拼字函数那一行 17 字符全是文字和空格
home:
    pop qr0
    hex 20 20 80 d1 30 30 30 30
    ; 不用标签指向 `love you`：函数调用会压栈破坏栈上的数据，
    ; 所以改用 0xd180（输入区）而不是栈区
    printline
    waitkey
    pop qr0
    hex 20 20
    adr label2
    hex 30 30 30 30
    printline
    waitkey
    pop qr0
    hex 22 d5 80 d1 30 30 30 30 ; er0=0xd522(栈底) er2=0xd180(输入区)
    smart_strcpy
    pop ER14
    adr home -16
    jpop qr80   ; 设 sp=er14 后 pop qr8、pop qr0
label2:
    hex 46 6f 72 20 65 76 65 72  ; `Forever`
    hex 20 20 20 20 20 20 20 20 20 ; 补 9 个空格，凑满一行 17 字符，避免把后面的内存内容显示出来
    ; 位于栈末尾，被压栈破坏也无所谓
