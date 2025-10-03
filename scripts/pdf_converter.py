# /// script
# dependencies = [
# "lxml",
# "pdf2image",
# "tqdm",
# ]
# ///

"""
PDFフォルダ（appendix または zuhan）の List.htm を参照し、
PDFを1ページずつPNG化して OtherResources 以下に保存し、
各PDFごとに1つの <d:entry> を持つXMLを出力する。
"""

from lxml import etree, html
from pdf2image import convert_from_path
from tqdm import tqdm
from pathlib import Path
import sys
import os
import re

NSMAP = {"d": "http://www.apple.com/DTDs/DictionaryService-1.0.rng"}

def parse_list_htm(list_path):
    """List.htm を読み込み、(pdfファイル名, タイトル) のリストを返す"""
    parser = html.HTMLParser(encoding="shift-jis")
    tree = html.parse(str(list_path), parser)
    rows = tree.xpath("//tr")
    entries = []
    for tr in rows:
        a = tr.find(".//a")
        if a is not None and a.get("href"):
            pdf_file = a.get("href").strip()
            title = a.text_content().strip()
            entries.append((pdf_file, title))
    return entries

def pdf_to_images(pdf_path, output_dir, prefix, dpi=350):
    """PDFを1ページずつPNG化して output_dir に保存。保存パスのリストを返す"""
    output_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(str(pdf_path), dpi=dpi)
    img_paths = []
    for i, img in enumerate(images, start=1):
        img_name = f"{prefix}_{i:03d}.png"
        img_path = output_dir / img_name
        img.save(str(img_path), format="PNG")
        img_paths.append(img_path)
    return img_paths

def make_entry(entry_id, title, img_paths):
    """1PDF分の <d:entry> を作成"""
    entry = etree.Element(f"{{{NSMAP['d']}}}entry",
                          attrib={"id": entry_id, f"{{{NSMAP['d']}}}title": title},
                          nsmap=NSMAP)
    # index
    idx = etree.Element(f"{{{NSMAP['d']}}}index", attrib={f"{{{NSMAP['d']}}}value": title, f"{{{NSMAP['d']}}}priority": "2"})
    entry.append(idx)
    # img要素
    for img_path in img_paths:
        # xml 内では OtherResources 以下の相対パス
        rel_path = str(img_path).replace("OtherResources/", "")
        img_el = etree.Element("img", src=rel_path)
        entry.append(img_el)
    return entry

def process_folder(folder_name, input_root, output_xml_root, output_img_root):
    """appendix or zuhan フォルダを処理"""
    folder = input_root
    list_file = next(folder.glob(f"{folder_name}List.htm"), None)
    if list_file is None:
        raise FileNotFoundError(f"{folder_name}List.htm が {folder} に見つかりません")

    entries = parse_list_htm(list_file)
    if folder_name == "appendix":
        entries.append(("maegaki.pdf", "前付"))

    # 出力ディレクトリ
    other_res_dir = output_img_root / folder_name
    xml_out_dir = output_xml_root / folder_name
    xml_out_dir.mkdir(parents=True, exist_ok=True)

    for pdf_file, title in tqdm(entries, desc=f"Converting {folder_name} PDF", unit="file", dynamic_ncols=True):
        pdf_path = folder / pdf_file
        if not pdf_path.exists():
            print(f"PDFが存在しません: {pdf_path}", file=sys.stderr)
            continue
        # PDF→画像
        img_paths = pdf_to_images(pdf_path, other_res_dir, pdf_path.stem)
        # d:entry作成
        entry_id = f"_{folder_name.capitalize()}-{pdf_path.stem}"
        d_entry = make_entry(entry_id, title, img_paths)
        # XML出力
        xml_file = xml_out_dir / f"{pdf_path.stem}.xml"
        tree = etree.ElementTree(d_entry)
        tree.write(str(xml_file), encoding="UTF-8", xml_declaration=True, pretty_print=True)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python pdf_converter.py [appendix|zuhan] input_dir output_xml_dir output_img_dir", file=sys.stderr)
        sys.exit(1)

    folder_name = sys.argv[1].lower()
    if folder_name not in ("appendix", "zuhan"):
        print("引数は 'appendix' か 'zuhan' を指定してください", file=sys.stderr)
        sys.exit(1)

    input_root = Path(sys.argv[2])
    output_xml_root = Path(sys.argv[3])
    output_img_root = Path(sys.argv[4])

    process_folder(folder_name, input_root, output_xml_root, output_img_root)
