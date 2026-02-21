// types/index.ts

// 複数のファイルで使い回す型を定義

// 検索結果が複数だった場合の型
export type Candidate = {
    name: string;
    location: string;
    corporate_number: string;
};

// 検索結果（単体）の型
export type SearchResponse = {
    status: "success" | "multiple" | "not_found";
    // success時
    markdown?: string;
    corporate_number?: string;
    corp_name?: string;
    corp_location?: string;
    url?: string;
    // multiple時
    message?: string;
    candidates?: Candidate[];
};