"use client";

import React, { useState } from "react";
import { LogoMark } from "./LogoMark";
import { Music, Settings } from "lucide-react";
import { SettingsModal } from "./SettingsModal";

export type ThemeOption = "dark" | "light" | "nordic" | "sage" | "espresso" | "midnight" | "sandstone";

interface HeaderProps {
  currentTheme: ThemeOption;
  onThemeChange: (theme: ThemeOption) => void;
  isBackendConnected: boolean;
  activeMedia?: { title: string; type: "music" | "video" } | null;
}

export const Header: React.FC<HeaderProps> = ({
  currentTheme,
  onThemeChange,
  isBackendConnected,
  activeMedia,
}) => {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  return (
    <>
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
        <div className="flex items-center gap-2">
          {/* Small Low-Opacity Settings Gear Icon */}
          <button
            onClick={() => setIsSettingsOpen(true)}
            aria-label="Open Settings"
            title="Luna System Settings"
            className="p-1.5 rounded-md border border-[var(--border)] bg-[var(--bg)] opacity-40 hover:opacity-100 transition-opacity text-[var(--text-primary)]"
          >
            <Settings className="w-3.5 h-3.5" />
          </button>
        </div>
      </header>

      {/* Glassmorphic Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        currentTheme={currentTheme}
        onThemeChange={onThemeChange}
      />
    </>
  );
};
