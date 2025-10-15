# royalfj-dic-conv
macOSの 辞書.app で『ロワイヤル仏和中辞典』を使う

## 概要
『ロワイヤル仏和中辞典 第2版』（旺文社、2005）付属のCD-ROM版辞書を、macOSの標準辞書アプリで利用できる形式に変換する。

## 準備物
- 『ロワイヤル仏和中辞典 第2版』付録CD-ROM（「Windows版 Ver 1.01」で動作確認）
- uv（Rust 製の python マネージャ https://docs.astral.sh/uv/ ）

## 変換手順

### 1. ダウンロード
``` sh
git clone https://github.com/metasta/royalfj-dic-conv.git
```

### 2. Additional Tools for Xcode を入手

Downloads - Apple Developer  
https://developer.apple.com/download/all/?q=Additional%20Tools%20for%20Xcode

※ Apple Developer アカウント（無料）が必要

`Utilities/Dictionary Development Kit/` 下にある `bin/` フォルダを、  
**先ほど作成した `royalfj-dic-conv` フォルダの直下にコピー**する。

### 3. パスの指定
CD-ROMをマウントする。

`env.make` を開き、`ROYALFJ_ROYAL_DIR` にCD-ROM内部の `Royal/` フォルダのパスを指定する。

### 4. 変換実行
```sh
make install
```
を実行すると、辞書データが変換され、インストールされる。

※ 辞書をビルドする過程で、辞書内リンクの処理を修正するパッチが Dictionary Development Kit に適用される。

※ `make install` により変換された辞書データは `~/Library/Dictionaries/RoyalFJ.dictionary/` に配置される。  
辞書をアンインストールする際はこの `RoyalFJ.dictionary/` を手動で削除する。

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
