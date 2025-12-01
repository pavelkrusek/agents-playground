# TL;DR

A modular Python/Poetry workspace for experimenting with AI agent frameworks (Google ADK), featuring a complete Capstone
multi-agent system (Kapellmeister) that merges Wikidata and Wikipedia via MCP servers to generate classical-music
explanations.

---

# Agents Playground

A Poetry-based project for experimenting with AI agent frameworks and patterns.

## Google ADK Playground

A subproject that extends the official assignments from the Google 5-Day Agents course and serves as a general-purpose
Google ADK playground.

### Course reference

[https://www.kaggle.com/learn-guide/5-day-agents](https://www.kaggle.com/learn-guide/5-day-agents)

### Why run this locally?

* Stability & speed — no Kaggle timeouts; local ADK Web UI
* Lower costs & full quota visibility
* `.env` secrets, reproducibility via `poetry.lock`
* Easy integration of custom tools
* Possibility to compare Gemini with local open-weight models

---

# Kapellmeister — ADK Multi-Agent Musicologist

Kapellmeister is a multi-agent system that explains classical composers and works by combining:

* **Structured facts via Wikidata MCP**
* **Narrative context via Wikipedia MCP**
* **A final aggregator agent** that produces a concert-program-style explanation

### Main Capstone agent

```
src/adk_playground/modules/kapellmeister_adk/agents/parallel_explainer.py
```

---

# MCP Integrations

This project uses **two forked MCP servers** (patched for stability):

* [**Wikidata MCP — forked & fixed**](https://github.com/pavelkrusek/mcp-wikidata)
* [**Wikipedia MCP — forked & fixed**](https://github.com/pavelkrusek/wikipedia-mcp)

Configured in:

```
src/adk_playground/config/mcp.yml
```

For both MCP forks (Wikidata and Wikipedia) I use a `uv`-based setup: install the server with `uv sync` and configure
the environment variable `WIKIDATA_USER_AGENT` in your `.env` file, for example:

`WIKIDATA_USER_AGENT=Kapellmeister-MCP/0.1 (https://github.com/pavelkrusek/agents-playground; mailto:pavel@krusek.dk)`

Using a proper, project-specific User-Agent like this prevents HTTP 403 responses from both Wikidata and Wikipedia APIs.


---

## Quick Start

You’ll need **Python 3.12+** and **Poetry**.

```bash
cp -n .env.example .env
# Edit .env and set:
# GEMINI_API_KEY=your_key_here
```

Additional required `.env` variables for MCP integration:

- `MCP_WIKIDATA_DIR=/abs/path/to/mcp-wikidata` — mandatory; directory containing the forked Wikidata MCP server
- `MCP_WIKIPEDIA_DIR=/abs/path/to/wikipedia-mcp` — mandatory; directory containing the forked Wikipedia MCP server

These paths are used by the ADK runtime to launch both MCP servers via stdio.

Install dependencies:

```bash
poetry install
```

---

## CLI Usage

Two entry points are exposed:

```toml
[tool.poetry.scripts]
adkp = "adk_playground.cli:app"
agents = "adk_playground.cli:app"
```

List commands:

```bash
poetry run adkp list
```

Run a specific agent:

```bash
poetry run adkp <agent> "Your query"
```

---

## Running the ADK Web UI

```bash
poetry run python -m google.adk.cli web --port 8001 ./adk_agents
```

---

## Makefile

Useful automation for development.

Targets:

| Target        | Description                                | Notes                                                                            |
|---------------|--------------------------------------------|----------------------------------------------------------------------------------|
| `list`        | List discovered CLI commands               | Runs `poetry run adkp list`.                                                     |
| `sync`        | Generate shim agents for the ADK Web UI    | Writes to `AGENTS_DIR` (default `adk_agents`) with `--clean`.                    |
| `web`         | Start ADK Web UI                           | Uses `$(ADK) web --host $(HOST) --port $(PORT) $(AGENTS_PATH)`.                  |
| `web-dev`     | Composite: `sync` then `web`               | One-shot refresh + launch.                                                       |
| `run`         | Run a discovered command with a user query | Usage: `make run CMD=<command> Q='<query>'`.                                     |
| `inspect-mcp` | Inspect and debug MCP setup                | Runs `poetry run python scripts/diagnose_mcp.py` against configured MCP servers. |

---

## Demo

Run the Kapellmeister agent:

```bash
make run CMD=k004_parallel_pipeline Q="Tell me about Hector Berlioz"
```

This triggers both MCP-backed researchers in parallel and returns a unified concert-program-style explanation.

A full demonstration is included in the repo's Capstone tag.

---

## Project Structure

```
src/
  adk_playground/
    modules/
      kapellmeister_adk/
        agents/
          parallel_explainer.py   # Main Capstone multi-agent pipeline
    config/
      mcp.yml                     # MCP server definitions
```

---

## Why This Submission Meets Requirements

| Requirement        | Implemented | Notes                                               |
|--------------------|-------------|-----------------------------------------------------|
| Multi-agent system | ✔           | Parallel + Sequential agents combined               |
| Parallel agents    | ✔           | Wikipedia + Wikidata run concurrently               |
| Sequential agents  | ✔           | Aggregator runs after parallel stage                |
| MCP tools          | ✔           | Two external MCP servers integrated                 |
| Sessions & State   | ✔           | ADK session state used to pass notes between agents |
| Observability      | ✔           | Full trace visible via ADK Web UI                   |

---

## Repository

**Capstone project repository:**
[https://github.com/pavelkrusek/agents-playground](https://github.com/pavelkrusek/agents-playground) (main branch, tag:
*Capstone submission*)
