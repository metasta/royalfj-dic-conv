#/// script
# dependencies = [
#     "typing",
# ]
# ///

import os
from typing import List, Tuple
from pathlib import Path

def replace_in_file(rules: List[Tuple[str, str]], in_file: str, out_file: str ):

    # 出力先のディレクトリが存在しなければ作成
    out_dir = Path(out_file).parent
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    # in_file 内の文字列を rules に従って置換し out_file に保存
    with open( in_file, "r", encoding="Shift-JIS") as fin, \
         open(out_file, "w", encoding="Shift-JIS") as fout:
        for line in fin:
            for old, new in rules:
                line= line.replace(old, new)
            fout.write(line)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python error_correction.py path/to/itemPages path/to/outDir", file=sys.stderr)
        sys.exit(1)

    src_dir = Path(sys.argv[1]).expanduser()
    dst_dir = Path(sys.argv[2]).expanduser()

    def correct_item(item: str, rules: List[Tuple[str, str]]):
        in_file  = src_dir / item
        out_file = dst_dir / item
        replace_in_file(rules, in_file, out_file)

    correct_item("A/A-04722.htm", [("<ギリシ", "＜ギリシ"), ("＜a ", "<a ")])
    correct_item("B/B-02465.htm", [("<it."  , "＜it."  ), ("＜a ", "<a ")])
    correct_item("B/B-03502.htm", [("<it."  , "＜it."  ), ("＜a ", "<a ")])
    correct_item("H/H-00271.htm", [("<angl.", "＜angl."), ("＜a ", "<a ")])
    correct_item("H/H-00795.htm", [("<数学者", "＜数学者"), ("＜a ", "<a ")])
    correct_item("L/L-01647.htm", [("<イタリ", "＜イタリ"), ("＜sp", "<sp")])
    correct_item("R/R-03715.htm", [("<gr."  , "＜gr."  ), ("＜i>", "<i>")])
    correct_item("S/S-02125.htm", [("<タイ王", "＜タイ王"), ("＜a ", "<a ")])
