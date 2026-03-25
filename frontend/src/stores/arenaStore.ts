/* ────────────────────────────────────────────
   Arena store — live run state via WebSocket
   ──────────────────────────────────────────── */

import { create } from "zustand";
import type { Message, PhaseType, RunStatus, Vote, WSEvent } from "../types";
import { arenaSocket } from "../services/ws";

interface ArenaState {
  runId: string | null;
  status: RunStatus | null;
  currentRound: number;
  messages: Message[];
  votes: Vote[];
  agents: string[];
  events: WSEvent[];

  /** Connect WebSocket and subscribe to events — call once at app startup. */
  initGlobal: () => void;
  reset: () => void;
}

export const useArenaStore = create<ArenaState>((set) => ({
  runId: null,
  status: null,
  currentRound: 0,
  messages: [],
  votes: [],
  agents: [],
  events: [],

  initGlobal: () => {
    console.log("[ArenaStore] initGlobal() called");
    arenaSocket.connect();
    arenaSocket.subscribe((event) => {
      console.log("[ArenaStore] Processing event:", event.type);
      set((s) => {
        const events = [...s.events, event];

        switch (event.type) {
          case "run_start":
            return {
              ...s,
              events,
              runId: event.run_id,
              status: "running" as RunStatus,
              agents: event.agents,
              currentRound: 0,
              messages: [],
              votes: [],
            };
          case "run_end":
            return { ...s, events, status: event.status as RunStatus };
          case "round_start":
            return { ...s, events, currentRound: event.round };
          case "message":
            return {
              ...s,
              events,
              messages: [
                ...s.messages,
                {
                  agent_id: event.agent_id,
                  agent_name: event.agent_name,
                  phase: event.phase as PhaseType,
                  content: event.content,
                  timestamp: new Date().toISOString(),
                  tokens_used: event.tokens ?? 0,
                  response_time_ms: event.response_time_ms ?? 0,
                },
              ],
            };
          case "vote":
            return {
              ...s,
              events,
              votes: [
                ...s.votes,
                {
                  agent_id: event.agent_id,
                  agent_name: event.agent_name,
                  target: event.target,
                  round_number: s.currentRound,
                },
              ],
            };
          default:
            return { ...s, events };
        }
      });
    });
  },

  reset: () =>
    set({
      runId: null,
      status: null,
      currentRound: 0,
      messages: [],
      votes: [],
      agents: [],
      events: [],
    }),
}));
