# ⚡ DevOps Incident Resolver Agent

An autonomous multi-agent AI system that analyzes server error logs, researches fixes, and automatically creates GitHub Issues — all without human intervention.

---

## 🎯 Problem Statement

When a server crashes, developers spend 45–90 minutes manually reading logs, Googling fixes, and filing reports. Every minute of downtime costs real money and user trust.

**Our agent does this entire process in under 2 minutes. Automatically.**

---

## 🤖 How It Works

Error Log → Manager Agent → Log Analyzer Agent → Web Search Agent → Self Correction → GitHub Issue

Three specialized AI agents work together:

- **Log Analyzer Agent** — Reads the error log, identifies the most critical error, assigns severity (Critical/High/Low) and responsible team (Backend/DevOps/Database)
- **Web Search Agent** — Searches the internet in real time for validated fixes
- **Manager Agent** — Orchestrates both agents, ranks solutions, and self-corrects if confidence is low

---

## ✨ Key Features

- 🔍 **Autonomous Log Analysis** — Detects root cause from raw error logs
- 🌐 **Live Web Search** — Finds real fixes from documentation and forums
- 🔁 **Self-Correction** — Automatically retries with a smarter query if confidence is low
- 📝 **Auto GitHub Issues** — Creates detailed issues with fix, severity, and team assignment
- ⚡ **Under 2 Minutes** — What takes a developer 45–90 minutes, done instantly
- 🎨 **Beautiful UI** — Clean Streamlit dashboard with live agent status

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **CrewAI** | Multi-agent orchestration |
| **Groq** | Fast LLM inference (Llama 3.3 70B) |
| **Tavily** | Real-time web search |
| **PyGithub** | Automatic GitHub Issue creation |
| **Streamlit** | Frontend UI |
| **Python** | Core language |

---

## 📁 Project Structure

devops-incident-resolver/
│
├── agents/
│   ├── log_analyzer.py      # Analyzes error logs
│   ├── web_search.py        # Searches for fixes
│   └── manager.py           # Orchestrates all agents
│
├── tools/
│   ├── github_tool.py       # Creates GitHub Issues
│   └── search_tool.py       # Tavily web search
│
├── sample_logs/
│   └── error.log            # Sample error log for demo
│
├── app.py                   # Streamlit UI
├── main.py                  # Terminal entry point
├── requirements.txt         # Dependencies
└── README.md
