.PHONY: tree

tree:
	@command -v tree >/dev/null 2>&1 && tree -a -I '.git|.venv|__pycache__|*.pyc|.idea' . || echo "Install 'tree' to view project tree."