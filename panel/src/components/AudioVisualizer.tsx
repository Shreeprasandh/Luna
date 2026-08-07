"use client";

import React from "react";
import { motion } from "framer-motion";
import { Volume2 } from "lucide-react";

interface AudioVisualizerProps {
  isActive?: boolean;
  label?: string;
}

export const AudioVisualizer: React.FC<AudioVisualizerProps> = ({
  isActive = true,
  label = "Luna Voice / Audio Active",
}) => {
  if (!isActive) return null;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="flex items-center gap-3 px-3.5 py-2 rounded-xl bg-[var(--surface-alt)] border border-[var(--border-strong)] shadow-lg backdrop-blur-md"
    >
      <div className="flex items-center gap-1.5 h-4">
        <Volume2 className="w-4 h-4 text-[var(--accent)] flex-shrink-0 animate-pulse" />
        {[0.4, 0.8, 0.3, 0.9, 0.5, 0.7, 0.2].map((height, i) => (
          <motion.div
            key={i}
            animate={{
              height: ["4px", "16px", "6px", "14px", "4px"],
            }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              repeatType: "reverse",
              delay: i * 0.1,
            }}
            className="w-1 rounded-full bg-[var(--accent)]"
          />
        ))}
      </div>
      <span className="text-[11px] font-mono text-[var(--text-primary)] tracking-wide truncate">
        {label}
      </span>
    </motion.div>
  );
};
