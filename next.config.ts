import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    rewrites: async () => {
        return [
            {
                source: "/api/py/:path*",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://127.0.0.1:8000/api/py/:path*" // ローカル
                        : "/api/", // 本番（サーバーレス関数）
            },
        ];
    },
};

export default nextConfig;

// ポイント
// destination の本番側が /api/ （末尾スラッシュあり）になっている点に注意。
// Vercel が api/index.py をサーバーレス関数として /api/ にマウントするため。