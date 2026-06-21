"use client";

import { useState } from "react";
import CapturePanel from "@/components/CapturePanel";
import RetrievePanel from "@/components/RetrievePanel";

type Tab = "capture" | "retrieve";

export default function Home() {
  const [activeTab, setActiveTab] = useState<Tab>("capture");

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="shrink-0 border-b border-zinc-800 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold tracking-tight text-zinc-100">
              Memory Layer
            </h1>
            <p className="text-sm text-zinc-500 mt-0.5">
              Capture, classify, and retrieve memories for AI agents
            </p>
          </div>
          <div className="flex gap-1 rounded-lg bg-zinc-900 p-1">
            <button
              onClick={() => setActiveTab("capture")}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${
                activeTab === "capture"
                  ? "bg-zinc-800 text-zinc-100"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              Capture
            </button>
            <button
              onClick={() => setActiveTab("retrieve")}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${
                activeTab === "retrieve"
                  ? "bg-zinc-800 text-zinc-100"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              Retrieve
            </button>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-5xl mx-auto px-6 py-6">
          {activeTab === "capture" ? <CapturePanel /> : <RetrievePanel />}
        </div>
      </main>
    </div>
  );
}
