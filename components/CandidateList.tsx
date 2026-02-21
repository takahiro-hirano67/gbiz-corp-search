// components/CandidateList.tsx

// 検索結果が複数あった場合のサジェストUIを担当

import { AlertTriangle, ChevronRight, MapPin } from "lucide-react";
import { Candidate } from "@/types";

type CandidateListProps = {
    message: string;
    candidates: Candidate[];
    onSelect: (candidate: Candidate) => void;
};

export default function CandidateList({ message, candidates, onSelect }: CandidateListProps) {
    return (
        <section>
            <div className="mb-4 bg-amber-50 border border-amber-200 rounded-xl p-4 flex gap-3 items-start">
                <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                <p className="text-sm text-amber-800">{message}</p>
            </div>
            <div className="grid sm:grid-cols-2 gap-3">
                {candidates.map((c) => (
                    <button
                        key={c.corporate_number}
                        onClick={() => onSelect(c)}
                        className="bg-white border border-slate-200 rounded-xl p-5 text-left hover:border-blue-400 hover:shadow-xs transition-all group"
                    >
                        <p className="font-semibold text-slate-800 group-hover:text-blue-600 transition-colors text-sm mb-2">
                            {c.name}
                        </p>
                        <p className="text-xs text-slate-500 flex items-start gap-1 mb-1">
                            <MapPin className="w-3.5 h-3.5 shrink-0 mt-0.5 text-slate-400" />
                            {c.location}
                        </p>
                        <p className="text-xs text-slate-400 font-mono">
                            法人番号: {c.corporate_number}
                        </p>
                        <div className="mt-3 flex justify-end">
                            <span className="text-xs font-medium text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                                この企業で検索
                                <ChevronRight className="w-3 h-3" />
                            </span>
                        </div>
                    </button>
                ))}
            </div>
        </section>
    );
}