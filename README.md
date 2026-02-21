# gBizINFO 企業情報検索

gBizINFO API から法人情報を取得し、日本語 Markdown として出力するWebアプリです。  
取得した情報を LLM に渡すことで、企業分析への活用を目的としています。

[アプリへのリンク（Vercel）](https://gbiz-corp-search.vercel.app/)

## 概要

企業名を入力すると、gBizINFO API の複数エンドポイントから情報を取得し、読みやすい日本語 Markdown 形式で表示します。出力結果はコピーまたはファイルダウンロードが可能です。

**取得できる情報**

| カテゴリ       | 内容                                          |
| -------------- | --------------------------------------------- |
| 法人基本情報   | 法人名・所在地・従業員数・代表者名・資本金 等 |
| 財務情報       | 売上高・純利益・総資産・大株主 等             |
| 特許情報       | 特許・意匠・商標の登録情報                    |
| 補助金情報     | 補助金交付の実績                              |
| 調達情報       | 政府調達の受注実績                            |
| 届出・認定情報 | 各府省による認定・届出                        |
| 表彰情報       | 各府省による表彰実績                          |
| 事業所情報     | 事業所名・所在地 等                           |
| 職場情報       | 平均年齢・育児休業取得率・女性活躍推進情報 等 |

## 実装のポイント

### LLMフレンドリーなデータ変換＆日本語キーマップによる変換

gBizINFO API のレスポンスは英語のキー名で返されます。本アプリでは、英語キーを日本語に変換するマッピングテーブル（`api/gbiz/keymap.py`）を独自に定義し、出力を日本語 Markdown に変換しています。

このマッピングは **gBizINFO 公式の Swagger UI 記載の定義に準拠**して作成しています。英語キーのまま LLM に渡すと解釈がブレるケースがあるため、公式定義に沿った日本語に変換することで、LLM による企業分析の精度向上を図っています。

```python
# 例: api/gbiz/keymap.py
basic_map = {
    "corporate_number": "法人番号",
    "net_sales_summary_of_business_results": "売上高",
    "representative_name": "法人代表者名",
    ...
}
```

### 最新バージョンに対応

2026年1月26日にリニューアルしたAPIの仕様に対応しています。

REST API （v1）--> REST API （v2）

### APIの並行処理と負荷制御

外部API（特に政府系）への負荷を考慮した設計。

`api/index.py` にて、gBizINFOの複数エンドポイント(計9種)を叩く際に `asyncio.gather` で並行処理しつつ、
`asyncio.Semaphore(3)` で同時接続数を制御し、さらに `await asyncio.sleep(0.1)` で間隔を空けている。


## 技術スタック

| レイヤー       | 技術                                                |
| -------------- | --------------------------------------------------- |
| フロントエンド | Next.js 16 (App Router) / TypeScript / Tailwind CSS |
| バックエンド   | FastAPI / Python                                    |
| Markdown 表示  | react-markdown                                      |
| デプロイ       | Vercel（単一プロジェクト）                          |

## ディレクトリ構成

```
.
├── api/                    # FastAPI アプリ
│   ├── index.py            # エントリポイント・APIエンドポイント定義
│   └── gbiz/
│       ├── keymap.py       # 英語→日本語 キーマッピング
│       ├── endpoints.py    # gBizINFO エンドポイント定義
│       └── formatter.py    # Markdown 整形ロジック
│
├── app/                    # Next.js App Router
│   ├── layout.tsx
│   ├── page.tsx            # 企業検索ページ
│   └── globals.css
│
├── next.config.ts          # /api/py/* → FastAPI へのリワイト設定
├── requirements.txt        # Python 依存パッケージ
└── .env.local.example      # 環境変数テンプレート
```

## セットアップ

### 前提条件

- Node.js 18 以上
- Python 3.11 以上
- gBizINFO API トークン（[gBizINFO 各種利用申請画面](https://info.gbiz.go.jp/hojin/various_registration/form)より取得）

### ローカル起動

```bash
# 1. リポジトリのクローン
git clone <repository-url>
cd <repository-name>

# 2. 環境変数の設定
cp .env.local.example .env.local
# .env.local を編集して GBIZ_API_TOKEN を記入

# 3. Python 仮想環境の作成
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 4. Node.js パッケージのインストール
npm install

# 5. 開発サーバーの起動
npm run dev
```

`http://localhost:3000` でアプリが起動します。

### Vercel へのデプロイ

1. GitHub リポジトリを Vercel に接続
2. Vercel ダッシュボード → Settings → Environment Variables に `GBIZ_API_TOKEN` を追加
3. `main` ブランチへ push

## 参考

- [gBizINFO 経済産業省](https://info.gbiz.go.jp/hojin/Top)
- [gBizINFO API](https://content.info.gbiz.go.jp/api/index.html)
- [国税庁 法人番号公表サイト](https://www.houjin-bangou.nta.go.jp/)

## ディレクトリ構造


```
gbiz-corp-search
├─ api
│  ├─ gbiz
│  │  ├─ endpoints.py
│  │  ├─ formatter.py
│  │  ├─ keymap.py
│  │  └─ __init__.py
│  └─ index.py
├─ app
│  ├─ favicon.ico
│  ├─ globals.css
│  ├─ layout.tsx
│  └─ page.tsx
├─ components
│  ├─ CandidateList.tsx
│  ├─ ResultView.tsx
│  └─ SearchForm.tsx
├─ eslint.config.mjs
├─ next.config.ts
├─ package-lock.json
├─ package.json
├─ postcss.config.mjs
├─ README.md
├─ repomix-output.xml
├─ requirements.txt
├─ styles
│  └─ markdown_style.css
├─ tailwind.config.js
├─ tsconfig.json
└─ types
   └─ index.ts

```