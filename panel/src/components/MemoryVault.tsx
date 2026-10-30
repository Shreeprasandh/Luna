"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Database, 
  Brain, 
  Search, 
  Plus, 
  Trash2, 
  Edit3, 
  Save, 
  Check, 
  Clock, 
  Sparkles,
  ShieldCheck,
  Tag
} from "lucide-react";

export interface MemoryItem {
  id: string;
  category: "core_ram" | "episodic" | "entity_graph";
  title: string;
  content: string;
  tags: string[];
  lastUpdated: string;
}

interface MemoryVaultProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

const mockMemories: MemoryItem[] = [
  {
    id: "mem-1",
    category: "core_ram",
    title: "Identity & Luna Protocol",
    content: "Persona: Personal AI assistant, Luna. Salutation: Sir. Tone: Grounded, professional, intelligent, respectful with subtle quiet wit. Strict Commit Rule: NEVER git commit without explicit instruction.",
    tags: ["core", "protocol", "identity"],
    lastUpdated: "Just now",
  },
  {
    id: "mem-2",
    category: "core_ram",
    title: "Architectural Directives",
    content: "Next.js 16.3 + React 19.2 Server Components by default. Async route params awaited. 8px spatial grid, Emil Kowalski out-expo motion physics. Zero generic AI slop.",
    tags: ["architecture", "nextjs", "physics"],
    lastUpdated: "Today",
  },
  {
    id: "mem-3",
    category: "episodic",
    title: "Project IdleBin Foundation",
    content: "Sir completed the initial commit and production digital twin initialization for IdleBin on October 30. Repository is clean on main branch.",
    tags: ["idlebin", "git", "milestone"],
    lastUpdated: "21:52",
  },
  {
    id: "mem-4",
    category: "entity_graph",
    title: "Sir's Hardware & Substrate",
    content: "Host Machine: Apple Silicon Mac (macOS). Local LLM server running on Ollama localhost:11434 with nomic-embed-text for 768-d cosine vector memory.",
    tags: ["hardware", "ollama", "apple-silicon"],
    lastUpdated: "22:15",
  },
];

export const MemoryVault: React.FC<MemoryVaultProps> = ({
  isOpen,
  onClose,
  className = "",
}) => {
  const [memories, setMemories] = useState<MemoryItem[]>(mockMemories);
  const [activeTab, setActiveTab] = useState<"all" | "core_ram" | "episodic" | "entity_graph">("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState("");
  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");
  const [isAdding, setIsAdding] = useState(false);

  const filteredMemories = memories.filter(m => {
    const matchesTab = activeTab === "all" || m.category === activeTab;
    const matchesSearch = 
      m.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesTab && matchesSearch;
  });

  const handleStartEdit = (item: MemoryItem) => {
    setEditingId(item.id);
    setEditContent(item.content);
  };

  const handleSaveEdit = (id: string) => {
    setMemories(prev =>
      prev.map(m =>
        m.id === id ? { ...m, content: editContent, lastUpdated: "Just now" } : m
      )
    );
    setEditingId(null);
  };

  const handleDelete = (id: string) => {
    setMemories(prev => prev.filter(m => m.id !== id));
  };

  const handleAddMemory = () => {
    if (!newTitle.trim() || !newContent.trim()) return;
    const newItem: MemoryItem = {
      id: `mem-${Date.now()}`,
      category: activeTab === "all" ? "episodic" : activeTab,
      title: newTitle.trim(),
      content: newContent.trim(),
      tags: ["custom", "live"],
      lastUpdated: "Just now",
    };
    setMemories([newItem, ...memories]);
    setNewTitle("");
    setNewContent("");
    setIsAdding(false);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md">
      <motion.div
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.96, y: 12 }}
        transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
        className={`w-full max-w-4xl h-[82vh] flex flex-col bg-[#0B0D11] border border-white/[0.08] rounded-3xl shadow-2xl overflow-hidden ${className}`}
      >
        {/* Header Bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/[0.06] bg-white/[0.015]">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-8 h-8 rounded-xl bg-amber-400/[0.08] border border-amber-400/20 text-amber-400">
              <Brain className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-white tracking-wide flex items-center gap-2">
                Cognitive Vault & Memory Matrix
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-400/10 text-emerald-400 border border-emerald-400/20">
                  Supabase pgvector Active
                </span>
              </h2>
              <p className="text-xs text-white/40">
                Explore, edit, and curate Luna&apos;s long-term memory and Core RAM blocks
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="px-3 py-1.5 rounded-lg text-xs font-mono text-white/50 hover:text-white bg-white/[0.04] hover:bg-white/[0.08] transition-colors"
          >
            Esc to close
          </button>
        </div>

        {/* Search & Filter Strip */}
        <div className="flex items-center justify-between gap-4 px-6 py-3 border-b border-white/[0.04] bg-white/[0.005]">
          {/* Tabs */}
          <div className="flex items-center gap-1.5 bg-white/[0.03] p-1 rounded-xl border border-white/[0.05]">
            {(["all", "core_ram", "episodic", "entity_graph"] as const).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                  activeTab === tab
                    ? "bg-amber-400/15 text-amber-300 shadow-sm"
                    : "text-white/40 hover:text-white/80"
                }`}
              >
                {tab === "all" ? "All Memories" : tab === "core_ram" ? "Core RAM" : tab === "episodic" ? "Episodic" : "Knowledge Graph"}
              </button>
            ))}
          </div>

          {/* Search Input */}
          <div className="relative flex-1 max-w-xs">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/40" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search cognitive memory..."
              className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/[0.06] text-xs text-white placeholder-white/30 focus:outline-none focus:border-amber-400/40 transition-colors"
            />
          </div>

          {/* Add New Memory Button */}
          <button
            onClick={() => setIsAdding(!isAdding)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-400/10 hover:bg-amber-400/20 text-amber-300 border border-amber-400/30 text-xs font-medium transition-colors cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Store Memory</span>
          </button>
        </div>

        {/* Add Memory Form Tray */}
        <AnimatePresence>
          {isAdding && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="px-6 py-4 bg-amber-500/[0.03] border-b border-amber-500/20"
            >
              <div className="space-y-2">
                <input
                  type="text"
                  value={newTitle}
                  onChange={e => setNewTitle(e.target.value)}
                  placeholder="Memory Title / Concept Anchor"
                  className="w-full px-3 py-1.5 rounded-lg bg-black/40 border border-white/10 text-xs text-white focus:outline-none focus:border-amber-400/50"
                />
                <textarea
                  rows={2}
                  value={newContent}
                  onChange={e => setNewContent(e.target.value)}
                  placeholder="Memory Content, facts, or instructions to remember..."
                  className="w-full px-3 py-1.5 rounded-lg bg-black/40 border border-white/10 text-xs text-white focus:outline-none focus:border-amber-400/50 resize-none"
                />
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => setIsAdding(false)}
                    className="px-3 py-1 text-xs text-white/50 hover:text-white"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleAddMemory}
                    className="px-4 py-1 rounded-lg bg-amber-400 text-black text-xs font-semibold hover:bg-amber-300 transition-colors"
                  >
                    Save to Vault
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Memory Grid */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredMemories.map(item => {
            const isEditing = editingId === item.id;

            return (
              <motion.div
                key={item.id}
                layout
                className="flex flex-col justify-between p-4 rounded-2xl bg-white/[0.02] border border-white/[0.06] hover:border-white/[0.12] transition-colors"
              >
                <div>
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${
                        item.category === "core_ram" ? "bg-purple-400" : item.category === "episodic" ? "bg-emerald-400" : "bg-sky-400"
                      }`} />
                      <span className="text-xs font-semibold text-white/90">
                        {item.title}
                      </span>
                    </div>
                    <span className="text-[10px] font-mono text-white/40">
                      {item.lastUpdated}
                    </span>
                  </div>

                  {isEditing ? (
                    <div className="space-y-2">
                      <textarea
                        value={editContent}
                        onChange={e => setEditContent(e.target.value)}
                        className="w-full p-2 text-xs bg-black/60 border border-amber-400/40 rounded-lg text-white focus:outline-none resize-none"
                        rows={4}
                      />
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => setEditingId(null)}
                          className="px-2 py-0.5 text-xs text-white/40 hover:text-white"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={() => handleSaveEdit(item.id)}
                          className="flex items-center gap-1 px-2.5 py-0.5 bg-amber-400 text-black rounded text-xs font-medium"
                        >
                          <Save className="w-3 h-3" /> Save
                        </button>
                      </div>
                    </div>
                  ) : (
                    <p className="text-xs leading-relaxed text-white/70">
                      {item.content}
                    </p>
                  )}
                </div>

                <div className="mt-4 pt-3 border-t border-white/[0.04] flex items-center justify-between">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    {item.tags.map(tag => (
                      <span
                        key={tag}
                        className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/[0.04] text-white/50"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center gap-1.5">
                    {!isEditing && (
                      <button
                        onClick={() => handleStartEdit(item)}
                        title="Edit Memory"
                        className="p-1.5 rounded-lg text-white/40 hover:text-white hover:bg-white/[0.06] transition-colors"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                      </button>
                    )}
                    <button
                      onClick={() => handleDelete(item.id)}
                      title="Prune Memory"
                      className="p-1.5 rounded-lg text-white/40 hover:text-rose-400 hover:bg-rose-400/[0.08] transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Footer info bar */}
        <div className="px-6 py-2.5 border-t border-white/[0.06] bg-white/[0.01] flex items-center justify-between text-xs font-mono text-white/40">
          <span>Vector Dimension: 768-d cosine index</span>
          <span>Indexed memories: {filteredMemories.length} entries</span>
        </div>
      </motion.div>
    </div>
  );
};
