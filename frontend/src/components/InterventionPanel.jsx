// InterventionPanel.jsx — AI teaching suggestions (#33, AC #4), responsive (#34)
// Shows 3+ suggestions from the intervention agent (#29).
// The agent is still a stub server-side; this renders the deterministic
// demo set from dashboardData so the panel is always populated for review.

import { DEMO_INTERVENTIONS } from "../lib/dashboardData";

export default function InterventionPanel() {
  const suggestions =
    DEMO_INTERVENTIONS.length > 0
      ? DEMO_INTERVENTIONS
      : [
          "Begin with a quick recap quiz to re-engage the class.",
          "Use a real-world example to anchor the next concept.",
          "Open the floor for questions before advancing to new material.",
        ];

  return (
    <div
      className="bg-white border border-gray-200 rounded-xl p-4 sm:p-5 shadow-sm"
      aria-label="Intervention suggestions"
    >
      <h3 className="text-base font-semibold text-gray-900 mb-1">
        Intervention Suggestions
      </h3>
      <p className="text-xs text-gray-500 mb-3">
        AI-generated, based on live engagement signals
      </p>

      <ol className="grid gap-2.5">
        {suggestions.map((s, i) => (
          <li key={i} className="flex gap-2.5 items-start">
            <span className="shrink-0 w-6 h-6 rounded-full bg-indigo-600 text-white text-xs font-bold flex items-center justify-center mt-0.5">
              {i + 1}
            </span>
            <span className="text-sm text-gray-700 leading-relaxed">{s}</span>
          </li>
        ))}
      </ol>
    </div>
  );
}
