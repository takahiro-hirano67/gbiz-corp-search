import time

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from api.gbiz.endpoints import get_endpoints
from api.gbiz.formatter import build_full_markdown, format_section


class Settings(BaseSettings):
    GBIZ_API_TOKEN: str

    class Config:
        env_file = ".env.local"


settings = Settings()

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

GBIZ_BASE_URL = "https://api.info.gbiz.go.jp/hojin/v2/hojin"


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
    # success
    markdown: str | None = None
    corporate_number: str | None = None
    corp_name: str | None = None
    corp_location: str | None = None
    url: str | None = None
    # multiple
    message: str | None = None
    candidates: list[Candidate] | None = None


# ---------- エンドポイント ----------


@app.get("/api/py/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.post("/api/py/search/corp", response_model=SearchResponse)
def search_corp(req: SearchRequest) -> SearchResponse:
    headers = _get_headers()
    corp_name = req.corp_name.strip()

    if not corp_name:
        raise HTTPException(status_code=400, detail="corp_name は必須です")

    # --- 法人検索（コード実行ノードに相当） ---
    resp = requests.get(
        url=f"{GBIZ_BASE_URL}?name={corp_name}&exist_flg=true&page=1&limit=100&metadata_flg=false",
        headers=headers,
        timeout=15,
    )

    if resp.status_code == 404:
        return SearchResponse(
            status="not_found",
            message=f"「{corp_name}」は見つかりませんでした。",
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"gBizINFO APIエラー: {resp.json().get('message', '不明なエラー')}",
        )

    body = resp.json()
    hojin_infos: list[dict] = body.get("hojin-infos", [])

    # --- 企業を特定できたか判定（IF/ELSEノードに相当） ---
    if len(hojin_infos) == 0:
        return SearchResponse(
            status="not_found",
            message=f"「{corp_name}」は見つかりませんでした。",
        )

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

    # --- 法人番号取得（コード実行ノードに相当） ---
    hojin_info = hojin_infos[0]
    corp_num: str = hojin_info["corporate_number"]
    resolved_name: str = hojin_info.get("name", corp_name)
    corp_location: str = hojin_info.get("location", "")

    # --- イテレーション（各エンドポイントを順次取得） ---
    endpoints = get_endpoints()
    sections: list[str] = []

    for item in endpoints:
        endpoint_path = item["endpoint"]
        ep_resp = requests.get(
            url=f"{GBIZ_BASE_URL}/{corp_num}{endpoint_path}?metadata_flg=false",
            headers=headers,
            timeout=15,
        )
        ep_body = ep_resp.json() if ep_resp.status_code == 200 else {"hojin-infos": []}
        sections.append(format_section(ep_body, item))
        time.sleep(0.6)  # 負荷軽減クールタイム（法人情報取得ノードより）

    # --- 出力テキスト整形（テンプレートノードに相当） ---
    markdown = build_full_markdown(
        corp_name=resolved_name,
        corp_num=corp_num,
        corp_location=corp_location,
        sections=sections,
    )
    gbiz_url = (
        f"https://info.gbiz.go.jp/hojin/ichiran?hojinBango={corp_num}"
    )

    return SearchResponse(
        status="success",
        markdown=markdown,
        corporate_number=corp_num,
        corp_name=resolved_name,
        corp_location=corp_location,
        url=gbiz_url,
    )
