# Project Roadmap & Backlog

This document outlines prioritized development milestones, workflow enhancements, and portfolio objectives for the JupyterHub LLM deployment stack.

---

## Phase 1: Automation & Developer Experience

- [ ] **[P1] PowerShell Environment Helper**: Create a cross-session helper script (`setup_env.ps1`) to automatically configure `$env:JUPYTERHUB_API_TOKEN` and `$env:OLLAMA_BASE_URL` without manually editing `.env`.
- [ ] **[P1] Hub Startup Script**: Add a companion shell script (`start_ollama.sh`) for the JupyterHub side to automate tmux session creation, environment exports (`OLLAMA_HOST`, `OLLAMA_KEEP_ALIVE`), and daemon health verification.
- [ ] **[P2] Clean Requirements Configuration**: Split dependencies into lightweight client requirements (`requirements.txt`) and development/notebook tooling (`requirements-dev.txt`).

---

## Phase 2: Client Integrations & Tooling

- [ ] **[P1] Open WebUI Integration**: Configure and test a local Open WebUI container pointing to the JupyterHub proxy endpoint with bearer token injection.
- [ ] **[P1] VS Code Continue Setup**: Configure `~/.continue/config.json` to route code-completion and chat requests to `qwen2.5-coder:14b` running on the hub instance.
- [ ] **[P2] Local Forwarding Proxy**: Build a lightweight local middleware proxy (e.g., FastAPI / mitmproxy) for client tools that do not support custom HTTP `Authorization` headers natively.

---

## Phase 3: RAG & Evaluation Pipeline

- [ ] **[P2] Document RAG Pipeline**: Build a reference Retrieval-Augmented Generation workflow using `nomic-embed-text` with LangChain / LlamaIndex and a local vector store (e.g., ChromaDB / FAISS).
- [ ] **[P2] Benchmark Suite**: Establish a standardized evaluation dataset (25–30 prompts covering reasoning, coding, summarization, and instruction following).
- [ ] **[P3] Performance & Cost Comparison**: Automate comparative benchmarking measuring token latency (TTFT, tokens/sec) and response quality between `llama3.1:8b` and commercial APIs (e.g., GPT-4o, Claude 3.5 Sonnet).

---

## Phase 4: Documentation & Portfolio Deliverables

- [ ] **[P2] Architecture & Demo Walkthrough**: Document the end-to-end setup with reproducible steps and terminal screencasts for technical portfolio presentations.
- [ ] **[P3] Model Selection Matrix**: Compile a VRAM-to-model guide tailored to the cluster GPU capacity (quantization levels, context length limits).

