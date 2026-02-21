# api/index.py

import asyncio

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from api.gbiz.endpoints import get_endpoints
from api.gbiz.formatter import build_full_markdown, format_section

# ---------- APIキー取得 ----------


class Settings(BaseSettings):
    GBIZ_API_TOKEN: str

    class Config:
        env_file = ".env.local"


settings = Settings()

# ---------- アプリケーションのセットアップ ----------

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# gBizINFO APIのベースURL
GBIZ_BASE_URL = "https://api.info.gbiz.go.jp/hojin/v2/hojin"


# ヘッダー定義
def _get_headers() -> dict:
    token = settings.GBIZ_API_TOKEN
    if not token:
        raise HTTPException(
            status_code=500, detail="GBIZ_API_TOKEN が設定されていません"
        )
    return {
        "accept": "application/json",
        "X-hojinInfo-api-token": token,
    }


# ---------- リクエスト/レスポンス スキーマ ----------


class SearchRequest(BaseModel):
    corp_name: str


class Candidate(BaseModel):
    name: str
    location: str
    corporate_number: str


class SearchResponse(BaseModel):
    status: str  # "success" | "multiple" | "not_found"
    # successのとき
    markdown: str | None = None
    corporate_number: str | None = None
    corp_name: str | None = None
    corp_location: str | None = None
    url: str | None = None
    # multipleのとき
    message: str | None = None
    candidates: list[Candidate] | None = None


# ---------- エンドポイント ----------


# 動作チェック
@app.get("/api/py/healthcheck")
async def healthcheck():
    return {"status": "ok"}


# 検索実行
@app.post("/api/py/search/corp", response_model=SearchResponse)
async def search_corp(req: SearchRequest) -> SearchResponse:
    headers = _get_headers()
    corp_name = req.corp_name.strip()

    if not corp_name:
        raise HTTPException(status_code=400, detail="corp_name は必須です")

    # セッションを再利用してパフォーマンスを向上させる
    async with httpx.AsyncClient(timeout=15.0) as client:
        # --- 法人検索（法人番号を取得するため） ---
        resp = await client.get(
            url=f"{GBIZ_BASE_URL}?name={corp_name}&exist_flg=true&page=1&limit=100&metadata_flg=false",
            headers=headers,
        )

        # 見つからなかった場合
        if resp.status_code == 404:
            return SearchResponse(
                status="not_found",
                message=f"「{corp_name}」は見つかりませんでした。",
            )

        # 404以外のエラー（共通）
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"gBizINFO APIエラー: {resp.json().get('message', '不明なエラー')}",
            )

        body = resp.json()
        hojin_infos: list[dict] = body.get("hojin-infos", [])

        # --- 企業を1件に特定できたか判定 ---
        if len(hojin_infos) == 0:
            return SearchResponse(
                status="not_found",
                message=f"「{corp_name}」は見つかりませんでした。",
            )

        # 特定できなかった場合、[企業名, 所在地, 法人番号]の一覧を返す
        if len(hojin_infos) > 1:
            candidates = [
                Candidate(
                    name=h.get("name", ""),
                    location=h.get("location", ""),
                    corporate_number=h.get("corporate_number", ""),
                )
                for h in hojin_infos
            ]
            return SearchResponse(
                status="multiple",
                message=f"「{corp_name}」で{len(hojin_infos)}件見つかりました。対象の企業を選択してください。",
                candidates=candidates,
            )

        # --- 法人番号取得 ---
        hojin_info = hojin_infos[0]
        corp_num: str = hojin_info["corporate_number"]
        resolved_name: str = hojin_info.get("name", corp_name)
        corp_location: str = hojin_info.get("location", "")

        # --- 法人番号を基に、各エンドポイントを並行で取得 ---
        endpoints = get_endpoints()
        # 並行処理後の順序を保つための配列を準備
        sections: list[str] = [""] * len(endpoints)

        # APIサーバーへの負荷を考慮し、同時接続数を3に制限
        sem = asyncio.Semaphore(3)

        async def fetch_endpoint(index: int, item: dict):
            endpoint_path = item["endpoint"]
            async with sem:
                try:
                    ep_resp = await client.get(
                        url=f"{GBIZ_BASE_URL}/{corp_num}{endpoint_path}?metadata_flg=false",
                        headers=headers,
                    )
                    ep_body = (
                        ep_resp.json()
                        if ep_resp.status_code == 200
                        else {"hojin-infos": []}
                    )
                except Exception:
                    # 通信エラー時は空のデータを渡してフォールバック
                    ep_body = {"hojin-infos": []}

                # 整形結果を正しいインデックスに格納
                sections[index] = format_section(ep_body, item)
                # 次のリクエストとの間隔をわずかに空ける（負荷軽減用）
                await asyncio.sleep(0.1)

        # 全エンドポイントのタスクを生成して一斉に実行
        tasks = [fetch_endpoint(i, item) for i, item in enumerate(endpoints)]
        await asyncio.gather(*tasks)

    # --- 出力テキスト整形 ---
    markdown = build_full_markdown(
        corp_name=resolved_name,
        corp_num=corp_num,
        corp_location=corp_location,
        sections=sections,
    )
    gbiz_url = f"https://info.gbiz.go.jp/hojin/ichiran?hojinBango={corp_num}"

    return SearchResponse(
        status="success",
        markdown=markdown,
        corporate_number=corp_num,
        corp_name=resolved_name,
        corp_location=corp_location,
        url=gbiz_url,
    )
