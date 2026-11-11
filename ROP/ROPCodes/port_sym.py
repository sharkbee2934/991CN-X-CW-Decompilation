"""把某个版本的 sym.txt 移植到另一个固件版本（如 vC -> VerF）。

做法：以每条符号地址处的**反汇编文本**作为指纹，把会随版本变化的绝对地址
（`093FEh`、`00h:093FEh` 之类）遮蔽掉，然后在目标版本里找指纹**最长公共前缀**
最长的那一处。函数体足够长，通常能唯一确定；短 gadget 天然多解，取最长匹配者
并在注释里标出候选数（这类 gadget 只要语义相同，用哪个实例都可以）。

用法：
    python port_sym.py <源反汇编> <目标反汇编> <sym.txt> <输出文件> [--quiet]
"""
import re
import sys

# 会随固件版本变化的部分：bank:offset 形式的跳转目标、十六进制操作数（地址/位移/位号）、
# 以及十进制立即数（版本间常量也会变，例如 line_print_col0 里的 MOV R2,#206 -> #238）
MASK = [
    (re.compile(r'[0-9A-F]{1,2}h:[0-9A-F]{5}h'), 'A'),
    (re.compile(r'[0-9A-F]+h'), 'H'),
    (re.compile(r'#-?\d+'), '#N'),
]


def normalize(text):
    for pat, rep in MASK:
        text = pat.sub(rep, text)
    return text


def parse_disas(path):
    items, index = [], {}
    with open(path, encoding='utf-8', newline='') as f:
        for raw in f:
            line = raw.rstrip('\r\n')
            if len(line) < 9:
                continue
            try:
                addr = int(line[:6], 16)
            except ValueError:
                continue
            m = re.match(r'^((?:[0-9A-F]{2} )+)', line[9:])
            if not m:
                continue
            index[addr] = len(items)
            items.append((addr, normalize(line[9 + len(m.group(1)):].strip())))
    return items, index


def best_match(src_items, src_index, dst_items, addr, min_depth=6, max_depth=64):
    """返回 (最长匹配长度, [命中地址...])。"""
    i = src_index.get(addr)
    if i is None:
        return 0, []
    best_len, best_hits = 0, []
    for start in range(len(dst_items)):
        n = 0
        while (i + n < len(src_items) and start + n < len(dst_items)
               and src_items[i + n][1] == dst_items[start + n][1]):
            n += 1
        if n > best_len:
            if n >= min_depth:
                best_len, best_hits = n, [dst_items[start][0]]
            else:
                best_len, best_hits = n, [dst_items[start][0]]
        elif n == best_len and n >= min_depth:
            if len(best_hits) < 64:
                best_hits.append(dst_items[start][0])
        if best_len >= max_depth:
            break
    return best_len, best_hits


def main():
    src_disas, dst_disas, sym_path, out_path = sys.argv[1:5]
    quiet = '--quiet' in sys.argv
    src_items, src_index = parse_disas(src_disas)
    dst_items, _ = parse_disas(dst_disas)

    out_lines, report = [], []
    stats = {'unique': 0, 'multi': 0, 'missing': 0}

    with open(sym_path, encoding='utf-8') as f:
        raw_lines = f.readlines()

    for raw in raw_lines:
        line = raw.rstrip('\n')
        body = re.sub(r';.*', '', line).strip()
        if not body or body.startswith('['):
            out_lines.append(line)
            continue
        m = re.match(r'^@?([0-9A-Fa-f]+)(?:\((\d+)\))?\s+(\S.*)$', body)
        if not m:
            out_lines.append(line)
            continue
        addr_s, name = m.group(1), m.group(3).strip()
        addr = int(addr_s, 16)

        depth, hits = best_match(src_items, src_index, dst_items, addr)
        if not hits:
            stats['missing'] += 1
            report.append((name, addr, 0, [], '源反汇编里没有该地址'))
            out_lines.append('; [未移植] ' + line.strip())
            continue

        new_addr = hits[0]
        new_hex = format(new_addr, 'X').rjust(len(addr_s), '0')
        idx = line.index(addr_s)
        new_line = line[:idx] + new_hex + line[idx + len(addr_s):]
        if len(hits) == 1:
            stats['unique'] += 1
            report.append((name, addr, depth, hits, 'ok'))
        else:
            stats['multi'] += 1
            report.append((name, addr, depth, hits, '多解'))
            new_line = new_line + '   ; 指纹长度 %d，另有 %d 处同指纹候选' % (depth, len(hits) - 1)
        out_lines.append(new_line)

    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out_lines) + '\n')

    total = sum(stats.values())
    print('=== %d 项: 唯一 %d, 多解 %d, 未找到 %d ==='
          % (total, stats['unique'], stats['multi'], stats['missing']))
    if not quiet:
        for name, old, depth, hits, st in sorted(report, key=lambda r: r[2]):
            if st == 'ok':
                continue
            print('  %-42s %06X 指纹=%2d %s %s' % (
                name, old, depth, st,
                ' '.join(format(h, 'X') for h in hits[:4]) + (' ...' if len(hits) > 4 else '')))


if __name__ == '__main__':
    main()
