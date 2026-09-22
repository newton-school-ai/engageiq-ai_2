// Minimal axios client. StudentDashboard.jsx (#32) already imports this
// path but the file was never added in that PR -- this is the smallest
// possible stub to unblock building/running the app so #34's responsive +
// PWA work can actually be tested end-to-end. Not a full API layer; the
// real implementation belongs to whichever issue owns the API client.
import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export default api;
