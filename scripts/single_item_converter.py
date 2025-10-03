# /// script
# dependencies = [
#  "lxml",
# ]
# ///

from lxml import etree, html
import re

NSMAP = {"d": "http://www.apple.com/DTDs/DictionaryService-1.0.rng"}

# hatuon の変換規則
hatuon_rules = {
    ord("!"): "æ", ord('"'): "ɑ", ord("#"): "ɛ", ord("$"): "ɔ",
    ord("%"): "œ", ord("&"): "ʌ", ord("'"): "ə", ord("*"): "ʌ",
    ord("+"): "ɑ", ord("0"): "ʒ", ord("1"): "ã", ord("2"): "ɑ̃",
    ord("3"): "ɛ̃", ord("4"): "ɔ̃", ord("5"): "œ̃", ord("6"): "ʃ",
    ord("7"): "ŋ", ord("8"): "θ", ord("9"): "ð", ord("?"): "ø",
    ord("@"): "ç", ord("A"): "à", ord("B"): "ɔ̀", ord("C"): "ʌ̀",
    ord("D"): "ə̀", ord("E"): "è", ord("F"): "ə́", ord("G"): "ɛ̀",
    ord("H"): "ɛ́", ord("I"): "ú", ord("J"): "œ̀", ord("K"): "œ́",
    ord("L"): "-", ord("M"): "ɲ", ord("N"): "ɔ́", ord("O"): "ò",
    ord("P"): "ó", ord("Q"): "æ̀", ord("R"): "é", ord("S"): "á",
    ord("T"): "ì", ord("U"): "ù", ord("V"): "ʌ́", ord("W"): "ǽ",
    ord("X"): "ɑ́", ord("Y"): "í", ord("Z"): "ɑ̀",ord("\\"): "ː",
    ord("^"): "ɡ", ord("_"): "ɥ",
}

# gaiji の変換規則
gaiji_rules = {
    ord("あ"): "☞", ord("え"): "∜10", ord("お"): "₵", ord("か"): "𝄐",
    ord("き"): "𝄪", ord("く"): "$", ord("こ"): "©", ord("せ"): "ͺ",
    ord("そ"): "卐", ord("た"): "V", ord("ち"): "ℵ", ord("の"): "1⅓",
    ord("は"): "2½", ord("亜"): "枘", ord("以"): "鄧", ord("伊"): "鈹",
    ord("位"): "苆", ord("哀"): "癤", ord("唖"): "痤", ord("圧"): "龕",
    ord("姐"): "晷", ord("姶"): "癭", ord("娃"): "炻", ord("安"): "瘙",
    ord("宛"): "鬐", ord("庵"): "嘈", ord("悪"): "禱", ord("愛"): "垜",
    ord("或"): "瘭", ord("扱"): "𨫤", ord("挨"): "蔲", ord("握"): "麬",
    ord("斡"): "鱝", ord("旭"): "簎", ord("暗"): "墩", ord("杏"): "煆",
    ord("案"): "痎", ord("梓"): "糝", ord("渥"): "皶", ord("穐"): "骶",
    ord("粟"): "跗", ord("絢"): "騸", ord("綾"): "楣", ord("芦"): "髁",
    ord("茜"): "搐", ord("葦"): "桛", ord("葵"): "獐", ord("虻"): "嗉",
    ord("袷"): "𥝱", ord("逢"): "窠", ord("闇"): "跑", ord("阿"): "埵",
    ord("鞍"): "蒴", ord("飴"): "橅", ord("鮎"): "姸", ord("鯵"): "蹰",
}

# name="000" の正規表現パターン
n000 = re.compile(r"^\d{3}$")

# name="A-0000" の正規表現パターン
nA0000 = re.compile(r"^[A-Z]-\d{4}$")

# onclick="jump()" の正規表現パターン
jump1 = re.compile(r"jump\('([^']*)','([^']*)'\)")

# onclick="openNewWin()" の正規表現パターン
jump2 = re.compile(r"openNewWin\('([^']*)','([^']*)'\)")

# onclick="openVerbTable()" の正規表現パターン
jump3 = re.compile(r"openVerbTable\('([^']*)'\)")

# -------------------------
# 補助関数
# -------------------------

def _translate_texts(elem, rules):
    for node in elem.iter():
        cls = node.get("class", "")
        if "gosi" in cls.split():
            pass # span.gosi の text はスキップ
        else:
            if node.text:
                node.text = node.text.translate(rules)
        if node.tail:
            node.tail = node.tail.translate(rules)

def replace_brackets(element):
    cls = element.get("class", "")
    # gosou の場合
    if "gosou" in cls.split():
        rules = [(r"\(\(", "〘"), (r"\)\)", "〙"),]
    # bunya の場合
    elif "bunya" in cls.split():
        rules = [(r"〔", "〚"), (r"〕", "〛"),]
    # それ以外
    else:
        rules = [(r"\(\(", "｟"), (r"\)\)", "｠"),
                 (r"《", "«"), (r"》", "»"),]
    # text と tail に適用
    if element.text:
        for pat, rep in rules:
            element.text = re.sub(pat, rep, element.text)
    if element.tail:
        for pat, rep in rules:
            element.tail = re.sub(pat, rep, element.tail)
    # 子要素にも再帰
    for child in element:
        replace_brackets(child)

# -------------------------
# メイン変換関数
# -------------------------

def convert_item(htm_path):
    parser = html.HTMLParser(encoding="shift-jis")
    tree = html.parse(htm_path, parser)
    body = tree.find(".//body")
    if body is None:
        raise ValueError(f"{htm_path} に <body> が見つかりません")

    # --- body.onload → id 抽出 ---
    onload = body.get("onload", "")
    m = re.search(r"'([^']+)'", onload)
    entry_id = m.group(1) if m else None

    # --- span.midasi → title 抽出 ---
    title_elem = body.xpath(".//*[@class='midasi']")
    entry_title = title_elem[0].text_content().strip() if title_elem else None

    # --- .hatuon 系 → d:pr="1" + 文字変換 ---
    for elem in body.xpath(".//*[contains(@class,'hatuon') or contains(@class,'phonetic')]"):
        elem.set(f"{{{NSMAP['d']}}}pr", "1")
        _translate_texts(elem, hatuon_rules)

    # --- .gaiji → 文字変換 ---
    for elem in body.xpath(".//*[@class='gaiji']"):
        _translate_texts(elem, gaiji_rules)

    # --- a name の変換 ---
    # 1. UI部品の a → 削除
    for a in body.xpath(".//a[@name='inyou1']|.//a[@name='yougo1']|.//a[@name='kanren1']|.//a[@name='info1']|.//a[contains(@name,'yourei_')]|.//a[contains(@name,'tyuki_')]"):
        a.getparent().remove(a)

    # 2. a name="page_top" → unwrap
    for a in body.xpath(".//a[@name='page_top']"):
        parent = a.getparent()
        idx = parent.index(a)
        # a.text を前に移す
        if a.text:
            if idx > 0:
                prev = parent[idx - 1]
                prev.tail = (prev.tail or "") + a.text
            else:
                parent.text = (parent.text or "") + a.text
        # 子要素を unwrap して親に移す
        for child in list(a):
            parent.insert(idx, child)
            idx += 1
        # a.tail を後に残す
        if a.tail:
            if idx > 0:
                prev = parent[idx - 1]
                prev.tail = (prev.tail or "") + a.tail
            else:
                parent.text = (parent.text or "") + a.tail
        # a 自体は削除
        parent.remove(a)

    # 3. a name="001", a name="A0001"
    for a in body.xpath(".//a[@name]"):
        name = a.get("name")
        # 3-1. name="012" タイプ → 「entryid_000」をつけて後続の td の id に
        if n000.match(name):
            tr = a.getparent().getparent() # a -> td -> tr
            sibs = list(tr.itersiblings(tag="tr"))
            if len(sibs) >= 1:
                target_tr = sibs[0] # 次の tr
                td = target_tr.find("./td")
                if td is not None:
                    if "id" in td.attrib:
                        raise ValueError(f"{td} には既に id があります")
                    td.set("id", entry_id + "_000" + name)
                    a.getparent().remove(a)
        # 3-2. name="A-0123" タイプ → 「entryid_」をつける
        elif nA0000.match(name):
            a.set("name", entry_id + "_" + name)
            # このタイプの a は次の処理で span#id のネストに変換される

    # 3-2b. （成句）内部に (a[name=id])+ を持つ span → span#id のネスト
    for span in body.xpath(".//span"):
        anchors = [a for a in span if a.tag == "a" and "name" in a.attrib]
        if not anchors:
            continue
        # 元の属性を保管
        original_attrib = dict(span.attrib)
        # テキストと a 以外を残す
        content = [c for c in span if not (c.tag == "a" and "name" in c.attrib)]
        if span.text and span.text.strip():
            content.insert(0, span.text)
        span.clear()
        # 元の属性を復元し id は上書き
        span.attrib.update(original_attrib)
        span.set("id", anchors[0].get("name"))
        parent = span
        for extra in anchors[1:]:
            new_span = etree.Element("span", id=extra.get("name"))
            parent.append(new_span)
            parent = new_span
        for item in content:
            if isinstance(item, str):
                if parent.text:
                    parent.text += item
                else:
                    parent.text = item
            else:
                parent.append(item)

    # --- onclick の変換 ---
    for el in body.xpath(".//*[@onclick]"):
        onclick = el.attrib.get("onclick", "")
        m1 = jump1.match(onclick)
        m2 = jump2.match(onclick)
        m3 = jump3.match(onclick)
        # span onclick="jump('A-01234','A001')"
        if m1 is not None:
            rid, anchor = m1.groups()
            # "012" タイプの anchor -> 「rid_000」をつける
            if n000.match(anchor):
                anchor = rid + "_000" + anchor
            # "A-0123" タイプの anchor -> 「rid_」をつける
            elif nA0000.match(anchor):
                anchor = rid + "_" + anchor
            # 同じ entry 内への anchor: 「a href="#anchor"」
            if rid == entry_id:
                href = f"#{anchor}" if anchor else ""
            # 別の entry への anchor: 「a href="x-dictionary:r:rid#anchor"」
            else:
                href = f"x-dictionary:r:{rid}" + (f"#{anchor}" if anchor else "")
        # span onclick="openNewWin(path.pdf,'ZUHAN'|'APPENDIX')"
        elif m2 is not None:
            refid, orig_type = m2.groups()
            refid = refid.replace("../../../zuhan/","_Zuhan-")
            refid = refid.replace("../../../appendix/","_Appendix-")
            refid = refid.replace(".pdf","")
            href = f"x-dictionary:r:{refid}"
        # input type="button" onclick="openVerbTable('A0123')"
        elif m3 is not None:
            conju_id = m3.group(1)
            href = f"x-dictionary:r:_Conju-{conju_id}"
        else:
            continue
        # a 要素を作成し、元の要素と置換
        a_tag = etree.Element("a", href=href)
        if m3 is not None:
            a_tag.text = "活用表"
        else:
            # 子ノード移動
            for child in list(el):
                a_tag.append(child)
            if el.text:
                if a_tag.text:
                    a_tag.text += el.text
                else:
                    a_tag.text = el.text
        el.getparent().replace(el, a_tag)

    # --- 不要な要素を削除 ---
    # a href="#page_top" → 削除
    for a in body.xpath(".//a[@href='#page_top']"):
        a.getparent().remove(a)

    # div.end_zone → 削除
    for div in body.xpath(".//div[@class='end_zone']"):
        div.getparent().remove(div)

    # UI部品の span (span.arrow, span.block_label) → 削除
    for sp in body.xpath(".//span[@class='arrow']|.//span[@class='block_label']"):
        sp.getparent().remove(sp)

    # 空の td 要素 → 削除
    for td in body.xpath(".//td[count(@*)=0 and not(node())]"):
        td.getparent().remove(td)
    
    # 空の tr 要素 → 削除
    for tr in body.xpath(".//tr[count(@*)=0 and not(node())]"):
        tr.getparent().remove(tr)

    # 括弧を置換
    replace_brackets(body)

    # --- <d:entry> 構築 ---
    entry = etree.Element(f"{{{NSMAP['d']}}}entry",
                          attrib={"id": entry_id,
                                  f"{{{NSMAP['d']}}}title": entry_title},
                          nsmap=NSMAP)
    for child in list(body):
        entry.append(child)

    return entry

# -------------------------
# コマンドライン実行用
# -------------------------

if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) != 3:
        print("Usage: python single_item_converter.py input.htm output.xml", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    d_entry = convert_item(input_path)
    tree = etree.ElementTree(d_entry)
    tree.write(output_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)
