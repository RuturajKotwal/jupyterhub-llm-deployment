# JupyterHub LLM Deployment

This project helps you run a local LLM stack on JupyterHub and connect it to useful developer workflows.

## Overview

- Run a local chat UI on your machine with Open WebUI.
- Use coding assistance in VS Code with Continue.
- Explore local RAG over your own documents.
- Compare local and hosted model quality side by side.
- Reduce setup friction with a small helper script.

## Initial setup

Add your local binaries to `PATH`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Set the required environment values:

```bash
export JUPYTERHUB_API_TOKEN="jupyterhub_api_token_here"
export OLLAMA_BASE_URL="ollama_base_url_here"
```

## Start Ollama in tmux

```bash
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_KEEP_ALIVE=24h
ollama serve
```

If you are managing it in a tmux session, keep the session name consistent and use it for debugging later.

## Troubleshooting

| Issue | Fix |
| --- | --- |
| `ollama: command not found` | Run `ls ~/.local/bin/ollama` and confirm the binary path. If it lives elsewhere, update the PATH export in your shell config. |
| `tmux: command not found` | Install it with `conda install -c conda-forge tmux`, or ask your admin if it is already available in the environment. |
| `did not respond within 30s` | Attach to the running tmux session with `tmux attach -t ollama`, or inspect `~/ollama.log` for the underlying error. |
| Model not found on preload | Pull the model first with `ollama pull llama3.1:8b`, or start the service with a different model such as `start_ollama.sh qwen2.5:14b`. |
| Port already in use | Stop the old Ollama instance with `pkill ollama`, then restart the service. |
| `start_ollama.sh: command not found` | Reload your shell config with `source ~/.bashrc`. |

## Recommended project ideas

- Use Open WebUI as a chat interface pointed at your cluster model.
- Pair Continue in VS Code with a stronger local coding model such as `qwen2.5-coder:14b` if your GPU has enough VRAM.
- Build a small local RAG pipeline using `nomic-embed-text` with LangChain or LlamaIndex.
- Run the same 20-30 prompts against `llama3.1:8b` and a paid API so you can compare quality and decide whether a larger model is worth the cost.
- Add a small PowerShell helper that sets `$HUB` and your token so each new terminal window does not need manual setup.
