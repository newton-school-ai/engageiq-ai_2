import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Nav from "./components/Nav.jsx";
import TeacherDashboard from "./pages/TeacherDashboard.jsx";
import StudentDashboard from "./pages/StudentDashboard.jsx";
import "./index.css";

function App() {
  return (
    <BrowserRouter>
      <div className="lg:flex">
        <Nav />
        <main className="flex-1 min-w-0">
          <Routes>
            <Route path="/teacher" element={<TeacherDashboard />} />
            <Route path="/student" element={<StudentDashboard />} />
            <Route path="/" element={<Navigate to="/teacher" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// PWA: register the service worker (acceptance criteria: service worker
// caches static assets). Only in production builds -- registering it
// during `vite dev` fights with Vite's own dev-server caching/HMR.
if ("serviceWorker" in navigator && import.meta.env.PROD) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/service-worker.js")
      .catch((err) => console.error("Service worker registration failed:", err));
  });
}
