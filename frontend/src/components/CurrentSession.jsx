import React from "react";

// CurrentSession.jsx — live session banner shown at the top of the student
// dashboard while a lecture is in progress. Referenced by StudentDashboard
// (#32) but never added in that PR; built here since it's a real, visible
// dashboard component and #34 requires every dashboard component to be
// responsive, not just the ones that happened to already exist.

const STATE_STYLES = {
  at_screen: { label: "Focused", dot: "bg-green-500", text: "text-green-700" },
  away_left: { label: "Distracted", dot: "bg-red-500", text: "text-red-700" },
  away_right: { label: "Distracted", dot: "bg-red-500", text: "text-red-700" },
  looking_down: { label: "Looking down", dot: "bg-yellow-500", text: "text-yellow-700" },
  eyes_closed: { label: "Away", dot: "bg-gray-400", text: "text-gray-600" },
};

const CurrentSession = ({ session }) => {
  if (!session) return null;

  const { title, score = 0, state, startedAt } = session;
  const stateInfo = STATE_STYLES[state] || STATE_STYLES.at_screen;

  return (
    <div
      className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-indigo-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
      aria-label="Current session"
    >
      <div className="flex items-center gap-3 min-w-0">
        <span
          className={`inline-block h-3 w-3 rounded-full ${stateInfo.dot} shrink-0 animate-pulse`}
          aria-hidden="true"
        />
        <div className="min-w-0">
          <p className="font-semibold text-gray-900 truncate">
            {title || "Live session"}
          </p>
          {startedAt && (
            <p className="text-xs text-gray-500">Started {startedAt}</p>
          )}
        </div>
      </div>

      <div className="flex items-center justify-between sm:justify-end gap-4 sm:gap-6">
        <div className="text-right">
          <p className="text-2xl font-extrabold text-indigo-600">{score}%</p>
          <p className={`text-xs font-medium ${stateInfo.text}`}>
            {stateInfo.label}
          </p>
        </div>
      </div>
    </div>
  );
};

export default CurrentSession;
