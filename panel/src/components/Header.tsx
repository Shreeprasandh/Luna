"use client";

import React, { useState } from "react";
import { LogoMark } from "./LogoMark";
import { 
  Brain, 
  Sliders, 
  Settings, 
  Radio, 
  Sparkles,
  Layers,
  Terminal
} from "lucide-react";
import { SettingsModal } from "./SettingsModal";

export type ThemeOption = "dark" | "light" | "nordic" | "sage" | "espresso" | "midnight" | "sandstone";

interface HeaderProps {
  currentTheme: ThemeOption;
  onThemeChange: (theme: ThemeOption) => void;
  isBackendConnected: boolean;
  onOpenMemoryVault?: () => void;
  onOpenSkillMatrix?: () => void;
  onToggleArtifactStudio?: () => void;
  isArtifactStudioOpen?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  currentTheme,
  onThemeChange,
  isBackendConnected,
  onOpenMemoryVault,
  onOpenSkillMatrix,
  onToggleArtifactStudio,
  isArtifactStudioOpen = false,
}) => {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  return (
    <>
      <header className="flex items-center justify-between px-5 py-3 border-b border-white/[0.06] bg-[#07080A]/90 backdrop-blur-xl select-none z-30">
        {/* Brand & Mark */}
        <div className="flex items-center gap-3">
          <LogoMark size={28} />
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-sm font-semibold tracking-wide text-white">
                Luna
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-amber-400/10 text-amber-300 border border-amber-400/20">
                Neural Cockpit
              </span>
            </div>
            <div className="text-[10px] font-mono tracking-wider text-white/40">
              Autonomous Command Station · Apple Silicon Substrate
            </div>
          </div>
        </div>

        {/* Center Live Substrate Status */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.03] border border-white/[0.05] text-[11px] font-mono text-white/60">
          <span className={`w-2 h-2 rounded-full ${isBackendConnected ? "bg-emerald-400 animate-pulse" : "bg-rose-400"}`} />
          <span>{isBackendConnected ? "Kernel Online · 14ms" : "Reconnecting Substrate..."}</span>
          <span className="text-white/20">|</span>
          <span className="text-white/40">768-d Vector Sync</span>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {/* Cognitive Memory Vault Button */}
          {onOpenMemoryVault && (
            <button
              onClick={onOpenMemoryVault}
              title="Open Cognitive Memory Matrix"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/[0.06] text-xs font-medium text-white/70 hover:text-white transition-all cursor-pointer"
            >
              <Brain className="w-3.5 h-3.5 text-amber-400" />
              <span className="hidden sm:inline">Memory</span>
            </button>
          )}

          {/* 156-Skill Matrix Studio Button */}
          {onOpenSkillMatrix && (
            <button
              onClick={onOpenSkillMatrix}
              title="156-Skill Matrix & Persona Tuning"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/[0.03] hover:bg-white/[0.08] border border-white/[0.06] text-xs font-medium text-white/70 hover:text-white transition-all cursor-pointer"
            >
              <Sliders className="w-3.5 h-3.5 text-purple-400" />
              <span className="hidden sm:inline">Skills</span>
            </button>
          )}

          {/* Artifact Studio Toggle Button */}
          {onToggleArtifactStudio && (
            <button
              onClick={onToggleArtifactStudio}
              title="Toggle Live Artifact & Canvas Studio"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-medium transition-all cursor-pointer ${
                isArtifactStudioOpen
                  ? "bg-amber-400/15 border-amber-400/30 text-amber-300"
                  : "bg-white/[0.03] hover:bg-white/[0.08] border-white/[0.06] text-white/70 hover:text-white"
              }`}
            >
              <Terminal className="w-3.5 h-3.5 text-sky-400" />
              <span className="hidden sm:inline">Canvas</span>
            </button>
          )}

          {/* Settings Gear */}
          <button
            onClick={() => setIsSettingsOpen(true)}
            aria-label="Open Settings"
            title="Luna Settings"
            className="p-2 rounded-xl border border-white/[0.06] bg-white/[0.03] hover:bg-white/[0.08] text-white/60 hover:text-white transition-all cursor-pointer"
          >
            <Settings className="w-3.5 h-3.5" />
          </button>
        </div>
      </header>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        currentTheme={currentTheme}
        onThemeChange={onThemeChange}
      />
    </>
  );
};
