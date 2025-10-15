# /// script
# dependencies = [
#  "lxml",
#  "tqdm",
# ]
# ///

from lxml import etree
from tqdm import tqdm
from pathlib import Path
import sys
import re

# converter 関数を import
from single_verbtable_converter import convert_verbtable as convert_verbtable
from single_index_converter import convert_index as convert_index
from single_item_converter  import convert_item  as convert_item

def convert_all(mode, input_root, output_root):
    input_root = Path(input_root)
    output_root = Path(output_root)

    # --- ファイル収集 ---
    all_files = list(input_root.rglob("*.htm"))

    if mode == "seiku":
        # "OLD" または "NEW" をサブフォルダ名に含むものは除外
        files = [
            f for f in all_files
            if not any(part in ("OLD", "NEW") for part in f.relative_to(input_root).parts)
        ]
    elif mode == "item":
        # ファイル名が A-00001.htm 形式に一致するものだけ
        pattern = re.compile(r"^[A-Z]-\d{5}\.htm$", re.IGNORECASE)
        files = [f for f in all_files if pattern.match(f.name)]
    elif mode == "verbTable":
        # ファイル名が A0001.htm 形式に一致するものだけ
        pattern = re.compile(r"^[A-Z]\d{4}\.htm$", re.IGNORECASE)
        files = [f for f in all_files if pattern.match(f.name)]
    else: # midasi, conju
        files = all_files

    # --- 変換処理 ---
    for htm_file in tqdm(files, desc=f"Converting ({mode})", unit="file", dynamic_ncols=True):
        if mode == "item":
            entry = convert_item(htm_file)
            if entry is None:
                raise ValueError(f"No entry returned for {htm_file}")
            tree = etree.ElementTree(entry)
        elif mode == "verbTable":
            entry = convert_verbtable(htm_file)
            if entry is None:
                raise ValueError(f"No entry returned for {htm_file}")
            tree = etree.ElementTree(entry)
        else: # midasi, seiku, conju
            dictionary = convert_index(htm_file, mode)
            tree = etree.ElementTree(dictionary)

        # 出力パスを入力と同じ構造で再現
        rel_path = htm_file.relative_to(input_root)
        out_path = output_root / rel_path.with_suffix(".xml")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        tree.write(out_path, encoding="UTF-8", xml_declaration=True, pretty_print=True)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python batch_converter.py mode input_dir output_dir", file=sys.stderr)
        print("mode: midasi | seiku | conju | item | verbTable", file=sys.stderr)
        sys.exit(1)

    mode_arg = sys.argv[1]
    if mode_arg not in ("midasi", "seiku", "conju", "item", "verbTable"):
        print(f"Invalid mode: {mode_arg}", file=sys.stderr)
        sys.exit(1)

    convert_all(mode_arg, sys.argv[2], sys.argv[3])
