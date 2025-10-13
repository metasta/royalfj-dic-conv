#/// script
# dependencies = [
#     "typing",
# ]
# ///

import os
import re
from typing import List, Tuple
from pathlib import Path

def correct_simple_items(src_dir, dst_dir):
    """単純置換"""
    def correct_item(item: str, rules: List[Tuple[str, str]]):
        in_file  = src_dir / item
        out_file = dst_dir / item
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

    correct_item("A/A-04722.htm", [("<ギリシ", "＜ギリシ"), ("＜a ", "<a ")])
    correct_item("B/B-02465.htm", [("<it."  , "＜it."  ), ("＜a ", "<a ")])
    correct_item("B/B-03502.htm", [("<it."  , "＜it."  ), ("＜a ", "<a ")])
    correct_item("H/H-00271.htm", [("<angl.", "＜angl."), ("＜a ", "<a ")])
    correct_item("H/H-00795.htm", [("<数学者", "＜数学者"), ("＜a ", "<a ")])
    correct_item("L/L-01647.htm", [("<イタリ", "＜イタリ"), ("＜sp", "<sp")])
    correct_item("R/R-03715.htm", [("<gr."  , "＜gr."  ), ("＜i>", "<i>")])
    correct_item("S/S-02125.htm", [("<タイ王", "＜タイ王"), ("＜a ", "<a ")])

def correct_split_r02616(src_dir, dst_dir):
    """R-02616.htm から R-02615.htm と R-02616.htm を生成する"""
    src_file = Path(src_dir) / "R" / "R-02616.htm"
    text = src_file.read_text(encoding="shift_jis")

    # R-02615.htm の生成
    r02615_text = text
    # 1. init('R-02616') → init('R-02615')
    r02615_text = r02615_text.replace("init('R-02616')", "init('R-02615')")
    # 2. (=battre an retraite)</span>以降「...防壁</span>」</td>を削除
    r02615_text = re.sub(
        r"\(=battre an retraite\)</span>.*防壁</span></td>",
        r"(=battre an retraite)</span></td>",
        r02615_text,
        flags=re.DOTALL
    )
    # 3. 「<div class="end_zone">...<hr>」を削除
    r02615_text = re.sub(
        r'<div class="end_zone"><hr>.*<hr>',
        "",
        r02615_text,
        flags=re.DOTALL
    )
    # 書き出し
    dst_r02615 = Path(dst_dir) / "R" / "R-02615.htm"
    dst_r02615.parent.mkdir(parents=True, exist_ok=True)
    dst_r02615.write_text(r02615_text, encoding="shift_jis")

    # R-02616.htm の生成
    r02616_text = text
    # 「retraiter</span>......<span class="midasi">」を削除
    r02616_text = re.sub(
        r"retraiter</span>.*<span class=\"midasi\">",
        "",
        r02616_text,
        flags=re.DOTALL
    )
    # 書き出し
    dst_r02616 = Path(dst_dir) / "R" / "R-02616.htm"
    dst_r02616.write_text(r02616_text, encoding="shift_jis")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python error_correction.py path/to/itemPages path/to/outDir", file=sys.stderr)
        sys.exit(1)

    src_dir = Path(sys.argv[1]).expanduser()
    dst_dir = Path(sys.argv[2]).expanduser()

    correct_simple_items(src_dir, dst_dir)
    correct_split_r02616(src_dir, dst_dir)
