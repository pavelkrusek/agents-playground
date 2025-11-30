SHELL := /usr/bin/env bash

ADK  := poetry run python -m google.adk.cli
ADKP := poetry run adkp

AGENTS_DIR  ?= adk_agents
AGENTS_PATH := $(abspath $(AGENTS_DIR))
HOST        ?= 127.0.0.1
PORT        ?= 8001 # because 8000 is often occupied

.PHONY: tree list sync web web-dev run

tree:
	@command -v tree >/dev/null 2>&1 && tree -a -I '.git|.venv|__pycache__|*.pyc|.idea' . || echo "Install 'tree' to view project tree."

list: ## List discovered CLI commands
	$(ADKP) list

sync: ## Generate shim agents for ADK Web UI
	$(ADKP) sync-agents --target $(AGENTS_PATH) --clean

web: ## Start ADK Web UI
	ADK_APP_PACKAGE=$(AGENTS_DIR) \
	$(ADK) web --host $(HOST) --port $(PORT) $(AGENTS_PATH)

web-dev: ## Generate shims and start Web UI - composite
	$(MAKE) sync
	$(MAKE) web

run: ## Run a specific command with CLI (e.g., make run CMD=m001_simple Q='...')
	@if [ -z "$(CMD)" ] || [ -z "$(Q)" ]; then \
		echo "Usage: make run CMD=<command> Q='<query>'"; \
		exit 1; \
	fi
	$(ADKP) $(CMD) "$(Q)"
