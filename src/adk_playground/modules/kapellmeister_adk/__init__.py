from adk_playground.modules.kapellmeister_adk.agents import explainer

REGISTRY = {
    "k001_explainer": explainer.build_agent,  # Simple explainer
}
