// app/page.tsx

"use client";

import "@/styles/markdown_style.css"; // Markdown用のスタイル

import { AlertCircle, AlertTriangle, Building, Loader2 } from "lucide-react"; // アイコン
import { useRef, useState } from "react";

import CandidateList from "@/components/CandidateList"; // 検索結果（複数）表示コンポーネント
import ResultView from "@/components/ResultView"; // 検索結果（単体）表示コンポーネント
import SearchForm from "@/components/SearchForm"; // 検索フォームコンポーネント
import { Candidate, SearchResponse } from "@/types"; // 型定義

export default function CorporateSearchPage() {

    // State管理
    const [corpName, setCorpName] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<SearchResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    // スクロール管理＆検索ボタンフォーカス
    const inputRef = useRef<HTMLInputElement>(null);
    const resultRef = useRef<HTMLDivElement>(null);

    // 検索ハンドラ
    const handleSearch = async (nameOverride?: string) => {
        const name = nameOverride ?? corpName;
        if (!name.trim()) return;

        setIsLoading(true);
        setError(null);
        setResult(null); // 前回の結果をクリア

        try {
            const res = await fetch("/api/py/search/corp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ corp_name: name }),
            });

            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail ?? `エラー: ${res.status}`);
            }

            const data: SearchResponse = await res.json();
            setResult(data);

            setTimeout(() => {
                resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 100);
        } catch (e: unknown) {
            if (e instanceof Error) {
                setError(e.message);
            } else {
                setError("予期しないエラーが発生しました");
            }
        } finally {
            setIsLoading(false);
        }
    };

    // 候補選択時のハンドラ
    const handleSelectCandidate = (candidate: Candidate) => {
        // 企業名をフォームに入力して検索を実行する
        setCorpName(candidate.name);
        handleSearch(candidate.name);
    };

    // リセット処理
    const handleReset = () => {
        setCorpName("");
        setResult(null);
        setError(null);
        inputRef.current?.focus();
    };

    return (
        <div className="min-h-screen font-sans">
            {/* ヘッダー */}
            <header className="bg-white border-b border-slate-200 px-6 py-4">
                <div className="max-w-3xl mx-auto flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
                        <Building className="text-white" size={20} />
                    </div>
                    <div>
                        <h1 className="text-base font-semibold text-slate-800">企業情報検索</h1>
                        <p className="text-xs text-slate-400">gBizINFO API</p>
                    </div>
                </div>
            </header>

            <main className="max-w-3xl mx-auto px-6 py-10 space-y-8">
                {/* 検索フォーム */}
                <SearchForm
                    corpName={corpName}
                    setCorpName={setCorpName}
                    onSearch={() => handleSearch()}
                    isLoading={isLoading}
                    inputRef={inputRef}
                />

                {/* 検索中ローディング */}
                {isLoading && (
                    <div className="bg-white rounded-xl border border-slate-200 p-10 text-center">
                        <Loader2 className="w-8 h-8 animate-spin text-blue-500 mx-auto mb-3" />
                        <p className="text-sm text-slate-500">gBizINFO から情報を取得しています...</p>
                        <p className="text-xs text-slate-400 mt-1">
                            複数のエンドポイントを順次取得するため、しばらくお待ちください
                        </p>
                    </div>
                )}

                {/* エラー表示 */}
                {!isLoading && error && (
                    <div className="bg-red-50 border border-red-200 rounded-xl p-5 flex gap-3">
                        <AlertCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
                        <div>
                            <p className="text-sm font-medium text-red-700">エラーが発生しました</p>
                            <p className="text-sm text-red-600 mt-0.5">{error}</p>
                        </div>
                    </div>
                )}

                {/* 見つからなかった場合 */}
                {!isLoading && result?.status === "not_found" && (
                    <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 flex gap-3">
                        <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                        <p className="text-sm text-amber-700">{result.message}</p>
                    </div>
                )}

                <div ref={resultRef}>
                    {/* 複数候補表示 */}
                    {!isLoading && result?.status === "multiple" && result.candidates && (
                        <CandidateList
                            message={result.message!}
                            candidates={result.candidates}
                            onSelect={handleSelectCandidate} // 再検索関数を渡す
                        />
                    )}

                    {/* 検索結果表示 */}
                    {!isLoading && result?.status === "success" && (
                        <ResultView
                            result={result}
                            corpName={corpName}
                            onReset={handleReset} // リセット関数を渡す
                        />
                    )}
                </div>
            </main>
        </div>
    );
}