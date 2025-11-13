# Agents Playground

A `Poetry`-based project for experimenting with AI agent frameworks and patterns.

## Google ADK Playground

A subproject that extends the official assignments from the Google “5-Day Agents” course and also serves as a
general `Google ADK playground`.

[Course reference](https://www.kaggle.com/learn-guide/5-day-agents)

> **Why run this locally (with `Poetry`) instead of only on `Kaggle` notebooks?**

- **Stability & speed:** No `Kaggle` timeouts or proxies; ADK web runs on `localhost`.
- **Quotas & costs:** Separate project/API key for clear visibility into course-only costs.
- **Secrets & security:** `.env` with key rotation; nothing persists in third-party environments.
- **Reproducibility:** `poetry.lock` version pinning; straightforward CI/CD.
- **Extensibility:** Integration of custom tools (HTTP, DB) and/or linkage to a `FastAPI` stack.
- **Local model experiments:** Support for applying the same agent patterns with `open-weight models` (`Meta Llama`/
  `Gemma`) via local
  runtimes (`llama.cpp`, `Ollama`, `Lemonade`, ...) and with `Hugging Face` models for classic NLP tasks (
  `classification`, `NER`, `summarization`, `embeddings/reranking`) using `transformers` / `sentence-transformers`;
  side-by-side comparisons with Gemini.

## Quick start

You’ll need **Python 3.12+** and **Poetry**—set it up the usual way (`poetry install`, etc.).

**Secrets:** the only required secret is `GEMINI_API_KEY`. An example file is provided:

```bash
cp -n .env.example .env
# then edit .env and set:
# GEMINI_API_KEY=your_key_here
```

## How to use

- Lesson content lives in `src/adk_playground/modules/`, adapted from the Kaggle notebooks.
- Register agents in each module’s `__init__.py` (e.g., `src/adk_playground/modules/<module_name>/__init__.py`).

## CLI tool

Project exposes two script entry points (primary `adkp` to avoid collision with Google ADK, alias `agents`):

```toml
[tool.poetry.scripts]
adkp = "adk_playground.cli:app"
agents = "adk_playground.cli:app"
```

Use either prefix: `poetry run adkp ...` or `poetry run agents ...`

### Commands

| Command        | Description                              | Example                                                     |
|----------------|------------------------------------------|-------------------------------------------------------------|
| `list`         | List discovered agent commands           | `poetry run adkp list`                                      |
| `sync-agents`  | (Re)generate agents for the ADK Web UI   | `poetry run adkp sync-agents --clean --target ./adk_agents` |
| `<agent-name>` | Run a discovered agent with a user query | `poetry run adkp <agent-name> "Your prompt here"`           |

## Running the Web UI

Run **after** `sync-agents`:

```bash
poetry run python -m google.adk.cli web --port 8001 ./adk_agents
```

## Makefile

Targets:

| Target    | Description                                | Notes                                                           |
|-----------|--------------------------------------------|-----------------------------------------------------------------|
| `list`    | List discovered CLI commands               | Runs `poetry run adkp list`.                                    |
| `sync`    | Generate shim agents for the ADK Web UI    | Writes to `AGENTS_DIR` (default `adk_agents`) with `--clean`.   |
| `web`     | Start ADK Web UI                           | Uses `$(ADK) web --host $(HOST) --port $(PORT) $(AGENTS_PATH)`. |
| `web-dev` | Composite: `sync` then `web`               | One-shot refresh + launch.                                      |
| `run`     | Run a discovered command with a user query | Usage: `make run CMD=<command> Q='<query>'`.                    |

**Usage examples**

```bash
make list
make sync
make web
make run CMD=m001_simple Q='What is ADK?'
```


