/* ────────────────────────────────────────────
   API service — wraps all backend HTTP calls
   ──────────────────────────────────────────── */

import type {
  AppSettings,
  ExperimentDefinition,
  ExperimentId,
  ModelInfo,
  ProviderStatus,
  ProviderType,
  RunConfig,
  RunResult,
  RunSummary,
} from "../types";

const BASE = "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// ─── Experiments ──────────────────────────
export const experiments = {
  list: () => request<ExperimentDefinition[]>("/experiments"),
  get: (id: ExperimentId) => request<ExperimentDefinition>(`/experiments/${id}`),
};

// ─── Providers ────────────────────────────
export const providers = {
  list: () => request<ProviderStatus[]>("/providers"),
  models: (type: ProviderType) => request<ModelInfo[]>(`/providers/${type}/models`),
  test: (type: ProviderType) =>
    request<{ type: string; connected: boolean }>(`/providers/${type}/test`, { method: "POST" }),
};

// ─── Runs ─────────────────────────────────
export const runs = {
  list: () => request<RunSummary[]>("/runs"),
  get: (id: string) => request<RunResult>(`/runs/${id}`),
  start: (config: RunConfig) =>
    request<{ message: string; experiment: string }>("/runs", {
      method: "POST",
      body: JSON.stringify(config),
    }),
  startBatch: (config: RunConfig, numGames: number) =>
    request<{ message: string; experiment: string; num_games: number }>("/runs/batch", {
      method: "POST",
      body: JSON.stringify({ config, num_games: numGames }),
    }),
  delete: (id: string) => request<{ message: string }>(`/runs/${id}`, { method: "DELETE" }),
  exportUrl: (id: string, fmt: "json" | "csv" | "md") => `${BASE}/runs/${id}/export/${fmt}`,
};

// ─── Settings ─────────────────────────────
export const settings = {
  get: () => request<AppSettings>("/settings"),
  update: (s: AppSettings) =>
    request<AppSettings>("/settings", { method: "PUT", body: JSON.stringify(s) }),
};

// ─── Health ───────────────────────────────
export const health = () => request<{ status: string }>("/health");
