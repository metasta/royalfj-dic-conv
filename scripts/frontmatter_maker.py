# /// script
# dependencies = [
#  "lxml",
# ]
# ///

from lxml import etree, html
import re
import sys
from pathlib import Path


NSMAP = {"d": "http://www.apple.com/DTDs/DictionaryService-1.0.rng"}

def make_frontmatter(input_dir, output_dir):
    htm_path = input_dir / "help" / "help.htm"
    parser = html.HTMLParser(encoding="shift-jis")
    tree = html.parse(htm_path, parser)
    syomei = tree.xpath(".//div[@class='syomei']")[0]
    if syomei is None:
        raise ValueError(f"{htm_path} に div.syomei が見つかりません")
    entry = etree.Element(f"{{{NSMAP['d']}}}entry",
                          attrib={"id": "_FrontMatter",
                                  f"{{{NSMAP['d']}}}title": "目次"},
                          nsmap=NSMAP)
    entry.append(syomei)
    contents = [
        ("x-dictionary:r:_Appendix-maegaki", "前付"),
        ("x-dictionary:r:_FrontMatter-zuhanList", "図版一覧"),
        ("x-dictionary:r:_FrontMatter-appendixList", "付録一覧"),
    ]
    for href, text in contents:
        p = etree.Element("p")
        a = etree.Element("a",attrib={"href": href})
        a.text = text
        entry.append(p)
        p.append(a)
    return entry

def convert_list_htm(folder_name, input_dir, output_dir):
    htm_path = input_dir / folder_name / (folder_name + "List.htm")
    parser = html.HTMLParser(encoding="shift-jis")
    tree = html.parse(htm_path, parser)
    body = tree.find(".//body")
    if body is None:
        raise ValueError(f"{htm_path} に <body> が見つかりません")
    # id 除去
    for el in body.xpath(".//*[@id]"):
        del(el.attrib["id"])
    # a href を置換
    for a in body.xpath(".//a[@href]"):
        a.attrib["href"] = f"x-dictionary:r:_{folder_name.capitalize()}-" + a.attrib["href"].replace(".pdf","")
    title_dict = {"zuhan":"図版一覧", "appendix":"付録一覧",}
    # d:entry 構築
    entry = etree.Element(f"{{{NSMAP['d']}}}entry",
                          attrib={"id": f"_FrontMatter-{folder_name}List",
                                  f"{{{NSMAP['d']}}}title": title_dict[folder_name]},
                          nsmap=NSMAP)
    for child in list(body):
        entry.append(child)
    return entry

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python frontmatter_maker.py input_contents_dir output_xml_dir", file=sys.stderr)
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    frontMatter  = make_frontmatter(input_dir, output_dir)
    zuhanList    = convert_list_htm("zuhan", input_dir, output_dir)
    appendixList = convert_list_htm("appendix", input_dir, output_dir)

    etree.ElementTree(frontMatter).write(str(output_dir / "frontMatter.xml"), encoding="UTF-8", xml_declaration=True, pretty_print=True)
    etree.ElementTree(zuhanList).write(str(output_dir / "zuhanList.xml"), encoding="UTF-8", xml_declaration=True, pretty_print=True)
    etree.ElementTree(appendixList).write(str(output_dir / "appendixList.xml"), encoding="UTF-8", xml_declaration=True, pretty_print=True)
