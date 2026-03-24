/* ────────────────────────────────────────────
   TypeScript types mirroring backend Pydantic models
   ──────────────────────────────────────────── */

// ─── Provider ─────────────────────────────
export type ProviderType = "ollama" | "lm_studio" | "openrouter";

export interface ProviderConfig {
  type: ProviderType;
  enabled: boolean;
  endpoint: string;
  api_key?: string;
  connected: boolean;
}

export interface ModelInfo {
  id: string;
  name: string;
  provider: ProviderType;
  context_length?: number;
  pricing?: { prompt: number; completion: number };
}

export interface ProviderStatus {
  type: ProviderType;
  available: boolean;
}

// ─── Settings ─────────────────────────────
export interface LLMDefaults {
  temperature: number;
  top_p: number;
  max_tokens: number;
  response_timeout_s: number;
}

export interface AppSettings {
  providers: Record<ProviderType, ProviderConfig>;
  llm_defaults: LLMDefaults;
  fallback_strategy: "ignore" | "replace" | "stop";
  debug_logging: boolean;
}

// ─── Experiment ───────────────────────────
export type ExperimentId =
  | "budget_groupe"
  | "conseil_crise"
  | "traitre_invisible"
  | "enquete_collective"
  | "negociation_ressources"
  | "pouvoir_tourne"
  | "information_fragmentee"
  | "repartition_priorites"
  | "construction_regle"
  | "loi_du_groupe";

export interface Scenario {
  id: string;
  name: string;
  description: string;
  data: Record<string, unknown>;
}

export interface PlotTwist {
  id: string;
  name: string;
  description: string;
  trigger_round?: number;
  intensity: "subtle" | "moderate" | "strong";
}

export interface ExperimentDefinition {
  id: ExperimentId;
  name: string;
  display_name: string;
  icon: string;
  color_primary: string;
  color_secondary: string;
  tagline: string;
  description: string;
  min_agents: number;
  max_agents: number;
  default_agents: number;
  min_rounds: number;
  max_rounds: number;
  default_rounds: number;
  scenarios: Scenario[];
  plot_twists: PlotTwist[];
}

export interface ExperimentSetup {
  experiment_id: ExperimentId;
  scenario_id?: string;
  num_rounds: number;
  enable_plot_twists: boolean;
  plot_twist_intensity: "subtle" | "moderate" | "strong";
  enable_random_events: boolean;
  custom_parameters: Record<string, unknown>;
}

// ─── Agent ────────────────────────────────
export type AgentStatus =
  | "idle"
  | "thinking"
  | "speaking"
  | "waiting"
  | "voting"
  | "eliminated";

export interface AgentConfig {
  id: string;
  name: string;
  model: string;
  provider: ProviderType;
  color: string;
}

// ─── Run ──────────────────────────────────
export type RunStatus = "pending" | "running" | "completed" | "failed" | "cancelled";

export type PhaseType =
  | "introduction"
  | "discussion"
  | "reaction"
  | "vote"
  | "resolution"
  | "event"
  | "plot_twist";

export interface Message {
  agent_id: string;
  agent_name?: string;
  phase: PhaseType;
  content: string;
  timestamp: string;
  tokens_used: number;
  response_time_ms: number;
}

export interface Vote {
  agent_id: string;
  agent_name?: string;
  target: string;
  round_number: number;
  reasoning?: string;
}

export interface RoundData {
  round_number: number;
  instruction?: string;
  messages: Message[];
  votes: Vote[];
  events: Record<string, unknown>[];
  summary?: string;
}

export interface RunConfig {
  experiment: ExperimentSetup;
  agents: AgentConfig[];
  seed?: number;
  temperature: number;
  top_p: number;
  max_tokens: number;
  response_timeout_s: number;
}

export interface RunMetrics {
  total_tokens: number;
  total_messages: number;
  avg_response_time_ms: number;
  duration_s: number;
  rounds_completed: number;
  consensus_reached?: boolean;
  winner?: string;
  agent_metrics: Record<string, Record<string, unknown>>;
}

export interface RunResult {
  run_id: string;
  status: RunStatus;
  experiment_id: ExperimentId;
  config: RunConfig;
  agents: AgentConfig[];
  rounds: RoundData[];
  metrics?: RunMetrics;
  created_at: string;
  completed_at?: string;
  error?: string;
}

export interface RunSummary {
  run_id: string;
  experiment_id: ExperimentId;
  experiment_name: string;
  status: RunStatus;
  agent_count: number;
  rounds_completed: number;
  total_rounds: number;
  created_at: string;
  duration_s?: number;
  consensus_reached?: boolean;
}

// ─── WebSocket Events ─────────────────────
export type WSEvent =
  | { type: "run_start"; run_id: string; experiment: string; agents: string[] }
  | { type: "run_end"; run_id: string; status: string; error?: string }
  | { type: "round_start"; run_id: string; round: number }
  | { type: "agent_message"; run_id: string; agent_id: string; agent_name: string; phase: PhaseType; content: string }
  | { type: "agent_vote"; run_id: string; agent_id: string; agent_name: string; target: string }
  | { type: "event"; round: number; [key: string]: unknown };
