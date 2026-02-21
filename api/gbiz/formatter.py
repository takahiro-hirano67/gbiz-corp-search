# api/gbiz/formatter.py

from typing import Any


def translate_keys(data: Any, mapping: dict) -> Any:
    """キーを日本語に置換する再帰関数"""

    # 辞書の場合
    if isinstance(data, dict):
        new_data = {}
        # 各キーをループ
        for k, v in data.items():
            # "meta-data" の除外
            if k == "meta-data":
                continue
            # マップにあれば日本語に置換、なければ元のキーを使用
            new_key = mapping.get(k, k)
            # 値にも再帰的に translate_keys を適用
            new_data[new_key] = translate_keys(v, mapping)
        return new_data

    # リストの場合
    elif isinstance(data, list):
        # リスト内の全要素に対して再帰処理
        return [translate_keys(item, mapping) for item in data]

    # それ以外の場合（文字列・数字など）
    else:
        return data


def to_markdown(data: Any, level: int = 0) -> str:
    """辞書/リストをMarkdownに変換する関数"""

    # 階層レベルごとにインデント（半角スペース4つ）を増やす
    indent = "    " * level
    # Markdown
    md = ""

    # 辞書の場合
    if isinstance(data, dict):
        for k, v in data.items():
            # 値が`更に`構造体（dict or list）の場合
            if isinstance(v, (dict, list)):
                md += f"{indent}- **{k}**:\n{to_markdown(v, level + 1)}"
            # 値が単純な文字列/数値の場合
            elif v is not None:
                md += f"{indent}- **{k}**: {v}\n"
            # Noneの場合
            else:
                md += f"{indent}- **{k}**: (なし)\n"

    # リストの場合
    elif isinstance(data, list):
        # 空リストの場合の表示
        if not data:
            md += f"{indent}(データなし)\n"
        # 要素ありの場合（番号付きで整理）
        else:
            for i, item in enumerate(data):
                md += f"{indent}- *項目 {i + 1}*:\n{to_markdown(item, level + 1)}"
    # その他の型（そのまま文字列化）
    else:
        md += f"{indent}{str(data)}\n"

    return md


def format_section(body: dict, item: dict) -> str:
    """
    1エンドポイント分のレスポンスをMarkdownセクションに整形する。
    """
    # オブジェクトから情報取得
    convert_map = item["convert_map"]  # キー変換マップ
    label_ja = item["label_ja"]  # 日本語ラベル（セクション見出し）
    label_en = item.get("label_en", "")  # 英語ラベル（処理用の識別子）

    # データ存在Check
    if not body.get("hojin-infos") or len(body["hojin-infos"]) == 0:
        return f"### {label_ja}\n(データなし)\n"

    raw_data = dict(body["hojin-infos"][0])

    # 基本情報以外は共通ヘッダを削除
    if label_en != "basic":
        # 削除したいキーのリスト
        for key in ["corporate_number", "name", "location"]:
            raw_data.pop(key, None)  # キーがあれば削除、なければ無視

    # キーを日本語に置換
    translated_data = translate_keys(raw_data, convert_map)

    # Markdown生成
    md_body = to_markdown(translated_data)

    # セクション完成
    return f"### {label_ja}\n\n{md_body.strip()}\n"


def build_full_markdown(
    corp_name: str,
    corp_num: str,
    corp_location: str,
    sections: list[str],
) -> str:
    """全セクションを結合して最終Markdownを生成する"""
    sections_text = "\n\n---\n\n".join(sections)  # セクション間に区切り線を入れる

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

# 補足の箇所の意図: LLMへの文脈用
# データが空だった際に「活動していない」のようなネガティブな評価をさせないため。
# gBizINFOに登録されていないだけで、実態とは異なる可能性があるため、空データを根拠に推測するのはNG