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