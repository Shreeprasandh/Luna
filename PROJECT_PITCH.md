# 🌙 Luna — Personal Autonomous AI Assistant

> **Zero-Token-Waste, Local-First, Autonomous AI Assistant with Long-Term Vector Memory & Native Tool Execution.**

---

## 🚀 Executive Summary

Luna is a personal autonomous AI assistant designed for seamless daily productivity. Unlike traditional chatbots that forget context between sessions, Luna continuously learns your preferences, schedule, and habits, storing durable semantic memories in a Supabase vector database (`pgvector`) using zero-cost local CPU embeddings (`all-MiniLM-L6-v2`).

Luna communicates via text or voice (24/7 background desktop daemon), executes multi-step tools (web search, browser scraping, local files, code execution, Gmail, Google Calendar, and multimodal screen vision), and renders a responsive sidepanel desktop interface supporting **7 curated minimal themes**.

---

## 🌟 Key Features

1. **Zero-Token-Waste Architecture**
   - 100% local CPU embeddings (`sentence-transformers/all-MiniLM-L6-v2`) for $0.00 vector retrieval.
   - Intelligent three-tier LLM fallback: **Groq** (primary speed) → **Gemini** (fallback) → **Ollama** (offline local).

2. **Long-Term Vector Memory & Auto-Learning**
   - Post-session summarisation automatically distils facts, preferences, patterns, and corrections into Supabase `pgvector`.
   - Semantic retrieval with cosine similarity surfaces contextually relevant memories before every turn.

3. **14 Native Tool Capabilities**
   - **Web & Image Search:** Free DuckDuckGo search + direct image payload rendering.
   - **Browser Automation:** Headless Playwright Chromium scraper + page screenshots.
   - **Isolated Code Execution:** Sandboxed Python interpreter with execution metrics.
   - **Multi-Account OAuth:** Gmail & Google Calendar integration supporting Work, Personal, and Luna Dedicated accounts.
   - **Desktop Vision:** Monitor display capture (`mss`) + Gemini Multimodal Vision analysis.

4. **24/7 Desktop Voice Assistant Daemon**
   - Local OpenWakeWord detector (0% idle CPU) + Whisper Speech-to-Text + offline `pyttsx3` Speech Synthesis.

5. **7 Curated Minimalist Aesthetic Themes**
   - Obsidian Slate, Warm Parchment, Nordic Fog, Kyoto Moss, Espresso Wood, Midnight Indigo, Sandstone Dune.

---

## 🛡️ Safety & Control Switches

- **Local Boot Switch:** `python boot_luna.py`
- **Local Process Kill Switch:** `python kill_luna.py`
- **Cloud Run Control:** `backend/boot_cloud.sh` / `backend/kill_cloud.sh`
