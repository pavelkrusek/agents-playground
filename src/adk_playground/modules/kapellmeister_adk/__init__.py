from adk_playground.modules.kapellmeister_adk.agents import explainer, explainer_wikidata, explainer_wikipedia, \
    parallel_explainer

REGISTRY = {
    "k001_explainer": explainer.build_agent,  # Simple explainer
    "k002_explainer_mcp": explainer_wikidata.build_agent,  # Simple explainer with MCP - Wikidata
    "k003_explainer_mcp": explainer_wikipedia.build_agent,  # Simple explainer with MCP - Wikipedia
    "k004_parallel_pipeline": parallel_explainer.build_agent,  # Parallel explainer - Wikidata & Wikipedia
}
