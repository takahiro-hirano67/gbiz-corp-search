def translate_keys(data: any, mapping: dict) -> any:
    """キーを日本語に置換する再帰関数（結果取得/法人情報ノードより）"""
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if k == "meta-data":
                continue
            new_key = mapping.get(k, k)
            new_data[new_key] = translate_keys(v, mapping)
        return new_data
    elif isinstance(data, list):
        return [translate_keys(item, mapping) for item in data]
    else:
        return data


def to_markdown(data: any, level: int = 0) -> str:
    """辞書/リストをMarkdownに変換する関数（結果取得/法人情報ノードより）"""
    indent = "  " * level
    md = ""

    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                md += f"{indent}- **{k}**:\n{to_markdown(v, level + 1)}"
            elif v is not None:
                md += f"{indent}- **{k}**: {v}\n"
            else:
                md += f"{indent}- **{k}**: (なし)\n"

    elif isinstance(data, list):
        if not data:
            md += f"{indent}(データなし)\n"
        else:
            for i, item in enumerate(data):
                md += f"{indent}- *項目 {i + 1}*:\n{to_markdown(item, level + 1)}"
    else:
        md += f"{indent}{str(data)}\n"

    return md


def format_section(body: dict, item: dict) -> str:
    """
    1エンドポイント分のレスポンスをMarkdownセクションに整形する。
    結果取得/法人情報（コード実行）ノードの処理に相当。
    """
    convert_map = item["convert_map"]
    label_ja = item["label_ja"]
    label_en = item.get("label_en", "")

    if not body.get("hojin-infos") or len(body["hojin-infos"]) == 0:
        return f"### {label_ja}\n(データなし)\n"

    raw_data = dict(body["hojin-infos"][0])

    # 基本情報以外は共通ヘッダを削除
    if label_en != "basic":
        for key in ["corporate_number", "name", "location"]:
            raw_data.pop(key, None)

    translated_data = translate_keys(raw_data, convert_map)
    md_body = to_markdown(translated_data)

    return f"### {label_ja}\n\n{md_body.strip()}\n"


def build_full_markdown(
    corp_name: str,
    corp_num: str,
    corp_location: str,
    sections: list[str],
) -> str:
    """全セクションを結合して最終Markdownを生成する（出力テキスト整形テンプレートに相当）"""
    sections_text = "\n\n---\n\n".join(sections)

    return f"""# gBizINFOから企業の法人情報取得

## 対象企業

- **法人名**: {corp_name}
- **法人番号**: {corp_num}
- **本社所在地**: {corp_location}

## 取得結果

{sections_text}

---

## 補足: データの限界

- gBizINFO APIには全ての情報が記録されているわけではありません。
- また、APIにデータが反映されるのにも時差が発生します。
- 存在しないデータを根拠に判断せず、あくまで確認できる範囲を判断材料としてください。
"""