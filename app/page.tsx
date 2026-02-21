"use client";

import { useState, useRef } from "react";
import ReactMarkdown from "react-markdown";

type Candidate = {
    name: string;
    location: string;
    corporate_number: string;
};

type SearchResponse = {
    status: "success" | "multiple" | "not_found";
    markdown?: string;
    corporate_number?: string;
    corp_name?: string;
    corp_location?: string;
    url?: string;
    message?: string;
    candidates?: Candidate[];
};

export default function CorporateSearchPage() {
    const [corpName, setCorpName] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<SearchResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const inputRef = useRef<HTMLInputElement>(null);
    const resultRef = useRef<HTMLDivElement>(null);

    const handleSearch = async (nameOverride?: string) => {
        const name = nameOverride ?? corpName;
        if (!name.trim()) return;

        setIsLoading(true);
        setError(null);
        setResult(null);

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
        } catch (e: any) {
            setError(e.message ?? "予期しないエラーが発生しました");
        } finally {
            setIsLoading(false);
        }
    };

    const handleSelectCandidate = (candidate: Candidate) => {
        setCorpName(candidate.name);
        handleSearch(candidate.name);
    };

    const handleReset = () => {
        setCorpName("");
        setResult(null);
        setError(null);
        inputRef.current?.focus();
    };

    const handleDownload = () => {
        if (!result?.markdown) return;
        const blob = new Blob([result.markdown], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${result.corp_name ?? corpName}_企業情報.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const handleCopy = () => {
        if (result?.markdown) navigator.clipboard.writeText(result.markdown);
    };

    return (
        <div className="min-h-screen bg-slate-50 font-sans">
            {/* ヘッダー */}
            <header className="bg-white border-b border-slate-200 px-6 py-4">
                <div className="max-w-3xl mx-auto flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                    </div>
                    <div>
                        <h1 className="text-base font-semibold text-slate-800">企業情報検索</h1>
                        <p className="text-xs text-slate-400">gBizINFO API</p>
                    </div>
                </div>
            </header>

            <main className="max-w-3xl mx-auto px-6 py-10 space-y-8">

                {/* 検索フォーム */}
                <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
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
                            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                            placeholder="例: 株式会社良品計画"
                            className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm
                            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                            placeholder:text-slate-400 transition"
                        />
                        <button
                            onClick={() => handleSearch()}
                            disabled={isLoading || !corpName.trim()}
                            className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg
                            hover:bg-blue-700 disabled:opacity-40 disabled:cursor-not-allowed
                            transition flex items-center gap-2 shrink-0"
                        >
                            {isLoading ? (
                                <>
                                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                                    </svg>
                                    検索中
                                </>
                            ) : (
                                <>
                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 11A6 6 0 105 11a6 6 0 0012 0z" />
                                    </svg>
                                    検索
                                </>
                            )}
                        </button>
                    </div>
                    <p className="mt-2 text-xs text-slate-400">
                        同名企業が複数ある場合は候補一覧から選択してください
                    </p>
                </section>

                {/* ローディング表示 */}
                {isLoading && (
                    <div className="bg-white rounded-xl border border-slate-200 p-10 text-center">
                        <svg className="w-8 h-8 animate-spin text-blue-500 mx-auto mb-3" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                        </svg>
                        <p className="text-sm text-slate-500">gBizINFO から情報を取得しています...</p>
                        <p className="text-xs text-slate-400 mt-1">複数のエンドポイントを順次取得するため、しばらくお待ちください</p>
                    </div>
                )}

                {/* エラー表示 */}
                {!isLoading && error && (
                    <div className="bg-red-50 border border-red-200 rounded-xl p-5 flex gap-3">
                        <svg className="w-5 h-5 text-red-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12A9 9 0 113 12a9 9 0 0118 0z" />
                        </svg>
                        <div>
                            <p className="text-sm font-medium text-red-700">エラーが発生しました</p>
                            <p className="text-sm text-red-600 mt-0.5">{error}</p>
                        </div>
                    </div>
                )}

                {/* 見つからなかった場合 */}
                {!isLoading && result?.status === "not_found" && (
                    <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 flex gap-3">
                        <svg className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12A9 9 0 113 12a9 9 0 0118 0z" />
                        </svg>
                        <p className="text-sm text-amber-700">{result.message}</p>
                    </div>
                )}

                {/* 複数候補 */}
                {!isLoading && result?.status === "multiple" && result.candidates && (
                    <section ref={resultRef}>
                        <div className="mb-4 bg-amber-50 border border-amber-200 rounded-xl p-4 flex gap-3 items-start">
                            <svg className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12A9 9 0 113 12a9 9 0 0118 0z" />
                            </svg>
                            <p className="text-sm text-amber-800">{result.message}</p>
                        </div>
                        <div className="grid sm:grid-cols-2 gap-3">
                            {result.candidates.map((c) => (
                                <button
                                    key={c.corporate_number}
                                    onClick={() => handleSelectCandidate(c)}
                                    className="bg-white border border-slate-200 rounded-xl p-5 text-left
                                hover:border-blue-400 hover:shadow-md transition-all group"
                                >
                                    <p className="font-semibold text-slate-800 group-hover:text-blue-600 transition-colors text-sm mb-2">
                                        {c.name}
                                    </p>
                                    <p className="text-xs text-slate-500 flex items-start gap-1 mb-1">
                                        <svg className="w-3.5 h-3.5 shrink-0 mt-0.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                        </svg>
                                        {c.location}
                                    </p>
                                    <p className="text-xs text-slate-400 font-mono">法人番号: {c.corporate_number}</p>
                                    <div className="mt-3 flex justify-end">
                                        <span className="text-xs font-medium text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                                            この企業で検索
                                            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                            </svg>
                                        </span>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </section>
                )}

                {/* 検索成功 - Markdown表示 */}
                {!isLoading && result?.status === "success" && result.markdown && (
                    <section ref={resultRef} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        {/* ツールバー */}
                        <div className="border-b border-slate-200 bg-slate-50 px-5 py-3 flex items-center justify-between gap-4">
                            <div className="flex items-center gap-2 text-xs text-slate-500 font-mono min-w-0">
                                <span className="truncate">法人番号: {result.corporate_number}</span>
                            </div>
                            <div className="flex gap-2 shrink-0">
                                <button
                                    onClick={handleCopy}
                                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md
                                border border-slate-200 bg-white text-slate-600
                                hover:bg-slate-50 transition"
                                >
                                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                                    </svg>
                                    コピー
                                </button>
                                <button
                                    onClick={handleDownload}
                                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md
                                border border-slate-200 bg-white text-slate-600
                                hover:bg-slate-50 transition"
                                >
                                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                    </svg>
                                    ダウンロード
                                </button>
                                {result.url && (
                                    <a
                                        href={result.url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md
                                border border-slate-200 bg-white text-blue-600
                                hover:bg-blue-50 transition"
                                    >
                                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                        </svg>
                                        gBizINFO
                                    </a>
                                )}
                                <button
                                    onClick={handleReset}
                                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md
                                border border-slate-200 bg-white text-slate-500
                                hover:bg-slate-50 transition"
                                >
                                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                    </svg>
                                    リセット
                                </button>
                            </div>
                        </div>

                        {/* Markdown本文 */}
                        <div className="p-8 prose prose-sm prose-slate max-w-none
                            prose-headings:font-semibold
                            prose-h1:text-xl prose-h1:mb-4
                            prose-h2:text-base prose-h2:mt-6 prose-h2:mb-3
                            prose-h3:text-sm prose-h3:mt-5 prose-h3:mb-2
                            prose-li:text-sm prose-li:my-0.5
                            prose-code:text-xs prose-code:bg-slate-100 prose-code:px-1 prose-code:rounded
                            prose-hr:border-slate-200">
                            <ReactMarkdown>{result.markdown}</ReactMarkdown>
                        </div>
                    </section>
                )}
            </main>
        </div>
    );
}