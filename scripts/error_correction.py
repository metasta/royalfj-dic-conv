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
    # --- < と ＜ ---
    correct_item("A/A-04722.htm", [("<ギリシ", "＜ギリシ"), ("＜a ", "<a ")])
    correct_item("B/B-02465.htm", [("<it."  , "＜it."  ), ("＜a ", "<a ")])
    correct_item("B/B-03502.htm", [("<it."  , "＜it."  ), ("＜a ", "<a ")])
    correct_item("H/H-00271.htm", [("<angl.", "＜angl."), ("＜a ", "<a ")])
    correct_item("H/H-00795.htm", [("<数学者", "＜数学者"), ("＜a ", "<a ")])
    correct_item("L/L-01647.htm", [("<イタリ", "＜イタリ"), ("＜sp", "<sp")])
    correct_item("R/R-03715.htm", [("<gr."  , "＜gr."  ), ("＜i>", "<i>")])
    correct_item("S/S-02125.htm", [("<タイ王", "＜タイ王"), ("＜a ", "<a ")])

    # --- "(())" → "｟｠" 置換の例外 ---
    correct_item("A/A-00192.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("A/A-00298.htm", [(" (fran&ccedil;aise))", " (fran&ccedil;aise) )")])
    correct_item("A/A-00332.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("A/A-00567.htm", [("B(qn.))", "B(qn.) )")]) # 2箇所置換
    correct_item("A/A-00775.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("A/A-01899.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("A/A-02450.htm", [("〜(s))", "〜(s) )")])
    correct_item("A/A-02451.htm", [("〜(s))", "〜(s) )")])
    correct_item("A/A-04809.htm", [("〜(s))", "〜(s) )")])
    correct_item("B/B-01016.htm", [("dessin&eacute;e))", "dessin&eacute;e) )")])
    correct_item("B/B-01267.htm", [("tout(e))", "tout(e) )")])
    correct_item("B/B-02662.htm", [("&oelig;uvres))", "&oelig;uvres) )")])
    correct_item("B/B-03303.htm", [("〜(s))", "〜(s) )")])
    correct_item("C/C-00106.htm", [("〜(s))", "〜(s) )")])
    correct_item("C/C-01189.htm", [("A(qc.))", "A(qc.) )")])
    correct_item("C/C-01368.htm", [("〜(s))", "〜(s) )")])
    correct_item("C/C-01674.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("C/C-02316.htm", [("B(qc./inf.))", "B(qc./inf.) )"), ("B(qc.))", "B(qc.) )")])
    correct_item("C/C-02702.htm", [("B(qc.))", "B(qc.) )"), ("B(qn.))", "B(qn.) )")])
    correct_item("C/C-03972.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("C/C-04226.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("C/C-04611.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("C/C-04932.htm", [("A(inf.))", "A(inf.) )")])
    correct_item("C/C-05059.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("C/C-05168.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("C/C-06024.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("C/C-06146.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("C/C-06183.htm", [("B(qc.))", "B(qc.) )")]) # 2箇所置換
    correct_item("C/C-06364.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("D/D-00377.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("D/D-00759.htm", [("A(inf.))", "A(inf.) )")])
    correct_item("D/D-00806.htm", [("B(inf./qc.))", "B(inf./qc.) )")])
    correct_item("D/D-00999.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("D/D-01397.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("D/D-01469.htm", [("〜(e))", "〜(e) )")])
    correct_item("D/D-01965.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("D/D-02385.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("D/D-02435.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("D/D-02646.htm", [("B(qc./inf.))", "B(qc./inf.) )")])
    correct_item("D/D-03465.htm", [("B(qn.))", "B(qn.) )"), ("B(qc.))", "B(qc.) )")])
    correct_item("D/D-03830.htm", [("〜(s))", "〜(s) )")])
    correct_item("D/D-03836.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("E/E-00160.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("E/E-00416.htm", [("〜(s))", "〜(s) )"), ("sainte(s))", "sainte(s) )")])
    correct_item("E/E-02051.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("E/E-02699.htm", [("rush(es))", "rush(es) )")])
    correct_item("E/E-03686.htm", [("(qc.))", "(qc.) )")])
    correct_item("E/E-03728.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("F/F-00154.htm", [("que+subj.])))", "que+subj.]) ))")])
    correct_item("F/F-00206.htm", [("que+subj.)))", "que+subj.) ))")])
    correct_item("F/F-00487.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("F/F-01207.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("F/F-01322.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("F/F-02341.htm", [("〜(s))", "〜(s) )")])
    correct_item("F/F-02565.htm", [("B(qc.))", "B(qc.) )")]) # 2箇所置換
    correct_item("G/G-00357.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00360.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00361.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00368.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00369.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00372.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00378.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00382.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-00387.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-02154.htm", [("〜(s))", "〜(s) )")])
    correct_item("G/G-02223.htm", [("groseille(s))", "groseille(s) )")])
    correct_item("G/G-02373.htm", [("〜(s))", "〜(s) )")])
    correct_item("H/H-00081.htm", [("(la))", "(la) )")])
    correct_item("H/H-00354.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("H/H-00367.htm", [("〜(s))", "〜(s) )")])
    correct_item("H/H-01320.htm", [("〜(s))", "〜(s) )")])
    correct_item("I/I-00307.htm", [("((simple)", "( (simple)")])
    correct_item("I/I-00834.htm", [("〜(s))", "〜(s) )")])
    correct_item("I/I-00848.htm", [("B(qc./inf.))", "B(qc./inf.) )")])
    correct_item("I/I-01020.htm", [("A(que+ind.))", "A(que+ind.) )")])
    correct_item("I/I-01494.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("I/I-01611.htm", [("B(qc.))", "B(qc.) )")]) # 2箇所置換
    correct_item("I/I-01829.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("I/I-01850.htm", [("B(n./inf.))", "B(n./inf.) )")])
    correct_item("I/I-01874.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("I/I-02038.htm", [("B(qn.))", "B(qn.) )"), ("B(inf.))", "B(inf.) )"), ("B(qc.))", "B(qc.) )")])
    correct_item("I/I-02135.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("I/I-02297.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("I/I-02379.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("L/L-00846.htm", [("〜(s))", "〜(s) )")])
    correct_item("M/M-02028.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("M/M-02424.htm", [("〜(s))", "〜(s) )")])
    correct_item("N/N-00081.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("O/O-00356.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("O/O-00560.htm", [("elle(s))", "elle(s) )")])
    correct_item("O/O-01250.htm", [("B(qn.))", "B(qn.) )"), ("B(qc.))", "B(qc.) )"), ("A(qc.))", "A(qc.) )")])
    correct_item("O/O-01276.htm", [(" (bien))", " (bien) )")])
    correct_item("O/O-01400.htm", [("dame(s))", "dame(s) )")])
    correct_item("P/P-00443.htm", [("〜(s))", "〜(s) )")])
    correct_item("P/P-00628.htm", [("〜(s))", "〜(s) )")])
    correct_item("P/P-00826.htm", [("〜(s))", "〜(s) )")])
    correct_item("P/P-00829.htm", [("〜(x))", "〜(x) )")])
    correct_item("P/P-00830.htm", [("〜(s))", "〜(s) )")])
    correct_item("P/P-00993.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("P/P-01072.htm", [("un(e))", "un(e) )")])
    correct_item("P/P-01130.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("P/P-01431.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("P/P-02139.htm", [(" qn.)))", " qn.) ))")])
    correct_item("P/P-02175.htm", [("(&agrave;))", "(&agrave;) )")])
    correct_item("P/P-04042.htm", [("(am&eacute;ricain))", "(am&eacute;ricain) )")])
    correct_item("P/P-04545.htm", [("〜(s))", "〜(s) )")])
    correct_item("P/P-04575.htm", [("〜(s))", "〜(s) )")])
    correct_item("P/P-04621.htm", [("〜(s))", "〜(s) )")])
    correct_item("P/P-05278.htm", [("B(qc.))", "B(qc.) )"), ("B(qn.))", "B(qn.) )")])
    correct_item("P/P-05434.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("P/P-05498.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("P/P-05591.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("P/P-05669.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("P/P-05818.htm", [("ind.])))", "ind.]) ))"), ("B(qn.))", "B(qn.) )")])
    correct_item("P/P-05898.htm", [("subj.])))", "subj.]) ))"), ("B(qn.))", "B(qn.) )")])
    correct_item("P/P-06131.htm", [("prune(s))", "prune(s) )")])
    correct_item("Q/Q-00374.htm", [("B(qn.))", "B(qn.) )"), ("B(qc.))", "B(qc.) )")])
    correct_item("R/R-00707.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("R/R-01314.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("R/R-01367.htm", [("A(n.))", "A(n.) )")])
    correct_item("R/R-01833.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("R/R-02382.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("R/R-02764.htm", [("B(qc.))", "B(qc.) )")]) # 4箇所置換
    correct_item("R/R-02807.htm", [("(Cuvier))の", "(Cuvier)の")]) # )) → )
    correct_item("R/R-03187.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("S/S-00267.htm", [("〜(s))", "〜(s) )")])
    correct_item("S/S-00494.htm", [("〜(s))", "〜(s) )")])
    correct_item("S/S-00874.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("S/S-02830.htm", [("B(inf.))", "B(inf.) )")])
    correct_item("S/S-03197.htm", [("〜(s))", "〜(s) )")])
    correct_item("S/S-03303.htm", [("〜(s))", "〜(s) )")])
    correct_item("S/S-04649.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("T/T-00993.htm", [("B(qn.))", "B(qn.) )")])
    correct_item("T/T-01684.htm", [("〜(s))", "〜(s) )")])
    correct_item("T/T-01753.htm", [("〜(s))", "〜(s) )")])
    correct_item("T/T-01760.htm", [("〜(s))", "〜(s) )")])
    correct_item("T/T-01763.htm", [("〜(s))", "〜(s) )")])
    correct_item("T/T-02456.htm", [("〜(s))", "〜(s) )")])
    correct_item("T/T-03309.htm", [("B(qc.))", "B(qc.) )")])
    correct_item("T/T-03499.htm", [("〜(s))", "〜(s) )")])
    correct_item("U/U-00130.htm", [("un(e))", "un(e) )"), ("autre C)))", "autre C) ))")])
    correct_item("U/U-00379.htm", [("(avec qn.)))", "(avec qn.) ))")])
    correct_item("U/U-00412.htm", [("(qn.))", "(qn.) )")])
    correct_item("V/V-00569.htm", [("(qn.))", "(qn.) )")])
    correct_item("V/V-01545.htm", [(" qn.)))", " qn.) ))")])

    # --- Êêtre → Être など ---
    correct_item("E/E-00201.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Échec
    correct_item("E/E-00204.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Échelle
    correct_item("E/E-00232.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Échiquier
    correct_item("E/E-00234.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Écho
    correct_item("E/E-00310.htm", [("&Eacute;&eacute;", "&Eacute;")]) # École
    correct_item("E/E-00359.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Écossais
    correct_item("E/E-00501.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Édit
    correct_item("E/E-00517.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Éducation
    correct_item("E/E-00648.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Égalité
    correct_item("E/E-00667.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Église
    correct_item("E/E-00776.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Électeur
    correct_item("E/E-01212.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Éminence
    correct_item("E/E-02484.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Éphésien
    correct_item("E/E-02671.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Époque
    correct_item("E/E-02694.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Époux
    correct_item("E/E-03255.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Établissements
    correct_item("E/E-03314.htm", [("&Eacute;&eacute;", "&Eacute;")]) # État
    correct_item("E/E-03345.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Éternel
    correct_item("E/E-03440.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Étoile
    correct_item("E/E-03445.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Étolienne
    correct_item("E/E-03479.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Étrangleur
    correct_item("E/E-03482.htm", [("&Ecirc;&ecirc;", "&Ecirc;")]) # Être
    correct_item("E/E-03513.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Étudiant
    correct_item("E/E-03664.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Évangile
    correct_item("E/E-03684.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Évêché
    correct_item("E/E-03701.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Éventreur
    correct_item("E/E-03714.htm", [("&Eacute;&eacute;", "&Eacute;")]) # Évidemment
    correct_item("I/I-00217.htm", [("&Icirc;&icirc;", "&Icirc;")]) # Île

def correct_r00345(src_dir, dst_dir):
    """R-00345.htm の .kanren 前の .tyuki の位置を修正する"""
    src_file = Path(src_dir) / "R" / "R-00345.htm"
    text = src_file.read_text(encoding="shift_jis")
    text = re.sub(
        r'<span class="tyuki">\(<span class="aster"><td>\s*<table>(.*?)\)</span>',
        r'<td><table><tr><td><span class="tyuki">(<span class="aster">\1)</span></td></tr>',
        text,
        flags=re.DOTALL
    )
    dst = Path(dst_dir) / "R" / "R-00345.htm"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="shift_jis")

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
    correct_r00345(src_dir, dst_dir)
    correct_split_r02616(src_dir, dst_dir)
