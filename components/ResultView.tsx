// components/ResultView.tsx

// Markdownのレンダリングと、コピーやダウンロードなどのツールバー機能を集約。

import { Copy, Download, ExternalLink, RotateCcw } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkBreaks from "remark-breaks";
import { SearchResponse } from "@/types";

type ResultViewProps = {
    result: SearchResponse;
    corpName: string;
    onReset: () => void;
};

export default function ResultView({ result, corpName, onReset }: ResultViewProps) {
    if (!result.markdown) return null;

    // コピー処理
    const handleCopy = () => {
        navigator.clipboard.writeText(result.markdown!);
    };

    // ダウンロード処理
    const handleDownload = () => {
        const blob = new Blob([result.markdown!], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${result.corp_name ?? corpName}_企業情報.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <section className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
            {/* ツールバー */}
            <div className="border-b border-slate-200 bg-slate-50 px-5 py-3 flex items-center justify-between gap-4">
                <div className="flex items-center gap-2 text-xs text-slate-500 font-mono min-w-0">
                    <span className="truncate">法人番号: {result.corporate_number}</span>
                </div>
                <div className="flex gap-2 shrink-0">
                    <button
                        onClick={handleCopy}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition"
                    >
                        <Copy className="w-3.5 h-3.5" />
                        コピー
                    </button>
                    <button
                        onClick={handleDownload}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition"
                    >
                        <Download className="w-3.5 h-3.5" />
                        ダウンロード
                    </button>
                    {result.url && (
                        <a
                            href={result.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border border-slate-200 bg-white text-blue-600 hover:bg-blue-50 transition"
                        >
                            <ExternalLink className="w-3.5 h-3.5" />
                            gBizINFO
                        </a>
                    )}
                    <button
                        onClick={onReset}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 transition"
                    >
                        <RotateCcw className="w-3.5 h-3.5" />
                        リセット
                    </button>
                </div>
            </div>

            {/* Markdown本文 */}
            <div className="markdown p-8 prose prose-sm prose-slate max-w-none">
                <ReactMarkdown remarkPlugins={[remarkBreaks]}>
                    {result.markdown}
                </ReactMarkdown>
            </div>
        </section>
    );
}