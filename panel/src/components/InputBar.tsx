"use client";

import React, { useState } from "react";
import { Mic, Send, Sparkles, AudioWaveform, Terminal, Zap } from "lucide-react";

interface InputBarProps {
  onSendMessage: (text: string, mode?: "fast" | "cli") => void;
  onVoiceToggle: () => void;
  isListening: boolean;
  disabled: boolean;
  audioLevel?: number;
  execMode?: "fast" | "cli";
  onToggleExecMode?: () => void;
}

export const InputBar: React.FC<InputBarProps> = ({
  onSendMessage,
  onVoiceToggle,
  isListening,
  disabled,
  audioLevel = 0,
  execMode = "fast",
  onToggleExecMode,
}) => {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSendMessage(text.trim(), execMode);
    setText("");
  };

  return (
    <footer className="p-3 border-t border-white/[0.06] bg-[#07080A]/90 backdrop-blur-xl z-20">
      <form onSubmit={handleSubmit} className="flex items-center gap-2 max-w-4xl mx-auto">
        {/* Voice Toggle */}
        <button
          type="button"
          aria-label={isListening ? "Mute Voice Stream" : "Activate Full-Duplex Voice"}
          onClick={onVoiceToggle}
          title={isListening ? "Mute Voice Stream" : "Speak to Luna"}
          className={`relative flex items-center justify-center p-2.5 rounded-xl border transition-all cursor-pointer ${
            isListening
              ? "bg-amber-400/20 border-amber-400/50 text-amber-300 shadow-[0_0_15px_rgba(245,166,35,0.2)]"
              : "bg-white/[0.03] hover:bg-white/[0.07] border-white/[0.06] text-white/50 hover:text-white"
          }`}
        >
          <Mic className={`w-4 h-4 ${isListening ? "animate-pulse" : ""}`} />
          {isListening && (
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping" />
          )}
        </button>

        {/* Input Field */}
        <div className="relative flex-1">
          <input
            type="text"
            value={text}
            onChange={e => setText(e.target.value)}
            placeholder={
              isListening
                ? "Luna is listening to your voice..."
                : "Enter command, project query, or actuation directive (e.g. 'audit repos', 'briefing')..."
            }
            aria-label="User prompt input"
            disabled={disabled}
            className="w-full px-4 py-2.5 text-xs rounded-xl bg-white/[0.03] border border-white/[0.07] text-white placeholder-white/30 focus:outline-none focus:border-amber-400/50 focus:bg-white/[0.045] transition-all"
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1 text-[10px] font-mono text-white/20 select-none pointer-events-none">
            <span>⏎ send</span>
          </div>
        </div>

        {/* CLI vs Fast Voice Mode Toggle */}
        {onToggleExecMode && (
          <button
            type="button"
            onClick={onToggleExecMode}
            title={
              execMode === "cli"
                ? "Switch to Fast Voice Mode (Instant sub-200ms audio conversational response)"
                : "Switch to CLI Mode (Dispatches directly to agy terminal agent)"
            }
            className={`flex items-center gap-1.5 px-3 py-2 rounded-xl border text-[11px] font-mono transition-all cursor-pointer ${
              execMode === "cli"
                ? "bg-sky-500/15 border-sky-500/30 text-sky-300 shadow-sm"
                : "bg-amber-400/15 border-amber-400/30 text-amber-300"
            }`}
          >
            {execMode === "cli" ? (
              <>
                <Terminal className="w-3.5 h-3.5 text-sky-400" />
                <span className="hidden sm:inline">CLI Mode</span>
              </>
            ) : (
              <>
                <Zap className="w-3.5 h-3.5 text-amber-400" />
                <span className="hidden sm:inline">Fast Voice</span>
              </>
            )}
          </button>
        )}

        {/* Send Button */}
        <button
          type="submit"
          aria-label="Send message"
          disabled={!text.trim() || disabled}
          className="flex items-center justify-center p-2.5 rounded-xl border border-amber-400/30 bg-amber-400 text-black font-semibold hover:bg-amber-300 disabled:opacity-30 disabled:hover:bg-amber-400 transition-all cursor-pointer shadow-sm"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </footer>
  );
};
