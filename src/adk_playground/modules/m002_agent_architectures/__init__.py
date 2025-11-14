from .agents import research_summarize_llm, research_summarize_seq, router_team, critic_loop

REGISTRY = {
    "m002_research_llm": research_summarize_llm.build_agent,  # LLM-orchestrated
    "m002_research_seq": research_summarize_seq.build_agent,  # Deterministic sequential
    "m002_router_team": router_team.build_agent,  # LLM-orchestrated with router
    "m002_critic_loop": critic_loop.build_agent,  # LoopAgent with exit function
}
