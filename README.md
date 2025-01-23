# レシピ検索アプリ

食材を入力すると、その食材を使用したレシピを検索し、日本語で表示するWebアプリケーションです。

## 機能

- 複数の食材からレシピを検索
- レシピ名、材料、作り方を日本語で表示
- レシピの写真表示
- 最大3件のレシピを表示

## 技術スタック

- Python 3.x
- Flask (Webフレームワーク)
- TheMealDB API (レシピデータベース)
- Google Cloud Translate API (翻訳機能)

## セットアップ

1. 必要なパッケージのインストール:
```bash
pip install flask requests python-dotenv google-cloud-translate
```

2. 環境変数の設定:
- `.env`ファイルを作成し、以下の内容を設定:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-credentials.json
```

3. Google Cloud Translateの認証情報:
- Google Cloud Consoleで認証情報を作成
- 取得したJSONファイルを保存し、環境変数で指定したパスに配置

## 使い方

1. アプリケーションの起動:
```bash
python app.py
```

2. ブラウザで以下のURLにアクセス:
```
http://localhost:5000
```

3. 検索ボックスに食材をカンマ区切りで入力（例：`玉ねぎ,じゃがいも`）

## 処理フロー

アプリケーションの処理フローは以下のフローチャートで表現されています：

[フローチャートを表示](./flowchart.md)

## 注意事項

- Google Cloud Translate APIの利用には課金が発生する可能性があります
- TheMealDB APIは英語のレシピのみ対応しています
- 翻訳結果は機械翻訳のため、完全な精度は保証されません

## ライセンス

MIT License
