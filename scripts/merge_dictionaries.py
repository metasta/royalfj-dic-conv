# /// script
# dependencies = [
# "lxml",
# "tqdm",
# ]
# ///

from lxml import etree
from tqdm import tqdm
from pathlib import Path
import argparse
import sys

"""
引数として、辞書データ(d:directory または d:entry)の入ったディレクトリを任意個指定
全てのディレクトリ内の辞書をmergeした1つの辞書(d:directory)を標準出力に書き出す
"""
def main():
    NSMAP = {"d": "http://www.apple.com/DTDs/DictionaryService-1.0.rng"}

    parser = argparse.ArgumentParser(
        description="Merge multipile dictionary directories."
    )
    parser.add_argument(
        "directories",
        nargs="+",
        type=Path,
        help="Paths to directories to process."
    )

    def process_dir(directory):
        xml_files = Path(directory).rglob("*.xml")
        for xml_file in tqdm(xml_files, desc=f"Merging {directory}", unit="file", dynamic_ncols=True):
            tree = etree.parse(str(xml_file))
            doc_root = tree.getroot()
            # doc_root 自身が d:entryか、doc_root 自身は d:dictionary でその子が d:entry か
            entries = [doc_root] if doc_root.tag.endswith("entry") else doc_root.findall("./{*}entry")

            for entry in entries:
                entry_id = entry.get("id")
                if entry_id not in entries_by_id:
                    # 既存 entry なし → 単に append
                    root.append(entry)
                    entries_by_id[entry_id] = entry
                else:
                    # 既存 entry あり → 既存 entry に属性値と内容をマージ
                    existing_entry = entries_by_id[entry_id]
                    title = entry.get(f"{{{NSMAP['d']}}}title")
                    # d:title 属性があれば既存 entry にも同じ値を設定
                    if title is not None:
                        existing_entry.set(f"{{{NSMAP['d']}}}title", title)
                    # 子要素をマージ
                    for child in entry:
                        if child.tag.endswith("index"):
                            # d:index のときは既存エントリーに同じ d:index があるか確認
                            if not any(
                                existing_child.tag == child.tag and dict(existing_child.attrib) == dict(child.attrib)
                                for existing_child in existing_entry
                            ):
                                # 重複がなかった時のみ append
                                existing_entry.append(child)
                        else:
                            # d:index 以外の要素はそのまま append
                            existing_entry.append(child)

    args = parser.parse_args()
    root = etree.Element(f"{{{NSMAP['d']}}}dictionary", nsmap=NSMAP)
    entries_by_id = {}
    for directory in args.directories:
        if not directory.is_dir():
            print(f"{directory} is not a directory, skipped",file=sys.stderr)
            continue
        process_dir(directory)

    # entries_by_id を利用して d:entry を id 昇順ソート
    sorted_entries = [entries_by_id[k] for k in sorted(entries_by_id.keys())]
    root[:] = sorted_entries

    # 標準出力に書き出す
    etree.ElementTree(root).write(sys.stdout.buffer, encoding="utf-8",
                                  pretty_print=True, xml_declaration=True)


if __name__ == "__main__":
    main()