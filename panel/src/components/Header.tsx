"use client";

import React from "react";
import { LogoMark } from "./LogoMark";
import { Power, Palette, Music } from "lucide-react";

export type ThemeOption = "dark" | "light" | "nordic" | "sage" | "espresso" | "midnight" | "sandstone";

interface HeaderProps {
  currentTheme: ThemeOption;
  onThemeChange: (theme: ThemeOption) => void;
  isBackendConnected: boolean;
  activeMedia?: { title: string; type: "music" | "video" } | null;
}

const THEME_LABELS: Record<ThemeOption, string> = {
  dark: "Obsidian Slate",
  light: "Warm Parchment",
  nordic: "Nordic Fog",
  sage: "Kyoto Moss",
  espresso: "Espresso Wood",
  midnight: "Midnight Indigo",
  sandstone: "Sandstone Dune",
};

export const Header: React.FC<HeaderProps> = ({
  currentTheme,
  onThemeChange,
  isBackendConnected,
  activeMedia,
}) => {
  return (
    <header className="flex items-center justify-between px-4 py-3 border-b border-[var(--border)] bg-[var(--surface)] select-none">
      {/* Brand & Mark */}
      <div className="flex items-center gap-3">
        <LogoMark size={26} />
        <div>
          <h1 className="text-base font-semibold tracking-tight text-[var(--text-primary)]">
            Luna
          </h1>
          <span className="text-[10px] tracking-wider uppercase text-[var(--text-secondary)]">
            Personal Assistant
          </span>
        </div>
      </div>

      {/* Currently Playing Media Status Pill */}
      {activeMedia && (
        <div className="hidden sm:flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-[var(--surface-alt)] border border-[var(--border)] text-[11px] text-[var(--text-primary)] animate-pulse">
          <Music className="w-3 h-3 text-[var(--accent)]" />
          <span className="truncate max-w-[120px]">{activeMedia.title}</span>
        </div>
      )}

      {/* Controls */}
      <div className="flex items-center gap-2.5">
        {/* Theme Selector Dropdown */}
        <div className="relative flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md bg-[var(--bg)] border border-[var(--border)]">
          <Palette className="w-3.5 h-3.5 text-[var(--accent)]" />
          <select
            value={currentTheme}
            onChange={(e) => onThemeChange(e.target.value as ThemeOption)}
            aria-label="Select theme preset"
            className="bg-transparent text-[var(--text-primary)] text-xs focus:outline-none cursor-pointer pr-1"
          >
            {Object.entries(THEME_LABELS).map(([value, label]) => (
              <option key={value} value={value} className="bg-[#222831] text-[#DFD0B8]">
                {label}
              </option>
            ))}
          </select>
        </div>

        {/* Backend Status Indicator */}
        <div
          role="status"
          aria-label={isBackendConnected ? "Backend online" : "Backend offline"}
          title={isBackendConnected ? "Backend Online" : "Backend Offline"}
          className="flex items-center justify-center p-1.5 rounded-md border border-[var(--border)]"
        >
          <Power
            className={`w-4 h-4 transition-colors ${
              isBackendConnected ? "text-emerald-400" : "text-amber-500/70"
            }`}
          />
        </div>
      </div>
    </header>
  );
};
