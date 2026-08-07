"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { LogoMark } from "./LogoMark";
import { Mic, Sparkles, X } from "lucide-react";

interface FloatingOrbProps {
  isListening?: boolean;
  onOrbClick?: () => void;
}

export const FloatingOrb: React.FC<FloatingOrbProps> = ({
  isListening = false,
  onOrbClick,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleClick = () => {
    setIsExpanded(!isExpanded);
    if (onOrbClick) onOrbClick();
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 select-none">
      <AnimatePresence>
        {!isExpanded && (
          <motion.button
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 0.4 }}
            whileHover={{ scale: 1.1, opacity: 1 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleClick}
            title="Luna Assistant - Click or Say 'Hey Luna'"
            className={`relative flex items-center justify-center w-14 h-14 rounded-full bg-[var(--surface)] border border-[var(--border-strong)] shadow-2xl backdrop-blur-md cursor-pointer transition-all duration-300 ${
              isListening ? "ring-4 ring-amber-400/50 opacity-100" : ""
            }`}
          >
            {/* Glowing Pulse Ring */}
            <span className="absolute inset-0 rounded-full bg-[var(--accent)]/20 animate-ping pointer-events-none" />

            {/* Inner Logo Mark */}
            <LogoMark size={28} />

            {/* Listening Indicator Icon */}
            {isListening && (
              <span className="absolute -top-1 -right-1 p-1 rounded-full bg-amber-500 text-black">
                <Mic className="w-3 h-3 animate-pulse" />
              </span>
            )}
          </motion.button>
        )}
      </AnimatePresence>
    </div>
  );
};
