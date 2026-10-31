"use client";

import React, { useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Image as ImageIcon, Download, FileText, Sparkles, Terminal, Copy, Check, Volume2 } from "lucide-react";
import { LogoMark } from "./LogoMark";

export interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  type?: "text" | "image" | "code" | "download";
  images?: Array<{ title: string; image_url: string; thumbnail?: string }>;
  download_url?: string;
  file_name?: string;
  timestamp: string;
}

interface ChatAreaProps {
  messages: Message[];
  isLoading: boolean;
  onQuickPrompt?: (prompt: string) => void;
  onSpeakMessage?: (text: string) => void;
}

export const ChatArea: React.FC<ChatAreaProps> = ({ 
  messages, 
  isLoading,
  onQuickPrompt,
  onSpeakMessage
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);
  const [copiedId, setCopiedId] = React.useState<string | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const samplePrompts = [
    "Check system load & battery status",
    "Audit git repositories across workspace",
    "Synthesize morning executive briefing",
    "List registered tools and MCP nodes",
  ];

  return (
    <div
      role="log"
      aria-live="polite"
      className="flex-1 overflow-y-auto px-5 py-4 space-y-4 bg-transparent select-text"
    >
      {/* Empty State / Welcome Screen */}
      {messages.length === 0 && (
        <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-4 select-none">
          <div className="p-3 rounded-2xl bg-white/[0.03] border border-white/[0.08] shadow-2xl">
            <LogoMark size={36} />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-white tracking-wide">
              Luna Autonomous Command Station
            </h2>
            <p className="text-xs text-white/40 mt-1 max-w-sm">
              All systems calibrated and ready for multimodal actuation, reasoning, and system control.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full max-w-md pt-2">
            {samplePrompts.map((prompt, idx) => (
              <button
                key={idx}
                onClick={() => onQuickPrompt && onQuickPrompt(prompt)}
                className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white/[0.02] hover:bg-white/[0.06] border border-white/[0.06] text-left text-xs text-white/60 hover:text-white transition-all cursor-pointer"
              >
                <Terminal className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                <span className="truncate">{prompt}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Message List */}
      <AnimatePresence initial={false}>
        {messages.map(msg => {
          const isUser = msg.role === "user";
          const isCopied = copiedId === msg.id;

          return (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 8, scale: 0.99 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
              className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}
            >
              <div className="flex items-start gap-2 max-w-[85%] sm:max-w-[78%]">
                {!isUser && (
                  <div className="mt-1 shrink-0 p-1 rounded-lg bg-white/[0.04] border border-white/[0.08]">
                    <LogoMark size={16} />
                  </div>
                )}

                <div
                  className={`relative group p-3.5 rounded-2xl text-xs leading-relaxed border transition-all ${
                    isUser
                      ? "bg-amber-400/10 border-amber-400/25 text-white shadow-sm"
                      : "bg-[#0E1117] border-white/[0.08] text-white/90 shadow-md"
                  }`}
                >
                  {/* Action buttons (Copy + Speak) */}
                  <div className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 flex items-center gap-1 transition-all">
                    {!isUser && onSpeakMessage && (
                      <button
                        onClick={() => onSpeakMessage(msg.text)}
                        title="Speak response aloud"
                        className="p-1 rounded bg-black/40 text-white/40 hover:text-amber-300 transition-all cursor-pointer"
                      >
                        <Volume2 className="w-3 h-3" />
                      </button>
                    )}
                    <button
                      onClick={() => handleCopy(msg.id, msg.text)}
                      title="Copy response"
                      className="p-1 rounded bg-black/40 text-white/40 hover:text-white transition-all cursor-pointer"
                    >
                      {isCopied ? (
                        <Check className="w-3 h-3 text-emerald-400" />
                      ) : (
                        <Copy className="w-3 h-3" />
                      )}
                    </button>
                  </div>

                  {/* Message Content */}
                  <div className="whitespace-pre-wrap font-sans text-xs">
                    {msg.text}
                  </div>

                  {/* Images */}
                  {msg.images && msg.images.length > 0 && (
                    <div className="mt-3 grid grid-cols-2 gap-2 border-t border-white/[0.06] pt-3">
                      {msg.images.map((img, idx) => (
                        <a
                          key={idx}
                          href={img.image_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="group relative block overflow-hidden rounded-xl border border-white/[0.08] bg-black/40 p-1"
                        >
                          <img
                            src={img.image_url}
                            alt={img.title}
                            className="h-24 w-full object-cover rounded-lg"
                            onError={e => {
                              (e.target as HTMLElement).style.display = "none";
                            }}
                          />
                          <div className="mt-1 flex items-center gap-1 text-[11px] text-white/50 truncate">
                            <ImageIcon className="w-3 h-3 shrink-0" />
                            <span className="truncate">{img.title}</span>
                          </div>
                        </a>
                      ))}
                    </div>
                  )}

                  {/* File Download */}
                  {msg.download_url && (
                    <div className="mt-3 border-t border-white/[0.06] pt-3">
                      <a
                        href={msg.download_url}
                        download={msg.file_name || "file"}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-between gap-3 p-2 rounded-xl bg-white/[0.03] border border-white/[0.08] text-xs text-white hover:border-amber-400/40 transition-all"
                      >
                        <div className="flex items-center gap-2 truncate">
                          <FileText className="w-4 h-4 text-amber-400 shrink-0" />
                          <span className="truncate font-medium">
                            {msg.file_name || "Download File"}
                          </span>
                        </div>
                        <div className="flex items-center gap-1 px-2 py-0.5 rounded bg-amber-400 text-black font-semibold text-[10px]">
                          <Download className="w-3 h-3" />
                          <span>Get</span>
                        </div>
                      </a>
                    </div>
                  )}
                </div>
              </div>

              {/* Timestamp */}
              <span className={`text-[10px] font-mono text-white/30 px-2 mt-1 ${isUser ? "text-right" : "text-left pl-8"}`}>
                {msg.timestamp}
              </span>
            </motion.div>
          );
        })}
      </AnimatePresence>

      {/* Loading Indicator */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className="flex items-center gap-2.5 px-3 py-2 w-fit rounded-xl bg-[#0E1117] border border-amber-400/25 text-xs text-white shadow-sm ml-7"
        >
          <div className="w-3 h-3 border-2 border-amber-400 border-t-transparent rounded-full animate-spin" />
          <span className="font-mono text-[11px] text-amber-300 tracking-wide">
            Synthesizing neural execution trajectory...
          </span>
        </motion.div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};
