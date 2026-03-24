/* ────────────────────────────────────────────
   Experiment store — loaded once from API
   ──────────────────────────────────────────── */

import { create } from "zustand";
import type { ExperimentDefinition, ExperimentId } from "../types";
import { experiments as api } from "../services/api";

interface ExperimentStore {
  experiments: ExperimentDefinition[];
  loading: boolean;
  error: string | null;
  fetch: () => Promise<void>;
  getById: (id: ExperimentId) => ExperimentDefinition | undefined;
}

export const useExperimentStore = create<ExperimentStore>((set, get) => ({
  experiments: [],
  loading: false,
  error: null,

  fetch: async () => {
    if (get().experiments.length > 0) return;
    set({ loading: true, error: null });
    try {
      const data = await api.list();
      set({ experiments: data, loading: false });
    } catch (e) {
      set({ error: (e as Error).message, loading: false });
    }
  },

  getById: (id) => get().experiments.find((e) => e.id === id),
}));
