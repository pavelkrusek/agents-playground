from .agents import simple

REGISTRY = {
    "m001_01_simple": simple.build_agent,
}
