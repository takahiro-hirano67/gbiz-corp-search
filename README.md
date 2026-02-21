## セットアップ手順

**1. 環境変数の設定**
```bash
cp .env.local.example .env.local
# .env.local に GBIZ_API_TOKEN=実際のトークン を記入
```

**2. ローカル起動**
```bash
npm install
npm run dev   # Next.js と FastAPI を同時起動
```

**3. Vercel へのデプロイ**
Vercel ダッシュボードの Environment Variables に `GBIZ_API_TOKEN` を追加してから push する。


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
├─ eslint.config.mjs
├─ next.config.ts
├─ package-lock.json
├─ package.json
├─ .env.local.example
├─ postcss.config.mjs
├─ public
│  ├─ file.svg
│  ├─ globe.svg
│  ├─ next.svg
│  ├─ vercel.svg
│  └─ window.svg
├─ README.md
├─ requirements.txt
├─ Tailwind.config.js
└─ tsconfig.json

```