// TeacherDashboard.jsx — main dashboard (#33), made responsive (#34)
// Orchestrates ClassOverview, LiveEngagement, session history, AtRiskPanel
// and InterventionPanel. Handles loading + empty states and is responsive
// from 375px phones through desktop (AC: no horizontal scroll, single
// column on mobile, two-column grid from lg: up).

import { useEffect, useState } from "react";
import ClassOverview from "../components/ClassOverview";
import LiveEngagement from "../components/LiveEngagement";
import AtRiskPanel from "../components/AtRiskPanel";
import InterventionPanel from "../components/InterventionPanel";
import { DEMO_SESSIONS, getSessionReport } from "../lib/dashboardData";

const DashboardSkeleton = () => (
  <div className="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8 animate-pulse">
    <div className="max-w-7xl mx-auto">
      <div className="h-8 bg-gray-200 rounded w-1/2 sm:w-1/4 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-3/4 sm:w-1/3 mb-8" />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <div className="h-80 bg-gray-200 rounded-xl" />
        <div className="h-80 bg-gray-200 rounded-xl" />
      </div>
    </div>
  </div>
);

export default function TeacherDashboard() {
  const [loading, setLoading] = useState(true);
  const [courseId, setCourseId] = useState(1);
  const [selectedSession, setSelectedSession] = useState(null);
  const [report, setReport] = useState(null);

  // Simulate initial data load so the loading state is real and demonstrable.
  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 900);
    return () => clearTimeout(t);
  }, []);

  const openSession = (id) => {
    setSelectedSession(id);
    setReport(getSessionReport(id));
  };

  if (loading) return <DashboardSkeleton />;

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900">
            Teacher Dashboard
          </h1>
          <p className="text-gray-600 mt-1 text-sm md:text-base">
            Real-time engagement monitoring &amp; AI teaching insights
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-[1.4fr_1fr] gap-4 sm:gap-6 items-start">
          {/* Left column: overview + live + history */}
          <div className="grid gap-4 sm:gap-6 min-w-0">
            <ClassOverview courseId={courseId} onSelectCourse={setCourseId} />
            <LiveEngagement sessionId={selectedSession || 101} />

            <section
              className="bg-white border border-gray-200 rounded-xl p-4 sm:p-5 shadow-sm"
              aria-label="Session history"
            >
              <h3 className="text-base font-semibold text-gray-900 mb-3">
                Session History
              </h3>

              {DEMO_SESSIONS.length === 0 ? (
                <div className="p-5 text-center text-gray-400 bg-gray-50 rounded-lg">
                  No past sessions yet.
                </div>
              ) : (
                <ul className="grid gap-2 mb-3">
                  {DEMO_SESSIONS.map((s) => (
                    <li key={s.id}>
                      <button
                        onClick={() => openSession(s.id)}
                        className={`w-full text-left border rounded-lg px-3 py-2.5 min-h-touch flex flex-col gap-0.5 transition-colors ${
                          selectedSession === s.id
                            ? "border-indigo-500 bg-indigo-50"
                            : "border-gray-200 bg-white hover:bg-gray-50"
                        }`}
                      >
                        <span className="text-sm font-semibold text-gray-900 truncate">
                          {s.title}
                        </span>
                        <span className="text-xs text-gray-400">
                          {s.date} · {s.durationMin}m · avg {s.avg}%
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}

              {report ? (
                <div className="mt-2 pt-3 border-t border-gray-100">
                  <div className="font-bold text-sm mb-2">
                    {report.title} — Report
                  </div>
                  <div className="flex gap-6 mb-3">
                    <div>
                      <div className="text-xl font-extrabold text-indigo-600">
                        {report.averageEngagement}%
                      </div>
                      <div className="text-xs text-gray-500">
                        Avg Engagement
                      </div>
                    </div>
                    <div>
                      <div className="text-xl font-extrabold text-indigo-600">
                        {report.durationMin}m
                      </div>
                      <div className="text-xs text-gray-500">Duration</div>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500 mb-1.5">
                    State distribution
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(report.stateDistribution).map(
                      ([k, v]) => (
                        <div
                          key={k}
                          className="bg-gray-50 rounded-lg px-2.5 py-1.5 text-center min-w-[56px]"
                        >
                          <span className="block text-sm font-bold text-gray-700">
                            {v}%
                          </span>
                          <span className="text-[10px] text-gray-400 capitalize">
                            {k}
                          </span>
                        </div>
                      )
                    )}
                  </div>
                  <div className="text-xs text-gray-600 mt-2.5 leading-relaxed">
                    {report.topIssues.map((iss, i) => (
                      <div key={i}>• {iss}</div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-xs text-gray-400 mt-2">
                  Select a session above to view its report.
                </div>
              )}
            </section>
          </div>

          {/* Right column: at-risk + interventions */}
          <div className="grid gap-4 sm:gap-6 min-w-0">
            <AtRiskPanel />
            <InterventionPanel />
          </div>
        </div>
      </div>
    </div>
  );
}
