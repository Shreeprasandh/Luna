# 🎬 Luna Hackathon Demo & Verification Guide

Follow this guide to demonstrate and test Luna's capabilities end-to-end.

---

## ⚡ Quick Start (Local Setup)

### 1. Boot System
Run the one-command boot switch:
```bash
python boot_luna.py
```
This automatically initializes:
- FastAPI Backend API (`http://localhost:8000`)
- Next.js Desktop Panel (`http://localhost:3000`)
- Desktop Voice Assistant Daemon

---

## 🧪 Verification Walkthrough

### Test 1: Health & Metrics Endpoint
Visit `http://localhost:8000/metrics` or run:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/metrics" -Method Get
```
*Expected Output:* Status `healthy`, Zero-Token-Waste cost `$0.00`, active memories count, and LLM status.

---

### Test 2: Long-Term Memory & Recall
1. Open the panel UI or send a request:
   *"My name is Shree. I prefer Python with type hints and work late at night."*
2. End the session (triggers background summariser).
3. Start a fresh session and ask: *"What do you know about me?"*
4. *Expected Output:* Luna recalls your name, preferred language, work schedule, and coding style automatically.

---

### Test 3: Tool Execution (Web & Image Search)
1. Ask: *"Search the web for news on SpaceX Starship."*
2. Ask: *"Show me an image of a mango fruit."*
3. *Expected Output:* Luna invokes DuckDuckGo search tools and renders text summaries and visual image cards in the sidepanel.

---

### Test 4: Code Generation & Execution
1. Ask: *"Execute a Python script to calculate the first 10 Fibonacci numbers."*
2. *Expected Output:* Luna generates the Python code, executes it in the sandboxed evaluator, and returns the output (`[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`).

---

### Test 5: Process Kill Switch
Run:
```bash
python kill_luna.py
```
*Expected Output:* Safely terminates backend server and voice daemon, releasing port 8000.
