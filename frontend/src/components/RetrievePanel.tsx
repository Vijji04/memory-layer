"use client";

import { useState } from "react";
import { retrieveMemories, type RetrieveResponse } from "@/lib/api";
import TracePanel from "@/components/TracePanel";

export default function RetrievePanel() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RetrieveResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleRetrieve() {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await retrieveMemories(question);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Input */}
      <div className="space-y-3">
        <label className="block text-sm font-medium text-zinc-400">
          Ask a question to search stored memories
        </label>
        <div className="flex gap-3">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleRetrieve()}
            placeholder="What programming language do I prefer?"
            className="flex-1 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-600 focus:border-zinc-600 focus:outline-none focus:ring-1 focus:ring-zinc-600"
          />
          <button
            onClick={handleRetrieve}
            disabled={loading || !question.trim()}
            className="rounded-lg bg-zinc-100 px-5 py-2.5 text-sm font-medium text-zinc-900 transition-colors hover:bg-white disabled:opacity-40 disabled:cursor-not-allowed whitespace-nowrap"
          >
            {loading ? "Searching..." : "Ask"}
          </button>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-red-900/50 bg-red-950/30 px-4 py-3 text-sm text-red-400">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          {/* Retrieved memories */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-zinc-300">
              Retrieved Memories
              <span className="ml-2 rounded-full bg-zinc-800 px-2 py-0.5 text-xs text-zinc-400">
                {result.retrieved_memories.length}
              </span>
            </h3>
            {result.retrieved_memories.length > 0 ? (
              <div className="space-y-2">
                {result.retrieved_memories.map((mem, i) => (
                  <div
                    key={i}
                    className="rounded-md border border-zinc-800 bg-zinc-900/50 px-4 py-3"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <p className="text-sm text-zinc-200">{mem.fact}</p>
                      <span className="shrink-0 rounded-md bg-emerald-950/50 border border-emerald-800/40 px-2 py-0.5 text-xs font-mono text-emerald-400">
                        {(mem.similarity_score * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-2">
                      <span
                        className={`inline-block rounded-md border px-2 py-0.5 text-xs font-medium ${typeStyle(
                          mem.memory_type
                        )}`}
                      >
                        {mem.memory_type}
                      </span>
                      <span className="inline-block rounded-md border border-zinc-700/40 bg-zinc-800/50 px-2 py-0.5 text-xs font-medium text-zinc-400">
                        importance: {mem.importance}/10
                      </span>
                      <span
                        className={`inline-block rounded-md border px-2 py-0.5 text-xs font-medium ${
                          mem.tier === "session"
                            ? "bg-amber-950/50 text-amber-400 border-amber-800/40"
                            : "bg-blue-950/50 text-blue-400 border-blue-800/40"
                        }`}
                      >
                        {mem.tier}
                      </span>
                    </div>
                    <p className="mt-1.5 text-xs text-zinc-500">{mem.signal}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-zinc-500">
                No matching memories found
              </p>
            )}
          </div>

          {/* Answer */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-zinc-300">Answer</h3>
            <div className="rounded-lg border border-zinc-800 bg-zinc-900/50 px-5 py-4">
              <p className="text-sm leading-relaxed text-zinc-200 whitespace-pre-wrap">
                {result.answer}
              </p>
            </div>
          </div>

          {/* Trace */}
          <TracePanel trace={result.trace} />
        </div>
      )}
    </div>
  );
}

function typeStyle(type: string): string {
  switch (type) {
    case "semantic":
      return "bg-emerald-950/50 text-emerald-400 border-emerald-800/40";
    case "procedural":
      return "bg-violet-950/50 text-violet-400 border-violet-800/40";
    case "episodic":
      return "bg-cyan-950/50 text-cyan-400 border-cyan-800/40";
    default:
      return "bg-zinc-800/50 text-zinc-400 border-zinc-700/40";
  }
}
