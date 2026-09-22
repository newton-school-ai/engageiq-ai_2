// LiveEngagement.jsx — real-time engagement graph (#33, AC #2 + #6),
// responsive + touch-friendly tooltip (#34)
//
// Reads the live engagement stream via connectLiveStream (real backend
// WebSocket when available, local 2s simulator otherwise) and renders a
// lightweight zero-dependency SVG line graph that advances every 2 seconds.
// Reconnect/backoff + simulator fallback are handled in dashboardData.js,
// surfaced here as a status pill.

import { useEffect, useRef, useState } from "react";
import { connectLiveStream } from "../lib/dashboardData";

const MAX_POINTS = 30; // ~60s of history at 2s ticks
const W = 640;
const H = 220;
const PAD = 28;

const xFor = (i) => PAD + i * ((W - PAD * 2) / Math.max(1, MAX_POINTS - 1));
const yFor = (s) => H - PAD - (s / 100) * (H - PAD * 2);

function buildPath(scores) {
  if (scores.length === 0) return "";
  return scores
    .map((s, i) => `${i === 0 ? "M" : "L"}${xFor(i).toFixed(1)},${yFor(s).toFixed(1)}`)
    .join(" ");
}

const STATUS_LABEL = {
  live: { text: "LIVE", className: "bg-green-600" },
  reconnecting: { text: "RECONNECTING", className: "bg-amber-500" },
  simulated: { text: "DEMO STREAM", className: "bg-indigo-500" },
};

export default function LiveEngagement({ sessionId = 101 }) {
  const [scores, setScores] = useState([]);
  const [status, setStatus] = useState("reconnecting");
  const [lastUpdate, setLastUpdate] = useState(null);
  const [hoverIndex, setHoverIndex] = useState(null);
  const cleanupRef = useRef(null);
  const svgRef = useRef(null);

  useEffect(() => {
    setScores([]);
    setStatus("reconnecting");
    cleanupRef.current = connectLiveStream(sessionId, {
      onStatus: setStatus,
      onScore: (s) => {
        setScores((prev) => [...prev, s].slice(-MAX_POINTS));
        setLastUpdate(new Date());
      },
    });
    return () => {
      if (cleanupRef.current) cleanupRef.current();
    };
  }, [sessionId]);

  const current = scores.length ? scores[scores.length - 1] : null;
  const badge = STATUS_LABEL[status] || STATUS_LABEL.simulated;

  // Touch/mouse -> nearest point index, for the tooltip. Works for both
  // pointer types via onPointerMove/onPointerDown (touch-friendly per AC).
  const updateHoverFromClientX = (clientX) => {
    if (!svgRef.current || scores.length === 0) return;
    const rect = svgRef.current.getBoundingClientRect();
    const relX = ((clientX - rect.left) / rect.width) * W;
    const step = (W - PAD * 2) / Math.max(1, MAX_POINTS - 1);
    const idx = Math.round((relX - PAD) / step);
    setHoverIndex(Math.max(0, Math.min(scores.length - 1, idx)));
  };

  return (
    <div
      className="bg-white border border-gray-200 rounded-xl p-4 sm:p-5 shadow-sm"
      role="region"
      aria-label="Live engagement graph"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-base font-semibold text-gray-900">
          Live Engagement
        </h3>
        <span
          className={`text-white text-[11px] font-bold tracking-wide px-2 py-1 rounded-full ${badge.className}`}
        >
          {badge.text}
        </span>
      </div>

      <div className="flex items-baseline gap-2 my-2 flex-wrap">
        <span className="text-3xl font-extrabold text-indigo-600">
          {current !== null ? current.toFixed(1) : "—"}
        </span>
        <span className="text-xs text-gray-500">current score / 100</span>
        {lastUpdate && (
          <span className="text-[11px] text-gray-400 ml-auto">
            updated {lastUpdate.toLocaleTimeString()}
          </span>
        )}
      </div>

      {scores.length === 0 ? (
        <div className="h-[220px] flex items-center justify-center text-gray-400 text-sm">
          Connecting to live stream…
        </div>
      ) : (
        <div className="relative">
          <svg
            ref={svgRef}
            viewBox={`0 0 ${W} ${H}`}
            width="100%"
            height="auto"
            style={{ aspectRatio: `${W} / ${H}` }}
            preserveAspectRatio="xMidYMid meet"
            className="block touch-none"
            onPointerMove={(e) => updateHoverFromClientX(e.clientX)}
            onPointerDown={(e) => updateHoverFromClientX(e.clientX)}
            onPointerLeave={() => setHoverIndex(null)}
          >
            {/* gridlines every 25 */}
            {[0, 25, 50, 75, 100].map((g) => {
              const y = yFor(g);
              return (
                <g key={g}>
                  <line x1={PAD} y1={y} x2={W - PAD} y2={y} stroke="#e5e7eb" strokeWidth="1" />
                  <text x={4} y={y + 4} fontSize="11" fill="#9ca3af">
                    {g}
                  </text>
                </g>
              );
            })}

            {scores.length > 1 && (
              <path
                d={buildPath(scores)}
                fill="none"
                stroke="#6366f1"
                strokeWidth="2.5"
                strokeLinejoin="round"
                strokeLinecap="round"
              />
            )}

            {/* leading dot */}
            <circle
              cx={xFor(scores.length - 1)}
              cy={yFor(scores[scores.length - 1])}
              r="4"
              fill="#4f46e5"
            />

            {/* touch-friendly tooltip: vertical guide + dot + value label */}
            {hoverIndex !== null && scores[hoverIndex] !== undefined && (
              <g pointerEvents="none">
                <line
                  x1={xFor(hoverIndex)}
                  y1={PAD}
                  x2={xFor(hoverIndex)}
                  y2={H - PAD}
                  stroke="#c7d2fe"
                  strokeWidth="1"
                  strokeDasharray="3 3"
                />
                <circle
                  cx={xFor(hoverIndex)}
                  cy={yFor(scores[hoverIndex])}
                  r="5"
                  fill="#4f46e5"
                  stroke="#fff"
                  strokeWidth="2"
                />
                <rect
                  x={Math.min(Math.max(xFor(hoverIndex) - 24, 2), W - 50)}
                  y={Math.max(yFor(scores[hoverIndex]) - 28, 2)}
                  width="48"
                  height="20"
                  rx="5"
                  fill="#111827"
                />
                <text
                  x={Math.min(Math.max(xFor(hoverIndex), 26), W - 26)}
                  y={Math.max(yFor(scores[hoverIndex]) - 14, 16)}
                  fontSize="11"
                  fill="#fff"
                  textAnchor="middle"
                >
                  {scores[hoverIndex].toFixed(0)}
                </text>
              </g>
            )}
          </svg>
        </div>
      )}
      <p className="text-[11px] text-gray-400 mt-2 mb-0">
        Updates every 2s. Auto-reconnects on disconnect; falls back to a
        local demo stream when the backend is offline. Tap or drag across
        the chart to inspect a point.
      </p>
    </div>
  );
}
