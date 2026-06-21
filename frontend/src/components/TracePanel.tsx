"use client";

import { useState } from "react";
import type { Trace } from "@/lib/api";

export default function TracePanel({ trace }: { trace: Trace }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="space-y-2">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 text-sm font-semibold text-zinc-400 hover:text-zinc-300 transition-colors"
      >
        <svg
          className={`h-3 w-3 transition-transform ${
            expanded ? "rotate-90" : ""
          }`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M6 4l8 6-8 6V4z" />
        </svg>
        Trace
        <span className="font-mono text-xs text-zinc-600">
          {trace.trace_id}
        </span>
        <span className="text-xs text-zinc-600">
          {trace.total_duration_ms}ms
        </span>
        <span className="text-xs text-zinc-600">
          {trace.total_tokens_in + trace.total_tokens_out} tokens
        </span>
      </button>

      {expanded && (
        <div className="rounded-lg border border-zinc-800 bg-zinc-900/30 p-4 space-y-3">
          {/* Summary bar */}
          <div className="flex gap-6 text-xs text-zinc-500">
            <span>
              Duration:{" "}
              <span className="text-zinc-300">
                {trace.total_duration_ms}ms
              </span>
            </span>
            <span>
              Tokens in:{" "}
              <span className="text-zinc-300">{trace.total_tokens_in}</span>
            </span>
            <span>
              Tokens out:{" "}
              <span className="text-zinc-300">{trace.total_tokens_out}</span>
            </span>
          </div>

          {/* Spans */}
          <div className="space-y-2">
            {trace.spans.map((span) => (
              <div
                key={span.span_id}
                className="flex items-center gap-4 rounded-md border border-zinc-800/50 bg-zinc-950/50 px-3 py-2"
              >
                <span className="text-xs font-medium text-zinc-300 w-40 shrink-0">
                  {span.name}
                </span>
                {/* Duration bar */}
                <div className="flex-1 h-2 rounded-full bg-zinc-800 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-zinc-500"
                    style={{
                      width: `${Math.min(
                        100,
                        ((span.duration_ms ?? 0) / trace.total_duration_ms) *
                          100
                      )}%`,
                    }}
                  />
                </div>
                <div className="flex gap-4 text-xs text-zinc-500 shrink-0">
                  <span>{span.duration_ms ?? 0}ms</span>
                  {span.model && (
                    <span className="text-zinc-600">{span.model}</span>
                  )}
                  {(span.tokens_in > 0 || span.tokens_out > 0) && (
                    <span>
                      {span.tokens_in}/{span.tokens_out}t
                    </span>
                  )}
                </div>
                {span.error && (
                  <span className="text-xs text-red-400">{span.error}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
