import importlib
import pkgutil
from typing import Callable

import typer

app = typer.Typer(help="ADK Playground")

_DISCOVERED: dict[str, Callable[[], object]] = {}
base_pkg = "adk_playground.modules"
pkg = importlib.import_module(base_pkg)
for m in pkgutil.iter_modules(pkg.__path__):
    mod = importlib.import_module(f"{base_pkg}.{m.name}")
    reg = getattr(mod, "REGISTRY", {})
    for cmd, fn in reg.items():
        _DISCOVERED[cmd] = fn
        _register(cmd, fn)

if __name__ == "__main__":
    app()
