// ClassOverview.jsx — class summary (#33, AC #1), responsive (#34)
// Course selector + student count + average engagement.

import { DEMO_COURSES, getClassOverview } from "../lib/dashboardData";

const AVG_COLOR = {
  good: "text-green-600",
  ok: "text-amber-500",
  bad: "text-red-600",
};
const AVG_BAR = {
  good: "bg-green-600",
  ok: "bg-amber-500",
  bad: "bg-red-600",
};

function avgTier(v) {
  if (v >= 70) return "good";
  if (v >= 50) return "ok";
  return "bad";
}

export default function ClassOverview({ courseId, onSelectCourse }) {
  const overview = getClassOverview(courseId);
  const avg = overview.averageEngagement;
  const tier = avgTier(avg);

  return (
    <div
      className="bg-white border border-gray-200 rounded-xl p-4 sm:p-5 shadow-sm"
      aria-label="Class overview"
    >
      <h3 className="text-base font-semibold text-gray-900 mb-3">
        Class Overview
      </h3>

      <label
        className="text-xs text-gray-500 block mb-1"
        htmlFor="course-select"
      >
        Course
      </label>
      <select
        id="course-select"
        value={courseId}
        onChange={(e) => onSelectCourse(Number(e.target.value))}
        className="w-full min-h-touch px-3 rounded-lg border border-gray-300 text-sm mb-4"
      >
        {DEMO_COURSES.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name} ({c.code})
          </option>
        ))}
      </select>

      <div className="flex gap-6">
        <div className="flex-1">
          <div className="text-2xl sm:text-3xl font-extrabold text-gray-900">
            {overview.studentCount}
          </div>
          <div className="text-xs text-gray-500">Students</div>
        </div>
        <div className="flex-1">
          <div className={`text-2xl sm:text-3xl font-extrabold ${AVG_COLOR[tier]}`}>
            {avg}%
          </div>
          <div className="text-xs text-gray-500">Avg Engagement</div>
        </div>
      </div>

      <div className="mt-3 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-500 ${AVG_BAR[tier]}`}
          style={{ width: `${avg}%` }}
        />
      </div>
      <p className="text-xs text-gray-400 mt-2 mb-0">{overview.courseName}</p>
    </div>
  );
}
