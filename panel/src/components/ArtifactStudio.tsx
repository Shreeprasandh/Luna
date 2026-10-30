"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  FileCode, 
  Eye, 
  Copy, 
  Check, 
  Download, 
  Maximize2, 
  Minimize2, 
  X, 
  Terminal, 
  Sparkles,
  GitCommit
} from "lucide-react";

export interface ArtifactData {
  id: string;
  title: string;
  type: "code" | "markdown" | "diff" | "svg";
  language?: string;
  content: string;
  timestamp: string;
}

interface ArtifactStudioProps {
  artifact?: ArtifactData | null;
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

const mockDefaultArtifact: ArtifactData = {
  id: "art-1",
  title: "GLSL Audio-Reactive Vertex Shader",
  type: "code",
  language: "glsl",
  timestamp: "22:35",
  content: `// Luna 3D Synaptic Core Shader
uniform float uTime;
uniform float uAudio;
uniform float uState;

attribute vec3 aRandom;
varying vec3 vPosition;
varying float vAudioIntensity;

void main() {
    vPosition = position;
    vec3 norm = normalize(position);
    
    // Physical harmonic respiration & audio perturbation
    float breath = sin(uTime * 1.5 + aRandom.x * 6.28) * 0.06;
    float audioDisplacement = uAudio * (0.2 + aRandom.y * 0.3);
    
    vec3 evolvedPosition = position + norm * (breath + audioDisplacement);
    vec4 mvPosition = modelViewMatrix * vec4(evolvedPosition, 1.0);
    gl_Position = projectionMatrix * mvPosition;
    gl_PointSize = max(1.5, 3.2 * (220.0 / -mvPosition.z));
}`,
};

export const ArtifactStudio: React.FC<ArtifactStudioProps> = ({
  artifact = mockDefaultArtifact,
  isOpen,
  onClose,
  className = "",
}) => {
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<"code" | "preview">("code");
  const [isExpanded, setIsExpanded] = useState(false);

  const currentArtifact = artifact || mockDefaultArtifact;

  const handleCopy = () => {
    navigator.clipboard.writeText(currentArtifact.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ opacity: 0, x: 24 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 24 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className={`flex flex-col bg-[#0B0D11]/95 backdrop-blur-2xl border border-white/[0.08] rounded-3xl overflow-hidden shadow-2xl ${
        isExpanded ? "fixed inset-6 z-50" : "h-full"
      } ${className}`}
    >
      {/* Top Action Bar */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-white/[0.06] bg-white/[0.015]">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-amber-400/10 text-amber-400">
            <FileCode className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-semibold text-white/90">
              {currentArtifact.title}
            </div>
            <div className="text-[10px] font-mono text-white/40">
              {currentArtifact.language?.toUpperCase() || currentArtifact.type.toUpperCase()} · {currentArtifact.timestamp}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1.5">
          {/* Code / Preview Switcher */}
          {currentArtifact.type === "code" || currentArtifact.type === "svg" ? (
            <div className="flex items-center bg-white/[0.04] p-0.5 rounded-lg border border-white/[0.06] mr-2">
              <button
                onClick={() => setActiveTab("code")}
                className={`px-2.5 py-1 text-[11px] font-medium rounded-md transition-colors ${
                  activeTab === "code"
                    ? "bg-white/[0.1] text-white"
                    : "text-white/40 hover:text-white/80"
                }`}
              >
                Source
              </button>
              <button
                onClick={() => setActiveTab("preview")}
                className={`px-2.5 py-1 text-[11px] font-medium rounded-md transition-colors ${
                  activeTab === "preview"
                    ? "bg-white/[0.1] text-white"
                    : "text-white/40 hover:text-white/80"
                }`}
              >
                Preview
              </button>
            </div>
          ) : null}

          {/* Copy Button */}
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] text-white/70 hover:text-white text-xs font-mono transition-colors cursor-pointer"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-emerald-400">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy</span>
              </>
            )}
          </button>

          {/* Fullscreen Expand */}
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 rounded-lg text-white/40 hover:text-white hover:bg-white/[0.06] transition-colors cursor-pointer"
          >
            {isExpanded ? (
              <Minimize2 className="w-4 h-4" />
            ) : (
              <Maximize2 className="w-4 h-4" />
            )}
          </button>

          {/* Close */}
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-white/40 hover:text-white hover:bg-white/[0.06] transition-colors cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-auto p-5 font-mono text-xs bg-black/40">
        {activeTab === "code" ? (
          <pre className="text-amber-100/90 leading-relaxed selection:bg-amber-400/20">
            <code>{currentArtifact.content}</code>
          </pre>
        ) : (
          <div className="h-full flex items-center justify-center p-8 bg-white/[0.01] rounded-2xl border border-white/[0.04] text-white/40 text-xs">
            <span>Live Interactive Preview Rendered on GPU</span>
          </div>
        )}
      </div>

      {/* Bottom telemetry line */}
      <div className="px-5 py-2 border-t border-white/[0.06] bg-white/[0.01] flex items-center justify-between text-[10px] font-mono text-white/40">
        <span>Artifact ID: {currentArtifact.id}</span>
        <span className="flex items-center gap-1.5 text-emerald-400/80">
          <Sparkles className="w-3 h-3" /> Ready to deploy or export
        </span>
      </div>
    </motion.div>
  );
};
