"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Terminal, 
  GitBranch, 
  Cpu, 
  Clock, 
  CheckCircle2, 
  AlertCircle, 
  ChevronRight, 
  ChevronDown, 
  Database,
  Layers,
  Sparkles
} from "lucide-react";

export interface DAGNode {
  id: string;
  name: string;
  type: "intent" | "tool" | "memory" | "synthesizer" | "safety_gate";
  status: "pending" | "running" | "success" | "failed";
  durationMs?: number;
  args?: Record<string, any>;
  result?: Record<string, any> | string;
  timestamp: string;
}

interface ReasoningDAGProps {
  nodes?: DAGNode[];
  thoughtStream?: string[];
  activeStep?: string;
  tokenVelocity?: number;
  totalLatencyMs?: number;
  className?: string;
}

const mockDefaultNodes: DAGNode[] = [
  {
    id: "node-1",
    name: "System 1 Intent Router",
    type: "intent",
    status: "success",
    durationMs: 42,
    args: { intent: "executive_briefing", confidence: 0.98 },
    result: { target: "multi_subsystem_dispatch" },
    timestamp: "22:30:12",
  },
  {
    id: "node-2",
    name: "Supabase Memory Context",
    type: "memory",
    status: "success",
    durationMs: 76,
    args: { query_vector: "768-d", table: "memories" },
    result: { retrieved: 3, top_cosine_sim: 0.89 },
    timestamp: "22:30:12",
  },
  {
    id: "node-3",
    name: "Subsystem Actuation [git_agent]",
    type: "tool",
    status: "success",
    durationMs: 148,
    args: { action: "status_summary", repos: ["Luna", "idlebin"] },
    result: { clean: 1, modified: 1 },
    timestamp: "22:30:13",
  },
  {
    id: "node-4",
    name: "Synthesizer & Audio Telemetry",
    type: "synthesizer",
    status: "running",
    durationMs: 95,
    timestamp: "22:30:13",
  },
];

export const ReasoningDAG: React.FC<ReasoningDAGProps> = ({
  nodes = mockDefaultNodes,
  thoughtStream = [
    "Evaluating semantic intent across 60 registered tools...",
    "Anchor project verified: /Users/shreeprasandhk/shree_projects/Luna",
    "Validating AST safety boundaries and file permissions...",
    "Dispatching parallel execution workers to local substrate...",
  ],
  activeStep = "Synthesizing conversational response",
  tokenVelocity = 84,
  totalLatencyMs = 361,
  className = "",
}) => {
  const [expandedNodeId, setExpandedNodeId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedNodeId(prev => (prev === id ? null : id));
  };

  const getNodeIcon = (type: DAGNode["type"]) => {
    switch (type) {
      case "intent":
        return <Cpu className="w-3.5 h-3.5 text-sky-400" />;
      case "tool":
        return <Terminal className="w-3.5 h-3.5 text-amber-400" />;
      case "memory":
        return <Database className="w-3.5 h-3.5 text-emerald-400" />;
      case "safety_gate":
        return <Layers className="w-3.5 h-3.5 text-rose-400" />;
      case "synthesizer":
        return <Sparkles className="w-3.5 h-3.5 text-purple-400" />;
    }
  };

  return (
    <div className={`flex flex-col h-full bg-[#0B0D11]/90 backdrop-blur-xl border border-white/[0.06] rounded-2xl overflow-hidden select-none ${className}`}>
      {/* Telemetry Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-white/[0.05] bg-white/[0.01]">
        <div className="flex items-center gap-2">
          <GitBranch className="w-4 h-4 text-amber-400/90" />
          <span className="text-xs font-medium tracking-wide text-white/90">
            Synaptic Telemetry & Reasoning DAG
          </span>
        </div>
        <div className="flex items-center gap-3 text-[11px] font-mono text-white/50">
          <div className="flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>{tokenVelocity} t/s</span>
          </div>
          <div className="flex items-center gap-1 border-l border-white/10 pl-3">
            <Clock className="w-3 h-3 text-white/40" />
            <span>{totalLatencyMs}ms</span>
          </div>
        </div>
      </div>

      {/* Thought Stream Ticker */}
      <div className="px-4 py-2.5 bg-white/[0.015] border-b border-white/[0.04]">
        <div className="flex items-center gap-2 mb-1.5">
          <span className="text-[10px] uppercase font-mono tracking-wider text-amber-400/80">
            Active Deliberation
          </span>
          <span className="text-[10px] font-mono text-white/40">· Live Stream</span>
        </div>
        <div className="space-y-1 font-mono text-xs text-white/70 max-h-24 overflow-y-auto">
          {thoughtStream.map((thought, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: -6 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.16, ease: [0.16, 1, 0.3, 1] }}
              className="flex items-start gap-1.5 text-white/60 hover:text-white/90 transition-colors"
            >
              <span className="text-white/20 select-none">›</span>
              <span className="leading-relaxed">{thought}</span>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Execution DAG Nodes */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2.5">
        <div className="text-[10px] uppercase font-mono tracking-wider text-white/40 mb-1">
          Execution Pipeline ({nodes.length} Nodes)
        </div>
        
        {nodes.map((node, index) => {
          const isExpanded = expandedNodeId === node.id;
          const isLast = index === nodes.length - 1;

          return (
            <div key={node.id} className="relative group">
              {/* Vertical connector line */}
              {!isLast && (
                <div className="absolute left-[17px] top-[32px] bottom-[-10px] w-px bg-white/[0.08] group-hover:bg-white/[0.15] transition-colors" />
              )}

              <div
                onClick={() => toggleExpand(node.id)}
                className={`flex flex-col p-2.5 rounded-xl border transition-all duration-200 cursor-pointer ${
                  node.status === "running"
                    ? "bg-amber-500/[0.05] border-amber-500/30 shadow-[0_0_15px_rgba(245,166,35,0.06)]"
                    : node.status === "success"
                    ? "bg-white/[0.02] border-white/[0.06] hover:border-white/[0.12] hover:bg-white/[0.035]"
                    : "bg-rose-500/[0.05] border-rose-500/30"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    {/* Status badge circle */}
                    <div className="relative flex items-center justify-center w-6 h-6 rounded-lg bg-white/[0.04] border border-white/[0.08]">
                      {getNodeIcon(node.type)}
                      {node.status === "running" && (
                        <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-amber-400 animate-ping" />
                      )}
                    </div>

                    <div>
                      <div className="text-xs font-medium text-white/90">
                        {node.name}
                      </div>
                      <div className="text-[10px] font-mono text-white/40">
                        {node.type.toUpperCase()} · {node.timestamp}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {node.durationMs && (
                      <span className="text-[10px] font-mono text-white/50 bg-white/[0.04] px-1.5 py-0.5 rounded">
                        {node.durationMs}ms
                      </span>
                    )}
                    {node.status === "success" && (
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    )}
                    {node.status === "running" && (
                      <div className="w-3.5 h-3.5 border-2 border-amber-400 border-t-transparent rounded-full animate-spin" />
                    )}
                    {node.status === "failed" && (
                      <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
                    )}
                    {isExpanded ? (
                      <ChevronDown className="w-3.5 h-3.5 text-white/40" />
                    ) : (
                      <ChevronRight className="w-3.5 h-3.5 text-white/40" />
                    )}
                  </div>
                </div>

                {/* Expanded Inspection Drawer */}
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
                      className="mt-2.5 pt-2 border-t border-white/[0.06] overflow-hidden"
                    >
                      {node.args && (
                        <div className="mb-2">
                          <div className="text-[10px] font-mono uppercase text-white/40 mb-1">
                            Input Parameters:
                          </div>
                          <pre className="p-2 rounded bg-black/40 text-[11px] font-mono text-amber-200/80 overflow-x-auto">
                            {JSON.stringify(node.args, null, 2)}
                          </pre>
                        </div>
                      )}
                      {node.result && (
                        <div>
                          <div className="text-[10px] font-mono uppercase text-white/40 mb-1">
                            Execution Return:
                          </div>
                          <pre className="p-2 rounded bg-black/40 text-[11px] font-mono text-emerald-300/80 overflow-x-auto">
                            {JSON.stringify(node.result, null, 2)}
                          </pre>
                        </div>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer Status Bar */}
      <div className="px-4 py-2 border-t border-white/[0.05] bg-white/[0.01] flex items-center justify-between text-[11px] font-mono text-white/50">
        <span className="truncate max-w-[220px]">
          Target: <span className="text-white/80">Headless macOS Substrate</span>
        </span>
        <span className="text-emerald-400/90 font-medium">Synced · Zero Defect</span>
      </div>
    </div>
  );
};
