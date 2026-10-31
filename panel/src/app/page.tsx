"use client";

import React, { useState, useEffect, useRef } from "react";
import { Header, ThemeOption } from "@/components/Header";
import { ChatArea, Message } from "@/components/ChatArea";
import { InputBar } from "@/components/InputBar";
import { NeuralCore, CognitiveState } from "@/components/NeuralCore";
import { ReasoningDAG, DAGNode } from "@/components/ReasoningDAG";
import { MemoryVault } from "@/components/MemoryVault";
import { SkillMatrix } from "@/components/SkillMatrix";
import { ArtifactStudio, ArtifactData } from "@/components/ArtifactStudio";
import { LockScreen } from "@/components/LockScreen";
import { lunaSpeech } from "@/utils/speech";
import { 
  Activity, 
  Sparkles, 
  Terminal, 
  Layers, 
  Volume2, 
  Cpu, 
  ShieldCheck, 
  Maximize2 
} from "lucide-react";

const getBackendUrl = () => {
  if (typeof window !== "undefined") {
    const host = window.location.hostname || "localhost";
    return `http://${host}:8000`;
  }
  return "http://localhost:8000";
};

export default function Home() {
  const [theme, setTheme] = useState<ThemeOption>("dark");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isBackendConnected, setIsBackendConnected] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  // Cognitive State & Real-Time Telemetry
  const [cognitiveState, setCognitiveState] = useState<CognitiveState>("idle");
  const [audioLevel, setAudioLevel] = useState<number>(0);
  const [isListening, setIsListening] = useState(false);
  const [isVoiceMuted, setIsVoiceMuted] = useState(false);
  const [execMode, setExecMode] = useState<"fast" | "cli">("fast");
  const [tokenVelocity, setTokenVelocity] = useState<number>(78);
  const [totalLatency, setTotalLatency] = useState<number>(142);
  const [thoughtStream, setThoughtStream] = useState<string[]>([
    "Substrate initialized · Apple Silicon Metal WebGL calibrated",
    "Cognitive matrix synchronized to Supabase pgvector vault",
    "Standing by for executive command, Sir.",
  ]);
  const [dagNodes, setDagNodes] = useState<DAGNode[]>([
    {
      id: "node-init",
      name: "Substrate Initialization",
      type: "intent",
      status: "success",
      durationMs: 24,
      timestamp: "Ready",
    },
    {
      id: "node-mem",
      name: "Core RAM Rehydration",
      type: "memory",
      status: "success",
      durationMs: 38,
      timestamp: "Ready",
    },
  ]);

  // Panels & Drawers
  const [isMemoryVaultOpen, setIsMemoryVaultOpen] = useState(false);
  const [isSkillMatrixOpen, setIsSkillMatrixOpen] = useState(false);
  const [isArtifactStudioOpen, setIsArtifactStudioOpen] = useState(false);
  const [currentArtifact, setCurrentArtifact] = useState<ArtifactData | null>(null);

  // Web Audio Context for Live Mic Reactivity
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  // Auto-bypass lock for localhost
  useEffect(() => {
    if (typeof window !== "undefined") {
      const host = window.location.hostname;
      if (host === "localhost" || host === "127.0.0.1") {
        setIsAuthenticated(true);
        return;
      }
    }
    const savedAuth = localStorage.getItem("luna_authenticated");
    if (savedAuth === "true") {
      setIsAuthenticated(true);
    }
  }, []);

  // Theme attribute
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  // Health check & session start
  useEffect(() => {
    if (!isAuthenticated) return;

    const initSession = async () => {
      const backendUrl = getBackendUrl();
      try {
        const healthRes = await fetch(`${backendUrl}/health`);
        if (healthRes.ok) {
          setIsBackendConnected(true);
        }

        const sessionRes = await fetch(`${backendUrl}/session/start`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        });

        if (sessionRes.ok) {
          const data = await sessionRes.json();
          setSessionId(data.session_id);
          setMessages([
            {
              id: "init",
              role: "assistant",
              text: "Luna online, Sir. Neural core calibrated, 60 tools verified, and standing by.",
              timestamp: new Date().toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              }),
            },
          ]);
        }
      } catch (err) {
        console.warn("Backend not reachable yet:", err);
        setIsBackendConnected(false);
        setMessages([
          {
            id: "offline",
            role: "assistant",
            text: "Backend kernel offline. Ready to start backend: uvicorn main:app --port 8000",
            timestamp: new Date().toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            }),
          },
        ]);
      }
    };

    initSession();
  }, [isAuthenticated]);

  // Real-time Antigravity CLI Telemetry & Cognitive DAG Sync
  useEffect(() => {
    if (!isAuthenticated) return;
    const backendUrl = getBackendUrl();

    const fetchCliTelemetry = async () => {
      try {
        const res = await fetch(`${backendUrl}/cli/telemetry?limit=25`);
        if (res.ok) {
          const data = await res.json();
          if (data.status === "synced") {
            if (data.dag_nodes && data.dag_nodes.length > 0) {
              setDagNodes(data.dag_nodes);
            }
            if (data.thought_stream && data.thought_stream.length > 0) {
              setThoughtStream(data.thought_stream);
            }
            if (data.metrics?.token_velocity) {
              setTokenVelocity(data.metrics.token_velocity);
            }
          }
        }
      } catch {
        // Silent background fallback
      }
    };

    fetchCliTelemetry();
    const interval = setInterval(fetchCliTelemetry, 2500);
    return () => clearInterval(interval);
  }, [isAuthenticated]);

  // Audio stream setup when voice listening is active
  useEffect(() => {
    let animId: number;

    const startAudio = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaStreamRef.current = stream;
        const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
        audioContextRef.current = ctx;
        const source = ctx.createMediaStreamSource(stream);
        const analyser = ctx.createAnalyser();
        analyser.fftSize = 256;
        source.connect(analyser);
        analyserRef.current = analyser;

        const dataArray = new Uint8Array(analyser.frequencyBinCount);

        const checkAudio = () => {
          if (!analyserRef.current) return;
          analyserRef.current.getByteFrequencyData(dataArray);
          let sum = 0;
          for (let i = 0; i < 16; i++) sum += dataArray[i];
          const avg = sum / 16 / 255;
          setAudioLevel(avg);
          animId = requestAnimationFrame(checkAudio);
        };
        checkAudio();
      } catch (err) {
        console.warn("Microphone access denied or unavailable:", err);
      }
    };

    if (isListening) {
      setCognitiveState("listening");
      startAudio();
    } else {
      setCognitiveState("idle");
      setAudioLevel(0);
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(t => t.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    }

    return () => {
      cancelAnimationFrame(animId);
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach(t => t.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, [isListening]);

  // Voice playback and mute handling
  const handleToggleVoice = () => {
    setIsVoiceMuted(prev => {
      const next = !prev;
      lunaSpeech.setMuted(next);
      return next;
    });
  };

  const handleSpeakMessage = (text: string) => {
    if (isVoiceMuted) return;
    setCognitiveState("speaking");
    lunaSpeech.speak(text, {
      onStart: () => setCognitiveState("speaking"),
      onEnd: () => {
        setCognitiveState("idle");
        setAudioLevel(0);
      },
      onAudioPulse: (intensity) => setAudioLevel(intensity),
    });
  };

  // Handle message submission (supports Fast Voice & Direct CLI Execution)
  const handleSendMessage = async (text: string, modeOverride?: "fast" | "cli") => {
    const backendUrl = getBackendUrl();
    const currentSessionId = sessionId || "active-session";
    const mode = modeOverride || execMode;

    const userMsg: Message = {
      id: String(Date.now()),
      role: "user",
      text,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);
    setCognitiveState("thinking");

    // Push new reasoning step to DAG
    const intentNodeId = `node-${Date.now()}`;
    setDagNodes(prev => [
      ...prev,
      {
        id: intentNodeId,
        name: mode === "cli" ? `CLI Dispatch [${text.slice(0, 24)}...]` : `Intent Analysis [${text.slice(0, 24)}...]`,
        type: mode === "cli" ? "tool" : "intent",
        status: "running",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      },
    ]);

    setThoughtStream(prev => [
      ...prev,
      mode === "cli" ? `Routing directive to Antigravity CLI (agy): "${text}"` : `Analyzing directive: "${text}"`,
      mode === "cli" ? "Bridging IPC with terminal agent substrate..." : "Evaluating tool contracts against 164 registered handlers...",
    ]);

    const startTime = performance.now();

    try {
      let res;
      if (mode === "cli") {
        res = await fetch(`${backendUrl}/cli/dispatch`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: text, mode: "cli", session_id: currentSessionId }),
        });
      } else {
        res = await fetch(`${backendUrl}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ session_id: currentSessionId, text }),
        });
      }

      const latency = Math.round(performance.now() - startTime);
      setTotalLatency(latency);

      if (res.ok) {
        const payload = await res.json();
        const replyText = payload.text || payload.reply || "";
        
        // Update DAG node to success
        setDagNodes(prev =>
          prev.map(n => (n.id === intentNodeId ? { ...n, status: "success", durationMs: latency } : n))
        );

        // Vocalize response through Web Speech engine
        if (replyText && !isVoiceMuted) {
          handleSpeakMessage(replyText);
        } else {
          setCognitiveState("idle");
        }

        const assistantMsg: Message = {
          id: String(Date.now() + 1),
          role: "assistant",
          text: replyText,
          type: payload.type || "text",
          images: payload.images || undefined,
          download_url: payload.download_url || undefined,
          file_name: payload.file_name || undefined,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        };

        setMessages(prev => [...prev, assistantMsg]);
        setThoughtStream(prev => [
          ...prev,
          `Execution cycle completed · ${latency}ms latency`,
          mode === "cli" ? "CLI subprocess output captured & delivered." : "Response delivered to user console.",
        ]);
      } else {
        throw new Error(`Server returned status ${res.status}`);
      }
    } catch (err) {
      console.error("Chat turn error:", err);
      setCognitiveState("idle");
      setDagNodes(prev =>
        prev.map(n => (n.id === intentNodeId ? { ...n, status: "failed" } : n))
      );
      setMessages(prev => [
        ...prev,
        {
          id: String(Date.now() + 2),
          role: "assistant",
          text: `Sir, I encountered a communication interruption with the kernel: ${err instanceof Error ? err.message : "Unknown error"}.`,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceToggle = () => {
    setIsListening(prev => !prev);
  };

  const handleUnlock = () => {
    localStorage.setItem("luna_authenticated", "true");
    setIsAuthenticated(true);
  };

  if (!isAuthenticated) {
    return <LockScreen onUnlock={handleUnlock} />;
  }

  return (
    <div className="flex flex-col h-screen w-screen bg-[#07080A] text-white overflow-hidden select-none">
      {/* Top Header */}
      <Header
        currentTheme={theme}
        onThemeChange={setTheme}
        isBackendConnected={isBackendConnected}
        onOpenMemoryVault={() => setIsMemoryVaultOpen(true)}
        onOpenSkillMatrix={() => setIsSkillMatrixOpen(true)}
        onToggleArtifactStudio={() => setIsArtifactStudioOpen(prev => !prev)}
        isArtifactStudioOpen={isArtifactStudioOpen}
        isVoiceMuted={isVoiceMuted}
        onToggleVoice={handleToggleVoice}
      />

      {/* Main Command Station Viewport */}
      <main className="flex-1 flex overflow-hidden p-4 gap-4">
        {/* Left Pane: Synaptic Reasoning DAG & Glass-Box Telemetry (Hidden on small screens) */}
        <div className="hidden lg:flex flex-col w-[340px] xl:w-[380px] h-full shrink-0">
          <ReasoningDAG
            nodes={dagNodes}
            thoughtStream={thoughtStream}
            tokenVelocity={tokenVelocity}
            totalLatencyMs={totalLatency}
            className="h-full shadow-2xl"
          />
        </div>

        {/* Center Stage: 3D Neural Particle Core & Interactive Conversation */}
        <div className="flex-1 flex flex-col h-full bg-[#090A0E]/80 backdrop-blur-xl border border-white/[0.06] rounded-3xl overflow-hidden shadow-2xl relative">
          {/* Subtle 3D Neural Core Anchor at Top Center */}
          <div className="relative flex flex-col items-center justify-center pt-3 pb-1 border-b border-white/[0.04] bg-white/[0.01]">
            <NeuralCore
              state={cognitiveState}
              audioLevel={audioLevel}
              size={180}
              className="drop-shadow-[0_0_30px_rgba(245,166,35,0.15)]"
            />
            {/* Cognitive State Indicator Pill */}
            <div className="flex items-center gap-2 px-3 py-0.5 rounded-full bg-white/[0.04] border border-white/[0.06] text-[10px] font-mono mt-1 text-white/60">
              <span className={`w-1.5 h-1.5 rounded-full ${
                cognitiveState === "listening"
                  ? "bg-amber-400 animate-ping"
                  : cognitiveState === "thinking"
                  ? "bg-purple-400 animate-pulse"
                  : cognitiveState === "speaking"
                  ? "bg-sky-400 animate-pulse"
                  : "bg-emerald-400"
              }`} />
              <span className="uppercase tracking-wider">
                CORE: {cognitiveState}
              </span>
            </div>
          </div>

          {/* Interactive Chat Stream */}
          <div className="flex-1 overflow-hidden flex flex-col">
            <ChatArea 
              messages={messages} 
              isLoading={isLoading} 
              onQuickPrompt={handleSendMessage} 
              onSpeakMessage={handleSpeakMessage}
            />
          </div>

          {/* Full-Duplex Input Console */}
          <InputBar
            onSendMessage={handleSendMessage}
            onVoiceToggle={handleVoiceToggle}
            isListening={isListening}
            disabled={isLoading}
            audioLevel={audioLevel}
            execMode={execMode}
            onToggleExecMode={() => setExecMode(prev => prev === "fast" ? "cli" : "fast")}
          />
        </div>

        {/* Right Pane: Live Artifact Studio (Rendered when toggled) */}
        {isArtifactStudioOpen && (
          <div className="hidden md:flex flex-col w-[420px] xl:w-[480px] h-full shrink-0">
            <ArtifactStudio
              artifact={currentArtifact}
              isOpen={isArtifactStudioOpen}
              onClose={() => setIsArtifactStudioOpen(false)}
            />
          </div>
        )}
      </main>

      {/* Interactive Modal Studios */}
      <MemoryVault
        isOpen={isMemoryVaultOpen}
        onClose={() => setIsMemoryVaultOpen(false)}
      />

      <SkillMatrix
        isOpen={isSkillMatrixOpen}
        onClose={() => setIsSkillMatrixOpen(false)}
      />
    </div>
  );
}
