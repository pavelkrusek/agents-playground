from .agents import simple

REGISTRY = {
    "m001_simple": simple.build_agent,
}
