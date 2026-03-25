/* ────────────────────────────────────────────
   WebSocket service — real-time arena updates
   ──────────────────────────────────────────── */

import type { WSEvent } from "../types";

type Listener = (event: WSEvent) => void;

class ArenaSocket {
  private ws: WebSocket | null = null;
  private listeners: Set<Listener> = new Set();
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private _connected = false;
  private _pendingResolvers: Array<() => void> = [];

  get connected() {
    return this._connected;
  }

  connect() {
    if (this.ws && this.ws.readyState <= WebSocket.OPEN) {
      console.log("[WS] connect() skipped — already connected/connecting, readyState:", this.ws.readyState);
      return;
    }

    const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
    const url = `${proto}//${window.location.host}/ws/arena`;
    console.log("[WS] Connecting to", url);

    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log("[WS] ✅ Connected!");
      this._connected = true;
      this._pendingResolvers.forEach((r) => r());
      this._pendingResolvers = [];
      this.startPing();
    };

    this.ws.onmessage = (ev) => {
      if (ev.data === "pong") return;
      try {
        const event = JSON.parse(ev.data) as WSEvent;
        console.log("[WS] 📨 Event:", event.type, event);
        this.listeners.forEach((fn) => fn(event));
      } catch {
        // ignore non-JSON messages
      }
    };

    this.ws.onclose = (ev) => {
      console.log("[WS] ❌ Closed, code:", ev.code, "reason:", ev.reason);
      this._connected = false;
      this.scheduleReconnect();
    };

    this.ws.onerror = (ev) => {
      console.error("[WS] ⚠️ Error:", ev);
      this.ws?.close();
    };
  }

  /** Returns a promise that resolves once the WebSocket is open. */
  waitForConnection(): Promise<void> {
    if (this._connected) return Promise.resolve();
    return new Promise((resolve) => {
      this._pendingResolvers.push(resolve);
      this.connect();
    });
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    this.ws?.close();
    this.ws = null;
    this._connected = false;
  }

  subscribe(fn: Listener): () => void {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  }

  private startPing() {
    const interval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send("ping");
      } else {
        clearInterval(interval);
      }
    }, 30_000);
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, 3000);
  }
}

export const arenaSocket = new ArenaSocket();
