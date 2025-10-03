# royal-frja-conv
macOSの 辞書.app で『ロワイヤル仏和中辞典』を使う

## 概要
『ロワイヤル仏和中辞典 第2版』（旺文社、2005）付属のCD-ROM版辞書を、macOSの標準辞書アプリで利用できる形式に変換する。

## 準備物
- 『ロワイヤル仏和中辞典 第2版』付録CD-ROM（「Windows版 Ver 1.01」で動作確認）
- `uv`（Rust 製の python マネージャ https://docs.astral.sh/uv/ ）

## 変換手順
### 1. Additional Tools for Xcode 最新版を入手

Downloads - Apple Developer  
https://developer.apple.com/download/all/?q=Xcode

※Apple Developer アカウント（無料）が必要

`Utilities/Dictionary Development Kit` をローカルにコピーし、以後このフォルダ内で作業する。

### 2. ツールをダウンロードして配置
``` sh
git clone https://github.com/metasta/royal-frja-conv.git
```

`Dictionary Development Kit/bin` と同じ階層に `royal-frja-conv` フォルダを配置する。
```
Dictionary Development Kit
└── bin
└── documents
└── project_templates
└── royal-frja-conv
    └── Makefile
    └── RoyalFJ.plist
    └── RoyalFJ.css
    └── scripts
└── samples
```

### 3. Makefile の編集
CD-ROMをマウントし、CD-ROMデータにアクセスできるパスを確認する。

`Makefile` を開き、CD-ROMデータ内の `Royal` フォルダのパスを `ROYALFJ_ROYAL_DIR` に指定する。

```Makefile
# -------------------------
# 使い方 + 設定項目
# -------------------------
# 
# 1. パスを設定する
# 『ロワイヤル仏和中辞典 第2版 CD-ROM版』の内部にある「Royal」ディレクトリを指定
ROYALFJ_ROYAL_DIR := /Volumes/Royal_FJ/Royal
#
...
```

### 4. 変換実行
```sh
make install
```
を実行すると、辞書データが変換され、インストールされる。

※`make install` により変換された辞書データは `~/Library/Dictionaries/RoyalFJ.dictionary` に配置される。  
アンインストールの際はこの `RoyalFJ.dictionary` を削除する。

### 5. 起動
「辞書.app」を起動し、「辞書 > 設定...（command+,）」から「ロワイヤル仏和中辞典」を追加。

## 機能
CD-ROM版辞書の機能をできる範囲で移植した。
- 通常の見出し語での検索
- 成句での検索（記事中の該当部分をハイライト）
- 活用形での検索（活用形を入力して原形がヒットする）
- 記事内のリンクから、別記事や図版へのジャンプ
- 動詞活用表［各動詞の活用表を別記事扱いで収録した。例：avoir →「avoir 活用表」］
- 前付・図版一覧・付録一覧［メニューの「移動 > 前付/後付」からアクセスできる］

## 免責条項
無償、無保証のプログラムです。各自の責任でご利用ください。
