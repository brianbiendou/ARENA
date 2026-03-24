/* ────────────────────────────────────────────
   Provider store — available providers & models
   ──────────────────────────────────────────── */

import { create } from "zustand";
import type { ModelInfo, ProviderStatus, ProviderType } from "../types";
import { providers as api } from "../services/api";

interface ProviderStore {
  providers: ProviderStatus[];
  models: Record<ProviderType, ModelInfo[]>;
  loadingModels: boolean;

  fetchProviders: () => Promise<void>;
  fetchModels: (type: ProviderType) => Promise<void>;
  testProvider: (type: ProviderType) => Promise<boolean>;
}

export const useProviderStore = create<ProviderStore>((set, get) => ({
  providers: [],
  models: {} as Record<ProviderType, ModelInfo[]>,
  loadingModels: false,

  fetchProviders: async () => {
    const data = await api.list();
    set({ providers: data });
  },

  fetchModels: async (type) => {
    set({ loadingModels: true });
    try {
      const data = await api.models(type);
      set((s) => ({
        models: { ...s.models, [type]: data },
        loadingModels: false,
      }));
    } catch {
      set({ loadingModels: false });
    }
  },

  testProvider: async (type) => {
    const result = await api.test(type);
    return result.connected;
  },
}));
