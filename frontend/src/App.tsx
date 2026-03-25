import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout.tsx";
import Hub from "./pages/Hub.tsx";
import Lobby from "./pages/Lobby.tsx";
import Arena from "./pages/Arena.tsx";
import Analysis from "./pages/Analysis.tsx";
import Settings from "./pages/Settings.tsx";
import History from "./pages/History.tsx";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Hub />} />
        <Route path="lobby/:experimentId" element={<Lobby />} />
        <Route path="arena" element={<Arena />} />
        <Route path="history" element={<History />} />
        <Route path="analysis/:runId" element={<Analysis />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
