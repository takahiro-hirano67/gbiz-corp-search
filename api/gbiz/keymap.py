# api/gbiz/keymap.py

def get_keymaps() -> dict:

    # ==========================================
    # 共通: メタデータ (Common Meta-data)
    # ※各情報のオブジェクト内に共通して含まれる定義
    # ==========================================

    common_metadata_map = {
        "data_quality": "データ品質",
        "import_frequency": "データ取込頻度",
        "key_field": "キー情報",
        "last_acquisition_date": "最終取得日",
        "last_update_date": "最終更新日",
        "source": "出典元"
    }

    # ==========================================
    # 1. 法人基本情報 (Basic)
    # ==========================================

    basic_map = {
        "corporate_number": "法人番号",
        "name": "法人名",
        "name_en": "法人名英語",
        "location": "本社所在地",
        "status": "ステータス",
        "postal_code": "郵便番号",
        "kana": "法人名フリガナ",
        "kind": "法人種別",
        "founding_year": "創業年",
        "date_of_establishment": "設立年月日",
        "close_cause": "登記記録の閉鎖等の事由",
        "close_date": "登記記録の閉鎖等年月日",
        "employee_number": "従業員数",
        "company_url": "企業ホームページ",
        "company_size_male": "企業規模詳細(男性)",
        "company_size_female": "企業規模詳細(女性)",
        "business_summary": "事業概要",
        "aggregated_year": "訂正区分",
        "update_date": "更新年月日",
        "representative_name": "法人代表者名",
        "process": "処理区分",
        "capital_stock": "資本金",
        "qualification_grade": "全省庁統一資格の資格等級",
        "industry": "業種",
        "business_items": "全省庁統一資格の営業品目",

        # --- meta-data (Root) ---
        # 法人基本情報の直下にあるメタデータオブジェクトのキー
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 2. 届出・認定情報 (Certification)
    # ==========================================

    certification_map = {
        "certification": "届出・認定リスト", # 親要素
        # --- certification items ---
        "title": "届出認定等",
        "category": "部門",
        "target": "対象",
        "government_departments": "府省",
        "date_of_approval": "認定日",

        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 3. 表彰情報 (Commendation)
    # ==========================================

    commendation_map = {
        "commendation": "表彰リスト", # 親要素
        # --- commendation items ---
        "title": "表彰名",
        "category": "部門",
        "target": "受賞対象",
        "government_departments": "府省",
        "date_of_commendation": "年月日",
        "note": "備考",
        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 4. 事業所情報 (Corporation)
    # ==========================================

    corporation_map = {
        "corporation-info": "事業所リスト", # 親要素 (ハイフン注意)
        # --- corporation-info items ---
        "corporation_name": "事業所名",
        "corporation_name_furigana": "事業所名フリガナ",
        "corporation_location": "事業所所在地",
        "corporation_location_furigana": "事業所所在地フリガナ",
        "insured_number": "被保険者数",
        "loss_date": "全喪年月日",

        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 5. 財務情報 (Finance)
    # ==========================================

    finance_map = {
        "finance": "財務情報詳細", # 親要素
        # --- finance (Root) ---
        "accounting_standards": "会計基準",
        "fiscal_year_cover_page": "事業年度",

        # 内部オブジェクトのキー
        "management_index": "財務指標",
        "major_shareholders": "大株主",

        # --- management_index (財務) ---
        "period": "回次",
        "net_sales_summary_of_business_results": "売上高",
        "net_sales_summary_of_business_results_unit_ref": "売上高(単位)",
        "ordinary_income_loss_summary_of_business_results": "経常利益又は経常損失(△)",
        "ordinary_income_loss_summary_of_business_results_unit_ref": "経常利益又は経常損失(△)(単位)",
        "net_income_loss_summary_of_business_results": "当期純利益又は当期純損失(△)",
        "net_income_loss_summary_of_business_results_unit_ref": "当期純利益又は当期純損失(△)(単位)",
        "total_assets_summary_of_business_results": "総資産額",
        "total_assets_summary_of_business_results_unit_ref": "総資産額(単位)",
        "net_assets_summary_of_business_results": "純資産額",
        "net_assets_summary_of_business_results_unit_ref": "純資産額(単位)",
        "capital_stock_summary_of_business_results": "資本金",
        "capital_stock_summary_of_business_results_unit_ref": "資本金(単位)",
        "number_of_employees": "従業員数",
        "number_of_employees_unit_ref": "従業員数(単位)",
        "gross_operating_revenue_summary_of_business_results": "営業総収入",
        "gross_operating_revenue_summary_of_business_results_unit_ref": "営業総収入（単位）",
        "operating_revenue1_summary_of_business_results": "営業収益",
        "operating_revenue1_summary_of_business_results_unit_ref": "営業収益（単位）",
        "operating_revenue2_summary_of_business_results": "営業収入",
        "operating_revenue2_summary_of_business_results_unit_ref": "営業収入（単位）",
        "ordinary_income_summary_of_business_results": "経常収益",
        "ordinary_income_summary_of_business_results_unit_ref": "経常収益（単位）",
        "net_premiums_written_summary_of_business_results_ins": "正味収入保険料",
        "net_premiums_written_summary_of_business_results_ins_unit_ref": "正味収入保険料（単位）",

        # --- major_shareholders (大株主) ---
        "name_major_shareholders": "氏名又は名称",
        "shareholding_ratio": "発行済株式総数に対する所有株式数の割合",

        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 6. 特許情報 (Patent)
    # ==========================================

    patent_map = {
        "patent": "特許・商標リスト", # 親要素

        # --- patent items ---
        "patent_type": "特許/意匠/商標",
        "title": "発明の名称(等)/意匠に係る物品/表示用商標",
        "application_date": "出願年月日",
        "registration_number": "登録番号",
        "url": "文献固定アドレス",

        # --- classifications (分類) ---
        "classifications": "分類",

        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 7. 調達情報 (Procurement)
    # ==========================================

    procurement_map = {
        "procurement": "調達実績リスト", # 親要素

        # --- procurement items ---
        "title": "事業名",
        "government_departments": "府省",
        "date_of_order": "受注日",
        "amount": "金額",
        "note": "備考",

        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 8. 補助金情報 (Subsidy)
    # ==========================================

    subsidy_map = {
        "subsidy": "補助金交付リスト", # 親要素

        # --- subsidy items ---
        "title": "補助金等",
        "target": "対象",
        "government_departments": "府省",
        "date_of_approval": "認定日",
        "amount": "金額",

        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    # ==========================================
    # 9. 職場情報 (Workplace)
    # ==========================================

    workplace_map = {
        "workplace_info": "職場情報詳細", # 親要素

        # 内部オブジェクトのキー
        "base_infos": "勤務基本情報",
        "compatibility_of_childcare_and_work": "育児・仕事の両立支援",
        "women_activity_infos": "女性活躍推進情報",

        # --- base_infos (勤務基本情報) ---
        "average_age": "従業員の平均年齢",
        "average_continuous_service_years": "正社員の平均継続勤務年数",
        "average_continuous_service_years_Male": "平均継続勤務年数-男性",
        "average_continuous_service_years_Female": "平均継続勤務年数-女性",
        "average_continuous_service_years_type": "平均継続勤務年数-範囲",
        "month_average_predetermined_overtime_hours": "月平均所定外労働時間",
        
        # --- compatibility_of_childcare_and_work (育児・仕事の両立に関する情報) ---
        "number_of_maternity_leave": "育児休業対象者数（女性）",
        "maternity_leave_acquisition_num": "育児休業取得者数（女性）",
        "number_of_paternity_leave": "育児休業対象者数（男性）",
        "paternity_leave_acquisition_num": "育児休業取得者数（男性）",

        # --- women_activity_infos (女性の活躍に関する情報) ---
        "female_share_of_manager": "女性管理職人数",
        "gender_total_of_manager": "管理職全体人数（男女計）",
        "female_share_of_officers": "女性役員人数",
        "gender_total_of_officers": "役員全体人数（男女計）",
        "female_workers_proportion": "労働者に占める女性労働者の割合",
        "female_workers_proportion_type": "労働者に占める女性労働者の割合-範囲",

        # --- meta-data ---
        "meta-data": "メタデータ",
        **common_metadata_map
    }

    return {
        "basic_map": basic_map,
        "certification_map": certification_map,
        "commendation_map": commendation_map,
        "corporation_map": corporation_map,
        "finance_map": finance_map,
        "patent_map": patent_map,
        "procurement_map": procurement_map,
        "subsidy_map": subsidy_map,
        "workplace_map": workplace_map,
    }