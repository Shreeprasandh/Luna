"use client";

import React from "react";
import { Mic, Music, Cpu, Terminal, Sparkles } from "lucide-react";

interface MobileQuickBarProps {
  onQuickAction: (actionText: string) => void;
}

export const MobileQuickBar: React.FC<MobileQuickBarProps> = ({ onQuickAction }) => {
  return (
    <div className="sm:hidden flex items-center justify-between gap-1.5 px-3 py-2 border-t border-[var(--border)] bg-[var(--surface-alt)]">
      {/* 1-Tap Laptop Hardware Health */}
      <button
        onClick={() => onQuickAction("Luna, check my laptop system health and battery")}
        className="flex items-center gap-1 px-2.5 py-1.5 rounded-md bg-[var(--bg)] border border-[var(--border)] text-[11px] font-medium text-[var(--text-primary)] active:scale-95 transition-transform"
      >
        <Cpu className="w-3.5 h-3.5 text-[var(--accent)]" />
        <span>PC Health</span>
      </button>

      {/* 1-Tap Laptop Music Remote */}
      <button
        onClick={() => onQuickAction("Luna, play focus music on my laptop")}
        className="flex items-center gap-1 px-2.5 py-1.5 rounded-md bg-[var(--bg)] border border-[var(--border)] text-[11px] font-medium text-[var(--text-primary)] active:scale-95 transition-transform"
      >
        <Music className="w-3.5 h-3.5 text-emerald-400" />
        <span>Play Music</span>
      </button>

      {/* 1-Tap VS Code & Terminal Launcher */}
      <button
        onClick={() => onQuickAction("Luna, launch VS Code and open terminal on my laptop")}
        className="flex items-center gap-1 px-2.5 py-1.5 rounded-md bg-[var(--bg)] border border-[var(--border)] text-[11px] font-medium text-[var(--text-primary)] active:scale-95 transition-transform"
      >
        <Terminal className="w-3.5 h-3.5 text-blue-400" />
        <span>VS Code</span>
      </button>

      {/* 1-Tap Morning Briefing */}
      <button
        onClick={() => onQuickAction("Luna, give me my morning briefing")}
        className="flex items-center gap-1 px-2.5 py-1.5 rounded-md bg-[var(--bg)] border border-[var(--border)] text-[11px] font-medium text-[var(--text-primary)] active:scale-95 transition-transform"
      >
        <Sparkles className="w-3.5 h-3.5 text-amber-400" />
        <span>Briefing</span>
      </button>
    </div>
  );
};
