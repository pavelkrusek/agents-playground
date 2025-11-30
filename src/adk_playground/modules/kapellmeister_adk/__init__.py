from adk_playground.modules.kapellmeister_adk.agents import explainer, explainer_wikidata

REGISTRY = {
    "k001_explainer": explainer.build_agent,  # Simple explainer
    "k002_explainer_mcp": explainer_wikidata.build_agent,  # Simple explainer with MCP
}
