include env.make

# -------------------------
# 変数
# -------------------------

# 辞書の素材
DICT_NAME  := RoyalFJ
DICT_XML   := RoyalFJ.xml
DICT_CSS   := RoyalFJ.css
DICT_PLIST := RoyalFJ.plist

# このMakefile が存在するディレクトリ
MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# build_dict.sh 含むビルドツールの場所
BUILD_TOOL_BIN := bin

# build_dict.sh により作成された辞書データの一時的な置場
OBJ := objects
DICT_DEV_OBJ_DIR := $(MAKEFILE_DIR)/$(OBJ)
export DICT_DEV_KIT_OBJ_DIR

# 辞書データのインストール先
INSTALL_DIR := ${HOME}/Library/Dictionaries

# -------------------------
# コマンド用ルール
# -------------------------

.DEFAULT_GOAL = help

help: ## helpを表示する
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's,^Makefile:,,g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
.PHONY: help

# -------------------------
# CD-ROMデータの変換
# -------------------------

correctedItems/.dummy:
	uv run scripts/error_correction.py "$(ROYALFJ_ROYAL_DIR)/Contents/fr/itemPages" correctedItems
	@touch correctedItems/.dummy

indexes/.dummy:
	uv run scripts/batch_converter.py midasi "$(ROYALFJ_ROYAL_DIR)/Contents/fr/index/Midasi" indexes/Midasi/
	uv run scripts/batch_converter.py seiku  "$(ROYALFJ_ROYAL_DIR)/Contents/fr/index/Seiku"  indexes/Seiku/
	uv run scripts/batch_converter.py conju  "$(ROYALFJ_ROYAL_DIR)/Contents/fr/index/Conju"  indexes/Conju/
	@touch indexes/.dummy

entries/.dummy: correctedItems/.dummy
	uv run scripts/batch_converter.py item "$(ROYALFJ_ROYAL_DIR)/Contents/fr/itemPages" entries
	uv run scripts/batch_converter.py item correctedItems entries
	@touch entries/.dummy

verbTable/.dummy:
	uv run scripts/batch_converter.py verbTable "$(ROYALFJ_ROYAL_DIR)/Contents/fr/conju" verbTable
	@touch verbTable/.dummy

frontMatter/appendix/.dummy:
	@mkdir -p frontMatter
	uv run scripts/pdf_converter.py appendix "$(ROYALFJ_ROYAL_DIR)/Contents/appendix" frontMatter/ OtherResources/
	@touch frontMatter/appendix/.dummy

frontMatter/zuhan/.dummy:
	@mkdir -p frontMatter
	uv run scripts/pdf_converter.py zuhan "$(ROYALFJ_ROYAL_DIR)/Contents/zuhan" frontMatter/ OtherResources/
	@touch frontMatter/zuhan/.dummy

frontMatter/.dummy:
	@mkdir -p frontMatter
	uv run scripts/frontmatter_maker.py "$(ROYALFJ_ROYAL_DIR)/Contents/" frontMatter/
	@touch frontMatter/.dummy

correctedItems: correctedItems/.dummy ## 元の辞書データのエラーを訂正
indexes: indexes/.dummy ## 辞書の見出し語リスト .htm を .xml に1対1変換
entries: entries/.dummy ## 辞書の各項目 .htm を .xml に1対1変換
verbTable: verbTable/.dummy ## 活用表 .htm を .xml に1対1変換
appendix: frontMatter/appendix/.dummy ## 付録 .pdf を .xml に1対1変換
zuhan: frontMatter/zuhan/.dummy ## 図版 .pdf を .xml に1対1変換
frontMatter: frontMatter/.dummy ## 辞書の前付を作成
.PHONY: correctedItems indexes entries verbTable appendix zuhan frontMatter

# -------------------------
# データの合成
# -------------------------

main/main.xml: indexes/.dummy entries/.dummy
	uv run scripts/merge_index_entry.py indexes entries main/main.xml

$(DICT_XML): main/main.xml verbTable/.dummy frontMatter/.dummy frontMatter/appendix/.dummy frontMatter/zuhan/.dummy ## 見出し、項目本文、活用表を結合した XML データを作成
	uv run scripts/merge_dictionaries.py main verbTable frontMatter | xmllint --format - > "$(DICT_XML)"

# -------------------------
# 辞書のビルドとインストール
# -------------------------

# patch -b .orig を作成 -N 差分適用済であれば無視
$(BUILD_TOOL_BIN)/extract_referred_id.pl.orig:
	patch -b -N ./bin/extract_referred_id.pl < scripts/extract_referred_id.pl.patch

patch: $(BUILD_TOOL_BIN)/extract_referred_id.pl.orig ## Dictionary Development Kit にパッチを当てる
.PHONY: patch

all: $(OBJ) ## ビルドを実行する
$(OBJ): $(DICT_XML) $(DICT_CSS) $(DICT_PLIST) $(BUILD_TOOL_BIN)/extract_referred_id.pl.orig
	"$(BUILD_TOOL_BIN)/build_dict.sh" "$(DICT_NAME)" "$(DICT_XML)" "$(DICT_CSS)" "$(DICT_PLIST)"
.PHONY: all

install: $(OBJ) ## ビルドした辞書データを $(INSTALL_DIR) にコピーする
	@echo "Installing into $(INSTALL_DIR)."
	mkdir -p "$(INSTALL_DIR)"
	ditto --noextattr --norsrc "$(OBJ)/$(DICT_NAME).dictionary" "$(INSTALL_DIR)/$(DICT_NAME).dictionary"
	touch "$(INSTALL_DIR)"
	@echo "Install Done. Try Dictionary.app to test the new dictionary."
.PHONY: install

# -------------------------
# 掃除
# -------------------------

clean: ## 一時ファイルを削除する
	-/bin/rm -rf "$(OBJ)"
	-/bin/rm -rf "$(DICT_XML)"
	-/bin/rm -rf frontMatter OtherResources verbTable
	-/bin/rm -rf correctedItems indexes entries main
.PHONY: clean
