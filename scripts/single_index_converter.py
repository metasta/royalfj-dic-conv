# /// script
# dependencies = [
#  "lxml",
# ]
# ///

from pathlib import Path
from lxml import etree, html
import re

NSMAP = {"d": "http://www.apple.com/DTDs/DictionaryService-1.0.rng"}

# -------------------------
# 共通補助関数
# -------------------------

def add_index_to_entry(id2entry, entry_id, value=None, anchor=None, title=None):
    if entry_id in id2entry:
        entry_elem = id2entry[entry_id]
    else:
        entry_elem = etree.Element(f"{{{NSMAP['d']}}}entry")
        entry_elem.set("id", entry_id)
        id2entry[entry_id] = entry_elem

    index_elem = etree.SubElement(entry_elem, f"{{{NSMAP['d']}}}index")
    if value: index_elem.set(f"{{{NSMAP['d']}}}value", value)
    if anchor: index_elem.set(f"{{{NSMAP['d']}}}anchor", f"xpointer(//*[@id='{entry_id}_{anchor}'])")
    if title: index_elem.set(f"{{{NSMAP['d']}}}title", title)

# -------------------------
# モード別関数
# -------------------------

def convert_midasi(tr_list):
    id2entry = {}
    for tr in tr_list:
        td = tr.find("td")
        if td is None:
            continue
        onclick = td.get("onclick", "")
        m = re.search(r"open_detail\('(.+?)','.*?'\)", onclick)
        if not m: 
            continue
        entry_id = m.group(1)
        a_elem = td.find("a")
        if a_elem is None: 
            continue
        term = "".join(a_elem.itertext()).strip()
        add_index_to_entry(id2entry, entry_id, value=term)
    return id2entry

def convert_seiku(tr_list):
    id2entry = {}
    for tr in tr_list:
        td = tr.find("td")
        if td is None:
            continue
        onclick = td.get("onclick", "")
        m = re.search(r"moveSeikuLine\('(.+?)','(.+?)','.*?'\)", onclick)
        if not m: 
            continue
        entry_id, anchor_num = m.group(1), m.group(2)
        term = "".join(td.itertext()).strip()
        add_index_to_entry(id2entry, entry_id, value=term, anchor=anchor_num)
    return id2entry

def convert_conju(tr_list):
    id2entry = {}
    for tr in tr_list:
        td = tr.find("td")
        if td is None:
            continue
        onclick = td.get("onclick", "")
        m = re.search(r"open_detail\('(.+?)','.*?'\)", onclick)
        if not m: 
            continue
        entry_id = m.group(1)
        a_elem = td.find("a")
        value_text = "".join(a_elem.itertext()).strip() if a_elem is not None else None
        span = td.find("span[@class='base_mida']")
        title_text = "".join(span.itertext()).lstrip("→⇒").strip() if span is not None else None
        add_index_to_entry(id2entry, entry_id, value=value_text, title=title_text)
    return id2entry

# -------------------------
# メイン変換関数
# -------------------------

def convert_index(htm_file: Path, mode: str):
    html_bytes = htm_file.read_bytes()
    html_text = html_bytes.decode("shift_jis")
    tree = html.fromstring(html_text)

    dictionary = etree.Element(f"{{{NSMAP['d']}}}dictionary", nsmap=NSMAP)

    if mode == "midasi":
        tr_list = tree.xpath("//tr[@class='index_mida']")
        id2entry = convert_midasi(tr_list)
    elif mode == "seiku":
        tr_list = tree.xpath("//tr[@class='seiku']")
        id2entry = convert_seiku(tr_list)
    elif mode == "conju":
        tr_list = tree.xpath("//tr[@class='index_mida']")
        id2entry = convert_conju(tr_list)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    for entry_elem in id2entry.values():
        dictionary.append(entry_elem)

    return dictionary

# -------------------------
# コマンドライン実行用
# -------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python single_index_converter.py mode(midasi|seiku|conju) input.htm output.xml", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    input_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    d_dictionary = convert_index(input_path, mode=mode)
    tree = etree.ElementTree(d_dictionary)
    tree.write(output_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
