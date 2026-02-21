from api.gbiz.keymap import get_keymaps


def get_endpoints() -> list[dict]:
    keymaps = get_keymaps()

    return [
        {
            "endpoint": "",
            "label_en": "basic",
            "label_ja": "法人基本情報",
            "convert_map": keymaps["basic_map"],
        },
        {
            "endpoint": "/certification",
            "label_en": "certification",
            "label_ja": "届出・認定情報",
            "convert_map": keymaps["certification_map"],
        },
        {
            "endpoint": "/commendation",
            "label_en": "commendation",
            "label_ja": "表彰情報",
            "convert_map": keymaps["commendation_map"],
        },
        {
            "endpoint": "/corporation",
            "label_en": "corporation",
            "label_ja": "事業所情報",
            "convert_map": keymaps["corporation_map"],
        },
        {
            "endpoint": "/finance",
            "label_en": "finance",
            "label_ja": "財務情報",
            "convert_map": keymaps["finance_map"],
        },
        {
            "endpoint": "/patent",
            "label_en": "patent",
            "label_ja": "特許情報",
            "convert_map": keymaps["patent_map"],
        },
        {
            "endpoint": "/procurement",
            "label_en": "procurement",
            "label_ja": "調達情報",
            "convert_map": keymaps["procurement_map"],
        },
        {
            "endpoint": "/subsidy",
            "label_en": "subsidy",
            "label_ja": "補助金情報",
            "convert_map": keymaps["subsidy_map"],
        },
        {
            "endpoint": "/workplace",
            "label_en": "workplace",
            "label_ja": "職場情報",
            "convert_map": keymaps["workplace_map"],
        },
    ]