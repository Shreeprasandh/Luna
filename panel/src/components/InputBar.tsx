"use client";

import React, { useState } from "react";
import { Mic, Send } from "lucide-react";

interface InputBarProps {
  onSendMessage: (text: string) => void;

  onVoiceToggle: () => void;
  isListening: boolean;
  disabled: boolean;
}

export const InputBar: React.FC<InputBarProps> = ({
  onSendMessage,
  onVoiceToggle,
  isListening,
  disabled,
}) => {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSendMessage(text.trim());
    setText("");
  };

  return (
    <footer className="p-3 border-t border-[var(--border)] bg-[var(--surface)]">
      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        {/* Input Field */}
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={isListening ? "Listening for voice..." : "Ask Luna..."}
          aria-label="User prompt input"
          disabled={disabled}
          className="flex-1 px-3.5 py-2.5 text-sm rounded-md bg-[var(--bg)] border border-[var(--border)] text-[var(--text-primary)] placeholder-[var(--text-secondary)] focus:outline-none focus:border-[var(--border-strong)] transition-colors"
        />


        {/* Send Button */}
        <button
          type="submit"
          aria-label="Send message"
          disabled={!text.trim() || disabled}
          className="p-2.5 rounded-md border border-[var(--border)] bg-[var(--bg)] text-[var(--text-primary)] hover:border-[var(--border-strong)] disabled:opacity-40 transition-colors"
        >
          <Send className="w-4 h-4 text-[var(--text-primary)]" />
        </button>

        {/* Voice Mic Button */}
        <button
          type="button"
          aria-label={isListening ? "Stop voice listening" : "Start voice listening"}
          onClick={onVoiceToggle}
          disabled={disabled}
          className={`relative p-2.5 rounded-md border transition-all ${
            isListening
              ? "bg-[var(--surface-alt)] border-[var(--accent)] text-[var(--accent)]"
              : "bg-[var(--bg)] border-[var(--border)] text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
          }`}
        >
          <Mic className="w-4 h-4" />
          {isListening && (
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-[var(--accent)] animate-pulse" />
          )}
        </button>

      </form>
    </footer>
  );
};
