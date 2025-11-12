from .runners import simple

REGISTRY = {
    "simple": simple.build_runner,
    # "blog-search": search.build_runner,
}
