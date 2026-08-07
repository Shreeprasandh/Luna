"use client";

import React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Image as ImageIcon, Download, FileText } from "lucide-react";

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
}

export const ChatArea: React.FC<ChatAreaProps> = ({ messages, isLoading }) => {
  const bottomRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div
      role="log"
      aria-live="polite"
      className="flex-1 overflow-y-auto p-4 space-y-4 bg-[var(--bg)]"
    >

      <AnimatePresence initial={false}>
        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className={`flex flex-col ${
              msg.role === "user" ? "items-end" : "items-start"
            }`}
          >
            <div
              className={`max-w-[88%] p-3.5 rounded-lg border text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-[var(--surface-alt)] border-[var(--border-strong)] text-[var(--text-primary)]"
                  : "bg-[var(--surface)] border-[var(--border)] text-[var(--text-primary)]"
              }`}
            >
              {/* Message Text */}
              <div className="whitespace-pre-wrap font-sans">{msg.text}</div>

              {/* Render Image Gallery Payload if Present */}
              {msg.images && msg.images.length > 0 && (
                <div className="mt-3 grid grid-cols-2 gap-2 border-t border-[var(--border)] pt-3">
                  {msg.images.map((img, idx) => (
                    <a
                      key={idx}
                      href={img.image_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group relative block overflow-hidden rounded border border-[var(--border)] bg-[var(--code-bg)] p-1 transition-opacity hover:opacity-90"
                    >
                      <img
                        src={img.image_url}
                        alt={img.title}
                        className="h-24 w-full object-cover rounded"
                        onError={(e) => {
                          (e.target as HTMLElement).style.display = "none";
                        }}
                      />
                      <div className="mt-1 flex items-center gap-1 text-[11px] text-[var(--text-secondary)] truncate">
                        <ImageIcon className="w-3 h-3 flex-shrink-0" />
                        <span className="truncate">{img.title}</span>
                      </div>
                    </a>
                  ))}
                </div>
              )}

              {/* Render 1-Tap Mobile Download Card if Present */}
              {msg.download_url && (
                <div className="mt-3 border-t border-[var(--border)] pt-3">
                  <a
                    href={msg.download_url}
                    download={msg.file_name || "file"}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-between gap-3 p-2.5 rounded-lg bg-[var(--surface-alt)] border border-[var(--border-strong)] text-xs text-[var(--text-primary)] hover:border-[var(--accent)] active:scale-98 transition-all"
                  >
                    <div className="flex items-center gap-2 truncate">
                      <FileText className="w-4 h-4 text-[var(--accent)] flex-shrink-0" />
                      <span className="truncate font-medium">{msg.file_name || "Download File"}</span>
                    </div>
                    <div className="flex items-center gap-1 px-2 py-1 rounded bg-[var(--accent)] text-[var(--bg)] font-semibold text-[11px]">
                      <Download className="w-3 h-3" />
                      <span>Download</span>
                    </div>
                  </a>
                </div>
              )}
            </div>

            {/* Timestamp */}
            <span className="mt-1 text-[10px] text-[var(--text-secondary)] px-1">
              {msg.timestamp}
            </span>
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Sleek Visual Live Tool / Research Animation Indicator */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className="flex items-center gap-2.5 px-3.5 py-2.5 w-fit rounded-lg bg-[var(--surface)] border border-[var(--border-strong)] text-xs text-[var(--text-primary)] shadow-sm"
        >
          <div className="relative flex items-center justify-center w-3.5 h-3.5">
            <div className="absolute w-3.5 h-3.5 rounded-full border-2 border-t-[var(--accent)] border-r-transparent border-b-transparent border-l-transparent animate-spin" />
            <div className="w-1.5 h-1.5 rounded-full bg-[var(--accent)]" />
          </div>
          <span className="font-mono text-[11px] text-[var(--text-primary)] tracking-wide">
            Gathering data & synthesizing key points, Sir...
          </span>
        </motion.div>
      )}

      <div ref={bottomRef} />
    </div>
  );
};
