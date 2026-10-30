"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { 
  Sliders, 
  Terminal, 
  Search, 
  ToggleLeft, 
  ToggleRight, 
  CheckCircle, 
  Wrench, 
  Zap, 
  Layers, 
  Sparkles,
  Shield,
  Code2,
  Volume2,
  Cpu
} from "lucide-react";

export interface SkillItem {
  name: string;
  category: "engineering" | "voice_3d" | "security_audit" | "research" | "os_actuation";
  description: string;
  active: boolean;
  model: string;
}

const mockSkills: SkillItem[] = [
  {
    name: "the-seven-shadows",
    category: "security_audit",
    description: "Automated auditing squad and full-spectrum security defense grid across 7 sentinels.",
    active: true,
    model: "Groq Llama 3.3",
  },
  {
    name: "the-alchemists",
    category: "research",
    description: "Pinnacle 10-member research, reconnaissance and data transmutation team.",
    active: true,
    model: "DeepSeek R1",
  },
  {
    name: "the-elders",
    category: "security_audit",
    description: "System One calibrated semantic judgment substrate for sub-80ms typed decisions.",
    active: true,
    model: "Llama 3.2 3B",
  },
  {
    name: "api-sentinel",
    category: "engineering",
    description: "Production REST, Route Handler, and Streaming Architecture Engine for Next.js 16.",
    active: true,
    model: "Qwen 2.5 Coder",
  },
  {
    name: "voice-synth",
    category: "voice_3d",
    description: "Local Offline Voice Synthesis, TTS, and Audio Narration Engine on Apple Silicon.",
    active: true,
    model: "Silero / Whisper",
  },
  {
    name: "webgpu-threejs",
    category: "voice_3d",
    description: "Interactive Web 3D, WebGPU, and Three.js shader pipeline engine.",
    active: true,
    model: "Three.js Metal",
  },
  {
    name: "git-sentinel",
    category: "engineering",
    description: "Conventional Commits, Merge Conflict Resolution, and Release Engineering Sentinel.",
    active: true,
    model: "Local Core",
  },
  {
    name: "cli-anything",
    category: "os_actuation",
    description: "Agent-Native Command Line Harness Generator for GUI software and system utilities.",
    active: true,
    model: "Local Core",
  },
  {
    name: "total-typescript",
    category: "engineering",
    description: "Senior type-level engineering, strict type safety, and zero-any sentinel.",
    active: true,
    model: "Qwen 2.5 Coder",
  },
  {
    name: "audio-whisper",
    category: "voice_3d",
    description: "Local Speech-to-Text Transcription and Audio Telemetry Engine.",
    active: true,
    model: "Whisper tiny.en",
  },
  {
    name: "freedom",
    category: "security_audit",
    description: "Policy-gated autonomous execution controller with System One safety checks.",
    active: true,
    model: "The Elders",
  },
  {
    name: "coffee",
    category: "os_actuation",
    description: "Keep-awake controller for macOS preventing screen timeout and remote drops.",
    active: true,
    model: "macOS Caffeinate",
  },
];

interface SkillMatrixProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

export const SkillMatrix: React.FC<SkillMatrixProps> = ({
  isOpen,
  onClose,
  className = "",
}) => {
  const [skills, setSkills] = useState<SkillItem[]>(mockSkills);
  const [activeCategory, setActiveCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Persona Tuning Dials
  const [witLevel, setWitLevel] = useState(30);
  const [brevityLevel, setBrevityLevel] = useState(85);
  const [rigorLevel, setRigorLevel] = useState(95);

  const toggleSkill = (name: string) => {
    setSkills(prev =>
      prev.map(s => (s.name === name ? { ...s, active: !s.active } : s))
    );
  };

  const filteredSkills = skills.filter(s => {
    const matchesCategory = activeCategory === "all" || s.category === activeCategory;
    const matchesSearch =
      s.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const getCategoryIcon = (cat: SkillItem["category"]) => {
    switch (cat) {
      case "engineering":
        return <Code2 className="w-3.5 h-3.5 text-sky-400" />;
      case "voice_3d":
        return <Volume2 className="w-3.5 h-3.5 text-purple-400" />;
      case "security_audit":
        return <Shield className="w-3.5 h-3.5 text-emerald-400" />;
      case "research":
        return <Sparkles className="w-3.5 h-3.5 text-amber-400" />;
      case "os_actuation":
        return <Cpu className="w-3.5 h-3.5 text-rose-400" />;
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md">
      <motion.div
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96, y: 12 }}
        transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
        className={`w-full max-w-5xl h-[86vh] flex flex-col bg-[#0B0D11] border border-white/[0.08] rounded-3xl shadow-2xl overflow-hidden ${className}`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/[0.06] bg-white/[0.015]">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-8 h-8 rounded-xl bg-purple-500/[0.08] border border-purple-500/20 text-purple-400">
              <Sliders className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-white tracking-wide flex items-center gap-2">
                156-Skill Matrix & Persona Tuning Studio
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-purple-400/10 text-purple-400 border border-purple-400/20">
                  {skills.filter(s => s.active).length} Active
                </span>
              </h2>
              <p className="text-xs text-white/40">
                Configure Luna&apos;s active neural skills, cognitive balance, and behavioral traits
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded-lg text-xs font-mono text-white/50 hover:text-white bg-white/[0.04] hover:bg-white/[0.08] transition-colors cursor-pointer"
          >
            Esc to close
          </button>
        </div>

        {/* Persona Tuning Dials Strip */}
        <div className="px-6 py-4 bg-white/[0.01] border-b border-white/[0.04] grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Dial 1: Brevity */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <span className="font-medium text-white/80">Executive Brevity</span>
              <span className="font-mono text-amber-400">{brevityLevel}%</span>
            </div>
            <input
              type="range"
              min="10"
              max="100"
              value={brevityLevel}
              onChange={e => setBrevityLevel(Number(e.target.value))}
              className="w-full accent-amber-400 bg-white/10 rounded-lg h-1.5 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] font-mono text-white/30">
              <span>Deeply Detailed</span>
              <span>Surgical & Direct</span>
            </div>
          </div>

          {/* Dial 2: Quiet Wit */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <span className="font-medium text-white/80">Quiet Wit & Poise</span>
              <span className="font-mono text-purple-400">{witLevel}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              value={witLevel}
              onChange={e => setWitLevel(Number(e.target.value))}
              className="w-full accent-purple-400 bg-white/10 rounded-lg h-1.5 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] font-mono text-white/30">
              <span>Strictly Stoic</span>
              <span>Subtle Wit</span>
            </div>
          </div>

          {/* Dial 3: Analytical Rigor */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs">
              <span className="font-medium text-white/80">Analytical Rigor</span>
              <span className="font-mono text-emerald-400">{rigorLevel}%</span>
            </div>
            <input
              type="range"
              min="50"
              max="100"
              value={rigorLevel}
              onChange={e => setRigorLevel(Number(e.target.value))}
              className="w-full accent-emerald-400 bg-white/10 rounded-lg h-1.5 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] font-mono text-white/30">
              <span>Standard</span>
              <span>Gold-Standard Strict</span>
            </div>
          </div>
        </div>

        {/* Filter Strip */}
        <div className="flex items-center justify-between gap-4 px-6 py-3 border-b border-white/[0.04] bg-white/[0.005]">
          <div className="flex items-center gap-1.5 bg-white/[0.03] p-1 rounded-xl border border-white/[0.05]">
            {(["all", "engineering", "voice_3d", "security_audit", "research", "os_actuation"] as const).map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                  activeCategory === cat
                    ? "bg-purple-500/15 text-purple-300 shadow-sm"
                    : "text-white/40 hover:text-white/80"
                }`}
              >
                {cat === "all" ? "All Skills" : cat.replace("_", " ").toUpperCase()}
              </button>
            ))}
          </div>

          <div className="relative flex-1 max-w-xs">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/40" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search skill matrix..."
              className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/[0.06] text-xs text-white placeholder-white/30 focus:outline-none focus:border-purple-400/40 transition-colors"
            />
          </div>
        </div>

        {/* Skills Grid */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {filteredSkills.map(skill => (
            <div
              key={skill.name}
              className={`p-3.5 rounded-2xl border transition-all flex flex-col justify-between ${
                skill.active
                  ? "bg-white/[0.02] border-white/[0.07] hover:border-white/[0.14]"
                  : "bg-white/[0.005] border-white/[0.03] opacity-50"
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <div className="p-1 rounded-md bg-white/[0.04]">
                      {getCategoryIcon(skill.category)}
                    </div>
                    <span className="text-xs font-semibold text-white/90">
                      {skill.name}
                    </span>
                  </div>
                  <button
                    onClick={() => toggleSkill(skill.name)}
                    className="cursor-pointer text-white/50 hover:text-white transition-colors"
                  >
                    {skill.active ? (
                      <ToggleRight className="w-5 h-5 text-emerald-400" />
                    ) : (
                      <ToggleLeft className="w-5 h-5 text-white/30" />
                    )}
                  </button>
                </div>
                <p className="text-[11px] leading-relaxed text-white/60 mb-3">
                  {skill.description}
                </p>
              </div>

              <div className="flex items-center justify-between text-[10px] font-mono text-white/40 pt-2 border-t border-white/[0.04]">
                <span>{skill.category.toUpperCase()}</span>
                <span className="text-white/60">{skill.model}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-2.5 border-t border-white/[0.06] bg-white/[0.01] flex items-center justify-between text-xs font-mono text-white/40">
          <span>Source: ~/.gemini/antigravity-cli & ~/.agents/skills/</span>
          <span>Changes synchronized directly to active runtime</span>
        </div>
      </motion.div>
    </div>
  );
};
