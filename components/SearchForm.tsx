// components/SearchForm.tsx

// 検索の入力とボタン、ローディング状態を受け取って描画

import { Loader2, Search } from "lucide-react";
import { RefObject } from "react";

type SearchFormProps = {
    corpName: string;
    setCorpName: (name: string) => void;
    onSearch: () => void;
    isLoading: boolean;
    inputRef: RefObject<HTMLInputElement | null>;
};

export default function SearchForm({
    corpName,
    setCorpName,
    onSearch,
    isLoading,
    inputRef,
}: SearchFormProps) {
    return (
        <section className="bg-white rounded-xl border border-slate-200 shadow-xs p-6">
            <label className="block text-sm font-medium text-slate-700 mb-2">
                企業名
                <span className="ml-1 text-red-500">*</span>
            </label>
            <div className="flex gap-3">
                <input
                    ref={inputRef}
                    type="text"
                    value={corpName}
                    onChange={(e) => setCorpName(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && onSearch()}
                    placeholder="例: 株式会社良品計画"
                    className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 placeholder:text-slate-400 transition"
                />
                <button
                    onClick={onSearch}
                    disabled={isLoading || !corpName.trim()}
                    className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed transition flex items-center gap-2 shrink-0"
                >
                    {isLoading ? (
                        <>
                            <Loader2 className="w-4 h-4 animate-spin" />
                            検索中
                        </>
                    ) : (
                        <>
                            <Search className="w-4 h-4" />
                            検索
                        </>
                    )}
                </button>
            </div>
            <p className="mt-2 text-xs text-slate-400">
                同名企業が複数ある場合は候補一覧から選択してください
            </p>
        </section>
    );
}