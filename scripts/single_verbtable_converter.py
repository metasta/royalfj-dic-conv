# /// script
# dependencies = [
#  "lxml",
# ]
# ///

from lxml import etree, html
import re
from common_functions import replace_apostrophe

NSMAP = {"d": "http://www.apple.com/DTDs/DictionaryService-1.0.rng"}

# -------------------------
# メイン変換関数
# -------------------------

def convert_verbtable(htm_path):
    parser = html.HTMLParser(encoding="shift-jis")
    tree = html.parse(htm_path, parser)
    body = tree.find(".//body")
    if body is None:
        raise ValueError(f"{htm_path} に <body> が見つかりません")

    # --- htm_path → id ---
    m = re.search(r"([^/]+)\.htm", htm_path.as_posix())
    entry_id = "_Conju-" + m.group(1) if m else None

    # --- .midasi → title ---
    midasi = body.xpath(".//*[@class='midasi']")
    if midasi is None:
        raise ValueError(f"{htm_path} に class='midasi' が見つかりません")
    infinitif = midasi[0].text_content().replace("：直説法", "")
    entry_title = f"{infinitif} 活用表"

    # --- tr.menu_bar を持つ table → 削除
    for table in body.xpath("./table[tr[@class='menu_bar']]"):
        body.remove(table)

    # --- body 直下の br → 削除 ---
    for br in body.findall("br"):
        body.remove(br)

    # --- <d:entry> 構築 ---
    entry = etree.Element(f"{{{NSMAP['d']}}}entry",
                          attrib={"id": entry_id,
                                  f"{{{NSMAP['d']}}}title": entry_title},
                          nsmap=NSMAP)
    # --- d:index ---
    all_texts = body.xpath("//tr[@class='data']//text()")
    words = set([
        (word[2:] if word.lower().startswith(("j'", "m'", "t'", "s'")) else word)
        for text in all_texts
        if text.strip()
        for word in [text.strip().split()[-1]]
    ])
    words.add(infinitif) # 原形を追加
    for w in words:
        i = etree.Element(f"{{{NSMAP['d']}}}index",
                          attrib={f"{{{NSMAP['d']}}}value": w, 
                                  f"{{{NSMAP['d']}}}title": entry_title},
                          nsmap=NSMAP)
        entry.append(i)

    # --- d:entry ---
    for child in list(body):
        entry.append(child)

    # アポストロフィを置換
    replace_apostrophe(entry)

    return entry

# -------------------------
# コマンドライン実行用
# -------------------------

if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) != 3:
        print("Usage: python single_verbtable_converter.py input.htm output.xml", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    d_entry = convert_conju(input_path)
    tree = etree.ElementTree(d_entry)
    tree.write(output_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
