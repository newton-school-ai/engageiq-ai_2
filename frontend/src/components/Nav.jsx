import React, { useState } from "react";
import { NavLink } from "react-router-dom";

// Nav.jsx — app shell navigation (#34, AC "Hamburger menu on mobile,
// sidebar on desktop"). Neither dashboard had any navigation wrapper
// before this, so this also gives the two dashboards a real place to live
// side by side (routes) instead of main.jsx hardcoding just one of them.

const LINKS = [
  { to: "/teacher", label: "Teacher Dashboard" },
  { to: "/student", label: "Student Dashboard" },
];

export default function Nav() {
  const [open, setOpen] = useState(false);

  const linkClass = ({ isActive }) =>
    `block rounded-lg px-3 py-2.5 text-sm font-medium transition-colors min-h-touch flex items-center ${
      isActive
        ? "bg-indigo-50 text-indigo-700"
        : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
    }`;

  return (
    <>
      {/* Mobile top bar with hamburger */}
      <header className="lg:hidden sticky top-0 z-40 flex items-center justify-between border-b border-gray-200 bg-white px-4 py-3">
        <span className="text-lg font-extrabold text-indigo-600">EngageIQ</span>
        <button
          type="button"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
          className="inline-flex min-h-touch min-w-touch items-center justify-center rounded-lg text-gray-700 hover:bg-gray-100"
        >
          {open ? (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          ) : (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          )}
        </button>
      </header>

      {/* Mobile dropdown menu */}
      {open && (
        <nav
          className="lg:hidden fixed inset-x-0 top-[57px] z-30 border-b border-gray-200 bg-white p-3 shadow-lg"
          aria-label="Mobile navigation"
        >
          {LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={linkClass}
              onClick={() => setOpen(false)}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      )}

      {/* Desktop sidebar */}
      <nav
        className="hidden lg:flex lg:flex-col lg:w-60 lg:shrink-0 lg:border-r lg:border-gray-200 lg:bg-white lg:min-h-screen lg:px-3 lg:py-6"
        aria-label="Sidebar navigation"
      >
        <span className="mb-6 px-3 text-lg font-extrabold text-indigo-600">
          EngageIQ
        </span>
        <div className="flex flex-col gap-1">
          {LINKS.map((link) => (
            <NavLink key={link.to} to={link.to} className={linkClass}>
              {link.label}
            </NavLink>
          ))}
        </div>
      </nav>
    </>
  );
}
