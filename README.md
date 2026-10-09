# JupyterHub LLM Deployment

Deploy, manage, and consume local Large Language Models (LLMs) hosted on a remote JupyterHub GPU instance using Ollama and OpenAI-compatible client interfaces.

---

## Architecture Overview

```text
┌─────────────────────────┐              HTTPS (Bearer Token)              ┌──────────────────────────────────────────────┐
│     Local Client        │ ─────────────────────────────────────────────► │             JupyterHub Server                │
│                         │                                                │                                              │
│ • Python Scripts / SDK  │                                                │  jupyter-server-proxy                        │
│ • VS Code (Continue)    │                                                │  (/user/<username>/proxy/11434/v1)           │
│ • Open WebUI / Chatbot  │                                                │                       │                      │
└─────────────────────────┘                                                │                       ▼                      │
                                                                           │  Ollama Daemon (tmux session: 'ollama')      │
                                                                           │  (0.0.0.0:11434, e.g. llama3.1:8b)           │
                                                                           └──────────────────────────────────────────────┘
```

This setup exposes an Ollama instance running inside a JupyterHub single-user container to your local machine via JupyterHub's built-in reverse proxy (`jupyter-server-proxy`). Authentication is enforced using standard JupyterHub API tokens.

---

## Getting Started

### 1. Server-Side Setup (JupyterHub Terminal)

Execute these steps within a JupyterLab/JupyterHub terminal session on the target GPU node.

#### Step 1.1: Ensure Binary Path Availability
Ensure local user binaries are available in your shell `PATH`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Step 1.2: Launch Ollama in a Persistent Session
Use `tmux` to ensure the Ollama server process persists even if your web terminal session disconnects:

```bash
# Start or attach to a dedicated tmux session
tmux new -s ollama
```

Inside the tmux session, configure environment variables and start the server:

```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_KEEP_ALIVE=24h
ollama serve
```

*To detach from the tmux session without stopping Ollama, press `Ctrl + B`, then release and press `D`.*

#### Step 1.3: Pull Desired Models
In another terminal session (or a new tmux window):

```bash
# Pull standard baseline model
ollama pull llama3.1:8b

# (Optional) Pull coding or embedding models
ollama pull qwen2.5-coder:14b
ollama pull nomic-embed-text
```

---

### 2. Client-Side Setup (Local Machine)

Configure your local development machine to communicate with the remote instance.

#### Step 2.1: Clone & Configure Environment
1. Clone this repository and create a Python virtual environment:

   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install openai python-dotenv
   ```

#### Step 2.2: Environment Variables
Create a `.env` file in the project root:

```env
JUPYTERHUB_API_TOKEN="your_jupyterhub_api_token_here"
OLLAMA_BASE_URL="https://<jupyterhub-domain>/user/<username>/proxy/11434/v1"
```

> **Note on `OLLAMA_BASE_URL`**: JupyterHub routes traffic to internal ports using the proxy format: `https://<JUPYTERHUB_HOST>/user/<USERNAME>/proxy/<PORT>/v1`. Ensure you include `/v1` at the end for OpenAI API compatibility.

---

## Verification & Usage

Run the verification scripts to test connectivity and streaming responses:

```bash
# Basic completion test
python test_llm.py

# Real-time streaming test
python test_stream.py
```

### Python Integration Example

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

token = os.getenv("JUPYTERHUB_API_TOKEN")
base_url = os.getenv("OLLAMA_BASE_URL")

client = OpenAI(
    base_url=base_url,
    api_key=token,
    default_headers={"Authorization": f"token {token}"},
    timeout=120.0,
)

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Explain KV cache in detail."}],
    stream=True,
)

for chunk in response:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
print()
```

---

## Troubleshooting

| Symptom / Error | Probable Cause | Recommended Resolution |
| :--- | :--- | :--- |
| `ollama: command not found` | Ollama binary is missing or not in `PATH`. | Verify binary location (`ls ~/.local/bin/ollama`). Ensure `~/.local/bin` is exported in `~/.bashrc`. |
| `tmux: command not found` | `tmux` package is not installed in the environment. | Install via Conda (`conda install -c conda-forge tmux`) or contact your cluster administrator. |
| Server did not respond / Timeout | Ollama daemon crashed or proxy is unreachable. | Attach to session (`tmux attach -t ollama`) to view live logs. Verify `OLLAMA_HOST=0.0.0.0:11434`. |
| HTTP 403 Forbidden | Missing or invalid JupyterHub API token. | Generate a fresh API token from your JupyterHub control panel (`File -> Hub Control Panel -> Token`). |
| HTTP 502 / 504 Bad Gateway | JupyterHub proxy cannot reach port 11434. | Confirm `ollama serve` is actively listening on `0.0.0.0:11434` (e.g., run `curl http://localhost:11434/api/tags` on the hub). |
| `model '...' not found` | The requested model has not been downloaded. | Run `ollama pull <model_name>` on the JupyterHub host before querying. |
| Port already in use | Stale Ollama daemon process is running. | Stop previous instances (`pkill ollama` or `kill $(pgrep ollama)`), then restart. |

---

## Recommended Integrations

- **Open WebUI**: Deploy Open WebUI locally and configure the backend URL to your JupyterHub proxy endpoint with token header authentication.
- **VS Code Continue Extension**: Point Continue's provider configuration to `OLLAMA_BASE_URL` with a dedicated coding model (`qwen2.5-coder:14b` or `deepseek-coder`).
- **Retrieval-Augmented Generation (RAG)**: Combine `nomic-embed-text` with LangChain / LlamaIndex and a local vector store (e.g., ChromaDB, FAISS).
- **Model Evaluation & Benchmarking**: Systematically evaluate latency, token throughput, and qualitative outputs across local models versus hosted commercial APIs.
