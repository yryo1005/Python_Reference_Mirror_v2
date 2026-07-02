# Python Reference Mirror

[Python 公式ドキュメント](https://docs.python.org/3/)を、インターネットなしで手元の PC から閲覧できるようにしたものです。

チュートリアル、言語リファレンス、ライブラリリファレンス、C API、FAQ など、公式サイトと同等の内容が `docs/` フォルダに含まれています。**GitHub から clone するだけで使えます。スクレイピングは不要です。**

> この README は **Windows ユーザー向け** に書いています（利用者の大半が Windows のため）。Mac / Linux 向けの手順は末尾の「その他の OS」を参照してください。

---

## この README でできること

Python を少し触ったことがある方向けに、次の流れを説明します。

1. **Git** のインストール
2. **Visual Studio Code（VS Code）** でリポジトリを clone する
3. **ローカルサーバー** を起動してドキュメントを閲覧する

---

## 必要なもの


| ソフトウェア             | 用途             | 入手先                                                       |
| ------------------ | -------------- | --------------------------------------------------------- |
| **Python 3.10 以上** | サーバー起動・仮想環境    | [python.org/downloads](https://www.python.org/downloads/) |
| **Git**            | リポジトリの clone   | [git-scm.com](https://git-scm.com/download/win)           |
| **VS Code**（推奨）    | 編集・ターミナル・clone | [code.visualstudio.com](https://code.visualstudio.com/)   |


> ドキュメント本体はリポジトリに同梱されているため、**閲覧時にインターネット接続は不要**です（clone 時のみ必要）。

---

## 手順 0: Python をインストールする（未インストールの場合）

1. [python.org/downloads](https://www.python.org/downloads/) から **Windows installer (64-bit)** をダウンロードします。
2. インストーラーを起動し、**最初の画面で「Add python.exe to PATH」に必ずチェック**を入れてから **Install Now** をクリックします。
3. インストール後、**PowerShell** または **コマンドプロンプト** を新しく開き、次で確認します。

```powershell
python --version
```

`Python 3.10` 以上と表示されれば OK です。

---

## 手順 1: Git をインストールする

1. [git-scm.com/download/win](https://git-scm.com/download/win) を開き、**64-bit Git for Windows Setup** をダウンロードします。
2. インストーラーは基本的に **Next のまま進めて問題ありません**。特に変更しなくてよい主な項目は次のとおりです。
  - **Adjusting your PATH environment** → **Git from the command line and also from 3rd-party software**（推奨・デフォルト）
  - **Choosing the default editor** → お好みで（VS Code を選ぶと便利）
3. インストール完了後、**PowerShell またはコマンドプロンプトを一度閉じて開き直し**、次で確認します。

```powershell
git --version
```

`git version 2.x.x` のように表示されれば OK です。

### Git が認識されない場合

- ターミナルを **開き直す**（PATH が反映されます）
- それでもダメな場合は PC を再起動してから再度 `git --version` を試してください

---

## 手順 2: VS Code でリポジトリを clone する

### 2-1. VS Code をインストールする

1. [code.visualstudio.com](https://code.visualstudio.com/) から **Windows** 版をダウンロードしてインストールします。
2. 初回起動時に **Japanese Language Pack** のインストールを促されたら、日本語化したい場合はインストールしてください（任意）。

### 2-2. clone する

1. VS Code を起動します。
2. メニュー ファイル → フォルダを開くから、任意のフォルダを開きます。
3. メニュー **ターミナル → 新しいターミナル**（ショートカット: `Ctrl + ``）
4. **ターミナルに下記のコマンドを入力し，実行します**

```
git clone https://github.com/yryo1005/Python_Reference_Mirror.git
```

clone 後、エクスプローラーに `Python_Reference_Mirror` フォルダが表示され、`docs/` や `main.py` などが見えれば成功です。

---

## 手順 3: 仮想環境を作る（初回のみ）

プロジェクト専用の Python 環境を作ります。手順2の直後の状態(**VS Code でフォルダを開いた状態)**で進めてください。

### 3-1. カレントディレクトリを変更する

**ターミナルに下記のコマンドを入力し、実行します。**

```
cd Python_Reference_Mirror
```

ターミナル下部に `Python_Reference_Mirror` がカレントディレクトリになっていることを確認します。

### 3-2. 仮想環境の作成と有効化

**PowerShell**（VS Code のデフォルト）の場合:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**コマンドプロンプト** の場合:

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

成功すると、プロンプトの先頭に `(.venv)` と表示されます。

### PowerShell で「スクリプトの実行が無効」と出る場合

次のエラーが出たとき:

```
.venv\Scripts\Activate.ps1 : このシステムではスクリプトの実行が無効になっているため...
```

**現在のユーザーだけ** 実行を許可します（PowerShell で 1 回だけ実行）:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

その後、もう一度 `.venv\Scripts\Activate.ps1` を実行してください。

---

## 手順 4: ローカルサーバーを起動する

仮想環境を有効にした状態（プロンプトに `(.venv)` が付いている状態）で、VS Code のターミナルで次を実行します。

```powershell
python main.py serve
```

正常に起動すると、次のような表示が出ます。

```
Local URL: http://127.0.0.1:8000/index.html
Press Ctrl+C to stop.
```

ブラウザが自動で開き、Python 公式ドキュメントのトップページが表示されます。

### ブラウザが自動で開かない場合

Edge や Chrome のアドレスバーに次の URL を入力してください。

```
http://127.0.0.1:8000/index.html
```

### サーバーを止める方法

VS Code のターミナルで `**Ctrl + C**` を押してください。

### 次回以降の起動（2 回目以降）

1. VS Code で `Python_Reference_Mirror` フォルダを開く
2. ターミナルを開く
3. 仮想環境を有効化 → サーバー起動

```powershell
.venv\Scripts\Activate.ps1
python main.py serve
```

---

## よくある操作


| やりたいこと         | 方法                                  |
| -------------- | ----------------------------------- |
| 言語リファレンスを読む    | 左のメニューから **Language Reference** を選ぶ |
| ライブラリリファレンスを読む | 左のメニューから **Library Reference** を選ぶ  |
| キーワードで検索する     | 右上の **Search** から検索（オフライン可）         |
| 別のポートで起動する     | `python main.py serve --port 8080`  |
| ブラウザを自動で開かない   | `python main.py serve --no-browser` |


---

## うまくいかないとき（Windows）

`**python` が認識されない / Microsoft Store が開く**

→ Python インストール時に **Add python.exe to PATH** にチェックを入れ忘れた可能性があります。Python を再インストールするか、[python.org](https://www.python.org/downloads/) から入れ直してください。

`**No module named ...` と出る（例: `bs4`）**

→ 手順 3 の `pip install -r requirements.txt` を実行してください。プロンプトに `(.venv)` が付いていても、別の Python が使われていることがあります。次で確認します。

```powershell
python -c "import sys; print(sys.executable)"
pip install -r requirements.txt
```

パスに `.venv` が含まれていなければ、仮想環境を有効化してから再度 `pip install` してください。確実に動かすには次の方法も使えます。

```powershell
.venv\Scripts\python.exe main.py serve
```

**ポートが使用中と出る**

→ 別ポートを指定します。

```powershell
python main.py serve --port 8080
```

`**index.html not found` と出る**

→ `docs/` フォルダが存在するか確認してください。clone が途中で失敗していないか、フォルダを正しく開いているか確認します。

**ファイアウォールの警告**

→ 初回起動時に Windows ファイアウォールが表示された場合、**プライベートネットワーク** で Python を許可すればローカル（127.0.0.1）からの閲覧ができます。インターネット公開はされません。

---

## プロジェクト構成

```
Python_Reference_Mirror/
├── main.py                 # 起動用スクリプト
├── requirements.txt        # 依存パッケージ
├── docs/                   # Python 公式ドキュメント（同梱）
└── python_doc_mirror/      # サーバー・スクレイパー本体
```

---

## 注意事項

- ドキュメント内の外部リンク（GitHub、PyPI など）は、オフラインでは開けません。
- ドキュメントの内容は [PSF License](https://docs.python.org/3/license.html) に従います。

---

## ライセンス

このツール自体のコードは自由に利用できます。同梱ドキュメントの利用については Python Software Foundation のライセンスに従ってください。

---

## 上級者向け: ドキュメントの再取得（スクレイピング）

リポジトリに含まれる `docs/` は、公開時点の公式ドキュメントです。**最新版に更新したい場合**や、**自分で取得し直したい場合**に使います。

```powershell
python main.py scrape
```

`docs/` に HTML・CSS・JavaScript・ソースファイルなどが保存されます。初回は数分程度かかります。中断しても `.mirror_state.json` から再開できます。

### 主なオプション


| オプション         | デフォルト                        | 説明            |
| ------------- | ---------------------------- | ------------- |
| `--base-url`  | `https://docs.python.org/3/` | 取得元 URL       |
| `--output`    | `docs`                       | 保存先ディレクトリ     |
| `--workers`   | `8`                          | 並列ダウンロード数     |
| `--delay`     | `0.05`                       | リクエスト間隔（秒）    |
| `--no-resume` | —                            | 進捗を無視して最初から取得 |


例:

```powershell
python main.py scrape --workers 4 --delay 0.1
```

公式サイトへの過度な負荷を避けるため、`--delay` でリクエスト間隔を調整してください。

---

## 上級者向け: ファイル確認（status）

ミラーの取得状況を確認するコマンドです。通常の閲覧では不要です。

```powershell
python main.py status
```

ダウンロード済みファイル数、失敗した URL の有無、サーバー起動の可否などを表示します。


| オプション          | デフォルト                | 説明               |
| -------------- | -------------------- | ---------------- |
| `--dir`        | `docs`               | 確認するドキュメントディレクトリ |
| `--state-file` | `.mirror_state.json` | 進捗ファイルのパス        |


---

## その他の OS（Mac / Linux）

### 必要なもの

- Python 3.10 以上
- Git
- ターミナル

### clone

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