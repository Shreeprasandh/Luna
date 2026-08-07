"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Palette, Volume2, Shield, Sparkles } from "lucide-react";
import { ThemeOption } from "./Header";

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentTheme: ThemeOption;
  onThemeChange: (theme: ThemeOption) => void;
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

export const SettingsModal: React.FC<SettingsModalProps> = ({
  isOpen,
  onClose,
  currentTheme,
  onThemeChange,
}) => {
  const [speechRate, setSpeechRate] = useState(175);
  const [pitch, setPitch] = useState(50);
  const [voiceGender, setVoiceGender] = useState<"female" | "male">("female");

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="w-full max-w-sm rounded-2xl bg-[var(--surface)] border border-[var(--border-strong)] shadow-2xl p-5 space-y-5 text-[var(--text-primary)]"
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-[var(--border)] pb-3">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[var(--accent)]" />
              <h2 className="text-sm font-semibold tracking-wide">Luna System Settings</h2>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-md text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-alt)] transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Theme Preset Selector */}
          <div className="space-y-2">
            <label className="flex items-center gap-1.5 text-xs font-medium text-[var(--text-secondary)]">
              <Palette className="w-3.5 h-3.5 text-[var(--accent)]" />
              <span>Theme Preset</span>
            </label>
            <select
              value={currentTheme}
              onChange={(e) => onThemeChange(e.target.value as ThemeOption)}
              className="w-full p-2 text-xs rounded-lg bg-[var(--bg)] border border-[var(--border)] text-[var(--text-primary)] focus:outline-none focus:border-[var(--accent)] cursor-pointer"
            >
              {Object.entries(THEME_LABELS).map(([val, label]) => (
                <option key={val} value={val} className="bg-[#222831] text-[#DFD0B8]">
                  {label}
                </option>
              ))}
            </select>
          </div>

          {/* Voice Personality Settings */}
          <div className="space-y-3 border-t border-[var(--border)] pt-3">
            <label className="flex items-center gap-1.5 text-xs font-medium text-[var(--text-secondary)]">
              <Volume2 className="w-3.5 h-3.5 text-[var(--accent)]" />
              <span>AI TTS Voice Personality</span>
            </label>

            <div className="space-y-1.5 text-xs">
              <div className="flex justify-between text-[11px] text-[var(--text-secondary)]">
                <span>Speech Speed</span>
                <span>{speechRate} WPM</span>
              </div>
              <input
                type="range"
                min="100"
                max="250"
                value={speechRate}
                onChange={(e) => setSpeechRate(Number(e.target.value))}
                className="w-full accent-[var(--accent)] cursor-pointer"
              />
            </div>

            <div className="space-y-1.5 text-xs">
              <div className="flex justify-between text-[11px] text-[var(--text-secondary)]">
                <span>Voice Pitch</span>
                <span>{pitch}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={pitch}
                onChange={(e) => setPitch(Number(e.target.value))}
                className="w-full accent-[var(--accent)] cursor-pointer"
              />
            </div>

            <div className="flex gap-2 pt-1">
              <button
                onClick={() => setVoiceGender("female")}
                className={`flex-1 py-1.5 text-xs rounded-md border text-center transition-all ${
                  voiceGender === "female"
                    ? "bg-[var(--surface-alt)] border-[var(--accent)] text-[var(--text-primary)] font-medium"
                    : "border-[var(--border)] text-[var(--text-secondary)]"
                }`}
              >
                Female Voice
              </button>
              <button
                onClick={() => setVoiceGender("male")}
                className={`flex-1 py-1.5 text-xs rounded-md border text-center transition-all ${
                  voiceGender === "male"
                    ? "bg-[var(--surface-alt)] border-[var(--accent)] text-[var(--text-primary)] font-medium"
                    : "border-[var(--border)] text-[var(--text-secondary)]"
                }`}
              >
                Male Voice
              </button>
            </div>
          </div>

          {/* Security Status - Secrets Hidden */}
          <div className="border-t border-[var(--border)] pt-3 text-[11px] text-[var(--text-secondary)] space-y-1.5">
            <div className="flex items-center justify-between text-xs font-medium text-[var(--text-primary)]">
              <div className="flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5 text-emerald-400" />
                <span>Security Protection Status</span>
              </div>
              <span className="text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20">
                ACTIVE
              </span>
            </div>
            <p className="text-[10px] text-[var(--text-secondary)] leading-relaxed">
              Master Access Credentials & Administrative Secrets are securely encrypted in server environment variables.
            </p>
          </div>

          <button
            onClick={onClose}
            className="w-full py-2 text-xs font-semibold rounded-lg bg-[var(--accent)] text-[var(--bg)] hover:opacity-90 transition-opacity"
          >
            Save & Apply Settings
          </button>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
