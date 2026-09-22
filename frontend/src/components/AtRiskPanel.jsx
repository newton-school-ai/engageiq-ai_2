// AtRiskPanel.jsx — at-risk students (#33, AC #5), responsive (#34)
// Anonymized student IDs with trend arrows (up = improving, down = declining).

import { DEMO_AT_RISK } from "../lib/dashboardData";

export default function AtRiskPanel() {
  return (
    <div
      className="bg-white border border-gray-200 rounded-xl p-4 sm:p-5 shadow-sm"
      aria-label="At-risk students"
    >
      <h3 className="text-base font-semibold text-gray-900 mb-3">
        At-Risk Students
      </h3>

      {DEMO_AT_RISK.length === 0 ? (
        <div className="p-6 text-center text-green-600 text-sm bg-green-50 rounded-lg">
          No at-risk students detected 🎉
        </div>
      ) : (
        <ul className="grid gap-2.5">
          {DEMO_AT_RISK.map((s) => {
            const down = s.trend === "down";
            return (
              <li
                key={s.anonId}
                className="flex items-center gap-2.5 min-h-touch"
              >
                <span
                  className={`text-base font-extrabold w-4 text-center shrink-0 ${
                    down ? "text-red-600" : "text-green-600"
                  }`}
                  aria-label={down ? "declining" : "improving"}
                >
                  {down ? "▼" : "▲"}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-mono text-gray-700 truncate">
                    {s.anonId}
                  </div>
                  <div className="text-xs text-gray-400 truncate">
                    {s.reason}
                  </div>
                </div>
                <span
                  className={`text-base font-bold shrink-0 ${
                    s.avg < 50 ? "text-red-600" : "text-amber-500"
                  }`}
                >
                  {s.avg}%
                </span>
              </li>
            );
          })}
        </ul>
      )}
      <p className="text-xs text-gray-400 mt-3 mb-0">
        IDs are anonymized per the privacy-first design. Teachers never see
        raw student identity here.
      </p>
    </div>
  );
}
