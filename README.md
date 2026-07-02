# Python Reference Mirror

[Python 公式ドキュメント](https://docs.python.org/3/)を、インターネットなしで手元の PC から閲覧できるようにしたものです。

チュートリアル、言語リファレンス、ライブラリリファレンス、C API、FAQ など、公式サイトと同等の内容をローカルで閲覧できます。**初回起動時に公式アーカイブ（zip）をダウンロードして展開します。** 2 回目以降はオフラインで利用できます。

> この README は **Windows ユーザー向け** に書いています（利用者の大半が Windows のため）。Linux 向けの手順は末尾の「Linux」を参照してください。

---

## この README でできること

Python を少し触ったことがある方向けに、次の流れを説明します。

1. **Git** のインストール
2. **コマンドプロンプト** でリポジトリを clone する
3. **ローカルサーバー** を起動してドキュメントを閲覧する

---

## 必要なもの


| ソフトウェア             | 用途           | 入手先                                                       |
| ------------------ | ------------ | --------------------------------------------------------- |
| **Python 3.10 以上** | サーバー起動・仮想環境  | [python.org/downloads](https://www.python.org/downloads/) |
| **Git**            | リポジトリの clone | [git-scm.com](https://git-scm.com/download/win)           |


> **閲覧時**はインターネット接続は不要です。**初回起動時のみ**、公式ドキュメントの zip をダウンロードします（clone 時にも GitHub へのアクセスが必要です）。

---

## 手順 0: Python をインストールする（未インストールの場合）

1. [python.org/downloads](https://www.python.org/downloads/) から **Windows installer (64-bit)** をダウンロードします。
2. インストーラーを起動し、**最初の画面で「Add python.exe to PATH」に必ずチェック**を入れてから **Install Now** をクリックします。
3. インストール後、**コマンドプロンプト** を新しく開き、次で確認します。

```cmd
python --version
```

`Python 3.10` 以上と表示されれば OK です。

---

## 手順 1: Git をインストールする

1. [git-scm.com/download/win](https://git-scm.com/download/win) を開き、**64-bit Git for Windows Setup** をダウンロードします。
2. インストーラーは基本的に **Next のまま進めて問題ありません**。特に変更しなくてよい主な項目は次のとおりです。
  - **Adjusting your PATH environment** → **Git from the command line and also from 3rd-party software**（推奨・デフォルト）
3. インストール完了後、**コマンドプロンプトを一度閉じて開き直し**、次で確認します。

```cmd
git --version
```

`git version 2.x.x` のように表示されれば OK です。

### Git が認識されない場合

- コマンドプロンプトを **開き直す**（PATH が反映されます）
- それでもダメな場合は PC を再起動してから再度 `git --version` を試してください

---

## 手順 2: コマンドプロンプトでリポジトリを clone する

1. **コマンドプロンプト** を開きます（スタートメニューで「cmd」と検索 → **コマンドプロンプト**）。
2. clone 先のフォルダへ移動します（例: デスクトップ）。

```cmd
cd %USERPROFILE%\Desktop
```

1. 次のコマンドを入力して実行します。

```cmd
git clone https://github.com/yryo1005/Python_Reference_Mirror_v2.git
```

1. clone 後、フォルダを開き `Python_Reference_Mirror_v2` の中に `main.py` や `requirements.txt` があることを確認します。

---

## 手順 3: 仮想環境を作る（初回のみ）

プロジェクト専用の Python 環境を作ります。手順 2 の直後、**コマンドプロンプト** で進めてください。

### 3-1. カレントディレクトリを変更する

```cmd
cd Python_Reference_Mirror_v2
```

プロンプトの行に `Python_Reference_Mirror_v2` が含まれていることを確認します。

### 3-2. 仮想環境の作成と有効化

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

成功すると、プロンプトの先頭に `(.venv)` と表示されます。

---

## 手順 4: ローカルサーバーを起動する

仮想環境を有効にした状態（プロンプトに `(.venv)` が付いている状態）で、**同じコマンドプロンプト** で次を実行します。

```cmd
python main.py serve
```

正常に起動すると、次のような表示が出ます。

```
Local URL: http://127.0.0.1:8000/ja/index.html
Press Ctrl+C to stop.
```

ブラウザが自動で開き、**日本語版** Python 公式ドキュメントのトップページが表示されます。初回は zip のダウンロードと展開のため、数分かかることがあります。

### ブラウザが自動で開かない場合

Edge や Chrome のアドレスバーに次の URL を入力してください。

```
http://127.0.0.1:8000/ja/index.html
```

英語版は次の URL です。

```
http://127.0.0.1:8000/index.html
```

ページ上部の **Language** メニューからも English / 日本語 を切り替えられます。

### サーバーを止める方法

コマンドプロンプトで **Ctrl + C** を押してください。

### 次回以降の起動（2 回目以降）

1. **コマンドプロンプト** を開く
2. プロジェクトフォルダへ移動する
3. 仮想環境を有効化 → サーバー起動

```cmd
cd %USERPROFILE%\Desktop\Python_Reference_Mirror
.venv\Scripts\activate
python main.py serve
```

（clone した場所に合わせて `cd` のパスを変更してください。）

---

## よくある操作


| やりたいこと         | 方法                                             |
| -------------- | ---------------------------------------------- |
| 言語リファレンスを読む    | 左のメニューから **言語リファレンス**（Language Reference）を選ぶ   |
| ライブラリリファレンスを読む | 左のメニューから **ライブラリリファレンス**（Library Reference）を選ぶ |
| キーワードで検索する     | 右上の **検索**（Search）から検索（オフライン可）                 |
| 英語版に切り替える      | ページ上部の **Language** → **English**              |
| 別のポートで起動する     | `python main.py serve --port 8080`             |
| ブラウザを自動で開かない   | `python main.py serve --no-browser`            |


---

## うまくいかないとき（Windows）

`**python` が認識されない / Microsoft Store が開く**

→ Python インストール時に **Add python.exe to PATH** にチェックを入れ忘れた可能性があります。Python を再インストールするか、[python.org](https://www.python.org/downloads/) から入れ直してください。

`**No module named ...` と出る（例: `bs4`）**

→ 手順 3 の `pip install -r requirements.txt` を実行してください。プロンプトに `(.venv)` が付いていても、別の Python が使われていることがあります。次で確認します。

```cmd
python -c "import sys; print(sys.executable)"
pip install -r requirements.txt
```

パスに `.venv` が含まれていなければ、仮想環境を有効化してから再度 `pip install` してください。確実に動かすには次の方法も使えます。

```cmd
.venv\Scripts\python.exe main.py serve
```

**ポートが使用中と出る**

→ 別ポートを指定します。

```cmd
python main.py serve --port 8080
```

`**index.html not found` と出る**

→ 初回起動時の zip ダウンロード・展開が失敗していないか確認してください。`archives/` フォルダと `docs/`、`docs-ja/` フォルダが作成されているか、インターネット接続がある状態で再度 `python main.py serve` を試してください。

**ファイアウォールの警告**

→ 初回起動時に Windows ファイアウォールが表示された場合、**プライベートネットワーク** で Python を許可すればローカル（127.0.0.1）からの閲覧ができます。インターネット公開はされません。

---

## プロジェクト構成

```
Python_Reference_Mirror/
├── main.py                 # 起動用スクリプト
├── requirements.txt        # 依存パッケージ
├── archives/               # ダウンロードした zip（初回起動時に作成）
├── docs/                   # 英語ドキュメント（初回起動時に展開）
├── docs-ja/                # 日本語ドキュメント（初回起動時に展開）
└── python_doc_mirror/      # サーバー本体
```

---

## 注意事項

- ドキュメント内の外部リンク（GitHub、PyPI など）は、オフラインでは開けません。移動できないリンクは薄い色で表示されます。
- ドキュメントの内容は [PSF License](https://docs.python.org/3/license.html) に従います。

---

## ライセンス

このツール自体のコードは自由に利用できます。同梱ドキュメントの利用については Python Software Foundation のライセンスに従ってください。

---

## Linux

### 必要なもの

- Python 3.10 以上
- Git
- ターミナル

### clone

ターミナルを開き、次を実行します。

```bash
git clone https://github.com/yryo1005/Python_Reference_Mirror.git
cd Python_Reference_Mirror
```

### 仮想環境（初回のみ）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### サーバー起動

```bash
python main.py serve
```

`python: command not found` の場合は `python3 main.py serve` を試してください。

ブラウザで `http://127.0.0.1:8000/ja/index.html` が開きます（初回は zip のダウンロードにインターネット接続が必要です）。

### 次回以降の起動

```bash
cd Python_Reference_Mirror
source .venv/bin/activate
python main.py serve
```

