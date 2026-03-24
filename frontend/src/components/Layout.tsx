import { Outlet, Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";

const NAV = [
  { path: "/", label: "Hub", icon: "🏠" },
  { path: "/settings", label: "Settings", icon: "⚙️" },
];

export default function Layout() {
  const location = useLocation();

  return (
    <div className="flex flex-col min-h-screen">
      {/* ─── Header ─── */}
      <header className="flex items-center justify-between px-6 py-3 border-b border-arena-border bg-arena-surface/80 backdrop-blur-sm sticky top-0 z-50">
        <Link to="/" className="flex items-center gap-2 group">
          <span className="text-2xl">⚔️</span>
          <span className="text-xl font-bold tracking-wide text-arena-accent-light group-hover:text-white transition-colors">
            ARENA
          </span>
        </Link>

        <nav className="flex items-center gap-4 text-sm">
          {NAV.map((n) => (
            <Link
              key={n.path}
              to={n.path}
              className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition-colors ${
                location.pathname === n.path
                  ? "bg-arena-accent/20 text-arena-accent-light"
                  : "text-arena-muted hover:text-white"
              }`}
            >
              <span>{n.icon}</span>
              <span>{n.label}</span>
            </Link>
          ))}
        </nav>
      </header>

      {/* ─── Main ─── */}
      <main className="flex-1 p-6">
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
        >
          <Outlet />
        </motion.div>
      </main>

      {/* ─── Footer ─── */}
      <footer className="text-center text-xs text-arena-muted py-3 border-t border-arena-border">
        ARENA v0.1 — Multi-Agent Experimental Platform
      </footer>
    </div>
  );
}
