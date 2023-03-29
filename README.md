# hito-koto-diary
スプレッドシートで用意した日記に対して書き込みや読み込みを行うことができるCLI

## Usage
```
$ hitokoto --help
Usage: hitokoto [OPTIONS]

  ヒトコト日記 CLI

  ヒトコト日記として利用している Google Spreadsheet に対しての読み込み、書き込み操作を行う

Options:
  -t, --text TEXT                 書き込むテキスト
  -d, --date [%Y-%m-%d|%Y/%m/%d]  予定の取得日 (yyyy-mm-dd or yyyy/mm/dd)
                                  default:Today
  -c, --column [PRIVATE|WORK|MEMO]
                                  書き込むカラムを指定する
  -force, -f                      書き込み操作実行時に値の上書きを強制する
  --help                          Show this message and exit.
```

## Install
### スプレッドシートの準備
* このような形式のスプレッドシートを準備する
  * 月日は一年間列挙可能
* スプレッドシートのタブ名は'年'にすること
  * 例えば、2022年であれば'2022'

|月日|今日の一言|仕事の一言|メモ|
|---|---|---|---|
|2022/01/01(土)||||
|2022/01/02(日)||||
|......||||
|2022/12/31(土)||||

### 仮想環境構築
```zsh
$ pipenv install --dev
$ pipenv shell
```

### 環境変数設定
```zsh
$ cp src/hitokoto/config/.env.sample src/hitokoto/config/.env
$ vim .env
```
* .env内に必要な情報を記述する
  * SA_KEY_PATH: credentials.json のディレクトリパス(hito_koto_diary.pyからの相対パス)
  * SPREADSHEET_ID: 読み書きを行うスプレッドシートID

### サービスアカウントキーの作成
* [サービスアカウントの作成と管理](https://cloud.google.com/iam/docs/creating-managing-service-accounts?hl=ja#creating_a_service_account)
  * credentials.json をダウンロードし、上で指定したSA_KEY_PATHに保存
* スプレッドシートアクセスに使用するため、サービスアカウントを当該スプレッドシートの共有設定に追加し権限を与える

## 実行
### Local
```
$ python src/hitokoto/hito_koto_diary.py
```

### pip install
```
$ exit
$ pip install <path to pyproject.toml>
$ hitokoto
```

* pip install することでパッケージのバージョンが自動的に振られる
