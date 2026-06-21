"use client";

import { useState } from "react";
import {
  captureMemories,
  type CaptureResponse,
  type EvaluatedMemory,
} from "@/lib/api";
import TracePanel from "@/components/TracePanel";

const PLACEHOLDER = `I prefer Python over Java for backend work. My current project is a memory layer for AI agents using FastAPI. I had a great sandwich for lunch today. Always use type hints in Python — they catch bugs early. Our team standup is at 9am Pacific every day. PostgreSQL is the best relational database for most use cases.`;

export default function CapturePanel() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CaptureResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleCapture() {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await captureMemories(text);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  const kept = result?.evaluation.filter((m) => m.decision === "keep") ?? [];
  const dropped =
    result?.evaluation.filter((m) => m.decision === "drop") ?? [];

  return (
    <div className="space-y-6">
      {/* Input */}
      <div className="space-y-3">
        <label className="block text-sm font-medium text-zinc-400">
          Paste a paragraph with multiple facts
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={PLACEHOLDER}
          rows={5}
          className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3 text-sm text-zinc-100 placeholder:text-zinc-600 focus:border-zinc-600 focus:outline-none focus:ring-1 focus:ring-zinc-600 resize-none"
        />
        <button
          onClick={handleCapture}
          disabled={loading || !text.trim()}
          className="rounded-lg bg-zinc-100 px-5 py-2 text-sm font-medium text-zinc-900 transition-colors hover:bg-white disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? "Processing..." : "Extract & Classify"}
        </button>
      </div>

      {error && (
        <div className="rounded-lg border border-red-900/50 bg-red-950/30 px-4 py-3 text-sm text-red-400">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          {/* Stage 1: Extraction */}
          <Section title="Stage 1: Extraction" count={result.extraction.length}>
            <div className="space-y-2">
              {result.extraction.map((fact, i) => (
                <div
                  key={i}
                  className="rounded-md border border-zinc-800 bg-zinc-900/50 px-4 py-3"
                >
                  <p className="text-sm text-zinc-200">{fact.fact}</p>
                  <p className="mt-1 text-xs text-zinc-500">
                    Source: &ldquo;{fact.source_sentence}&rdquo;
                  </p>
                </div>
              ))}
            </div>
          </Section>

          {/* Stage 2: Evaluation */}
          <Section
            title="Stage 2: Evaluation"
            count={result.evaluation.length}
          >
            {/* Kept */}
            {kept.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs font-medium uppercase tracking-wider text-emerald-500">
                  Kept ({kept.length})
                </h4>
                {kept.map((mem, i) => (
                  <MemoryCard key={i} memory={mem} />
                ))}
              </div>
            )}
            {/* Dropped */}
            {dropped.length > 0 && (
              <div className="mt-4 space-y-2">
                <h4 className="text-xs font-medium uppercase tracking-wider text-zinc-500">
                  Dropped ({dropped.length})
                </h4>
                {dropped.map((mem, i) => (
                  <MemoryCard key={i} memory={mem} dimmed />
                ))}
              </div>
            )}
          </Section>

          {/* Storage summary */}
          <Section title="Storage">
            <div className="grid grid-cols-2 gap-4">
              <StoreBucket
                label="Session"
                items={result.stored.session}
                color="amber"
              />
              <StoreBucket
                label="Long-term"
                items={result.stored.long_term}
                color="blue"
              />
            </div>
          </Section>

          {/* Trace */}
          <TracePanel trace={result.trace} />
        </div>
      )}
    </div>
  );
}

function Section({
  title,
  count,
  children,
}: {
  title: string;
  count?: number;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <h3 className="text-sm font-semibold text-zinc-300">{title}</h3>
        {count !== undefined && (
          <span className="rounded-full bg-zinc-800 px-2 py-0.5 text-xs text-zinc-400">
            {count}
          </span>
        )}
      </div>
      {children}
    </div>
  );
}

function MemoryCard({
  memory,
  dimmed = false,
}: {
  memory: EvaluatedMemory;
  dimmed?: boolean;
}) {
  return (
    <div
      className={`rounded-md border px-4 py-3 ${
        dimmed
          ? "border-zinc-800/50 bg-zinc-900/20 opacity-60"
          : "border-zinc-800 bg-zinc-900/50"
      }`}
    >
      <p className={`text-sm ${dimmed ? "text-zinc-500" : "text-zinc-200"}`}>
        {memory.fact}
      </p>
      <div className="mt-2 flex flex-wrap gap-2">
        <Badge color={typeColor(memory.type)}>{memory.type}</Badge>
        <Badge color="zinc">importance: {memory.importance}/10</Badge>
        <Badge color="zinc">confidence: {memory.confidence}</Badge>
        <Badge color={memory.tier === "session" ? "amber" : "blue"}>
          {memory.tier}
        </Badge>
      </div>
      <p className="mt-1.5 text-xs text-zinc-500">{memory.reason}</p>
    </div>
  );
}

function StoreBucket({
  label,
  items,
  color,
}: {
  label: string;
  items: string[];
  color: "amber" | "blue";
}) {
  const borderColor =
    color === "amber" ? "border-amber-800/40" : "border-blue-800/40";
  const labelColor =
    color === "amber" ? "text-amber-500" : "text-blue-500";

  return (
    <div className={`rounded-lg border ${borderColor} bg-zinc-900/30 p-4`}>
      <h4
        className={`text-xs font-medium uppercase tracking-wider ${labelColor}`}
      >
        {label} ({items.length})
      </h4>
      {items.length > 0 ? (
        <ul className="mt-2 space-y-1">
          {items.map((item, i) => (
            <li key={i} className="text-sm text-zinc-300">
              {item}
            </li>
          ))}
        </ul>
      ) : (
        <p className="mt-2 text-xs text-zinc-600">No memories stored</p>
      )}
    </div>
  );
}

function Badge({
  children,
  color,
}: {
  children: React.ReactNode;
  color: string;
}) {
  const colorMap: Record<string, string> = {
    emerald: "bg-emerald-950/50 text-emerald-400 border-emerald-800/40",
    violet: "bg-violet-950/50 text-violet-400 border-violet-800/40",
    cyan: "bg-cyan-950/50 text-cyan-400 border-cyan-800/40",
    amber: "bg-amber-950/50 text-amber-400 border-amber-800/40",
    blue: "bg-blue-950/50 text-blue-400 border-blue-800/40",
    zinc: "bg-zinc-800/50 text-zinc-400 border-zinc-700/40",
  };
  return (
    <span
      className={`inline-block rounded-md border px-2 py-0.5 text-xs font-medium ${
        colorMap[color] || colorMap.zinc
      }`}
    >
      {children}
    </span>
  );
}

function typeColor(type: string): string {
  switch (type) {
    case "semantic":
      return "emerald";
    case "procedural":
      return "violet";
    case "episodic":
      return "cyan";
    default:
      return "zinc";
  }
}
