from .agents import research_summarize_llm, research_summarize_seq, router_team, critic_loop, parallel_researchers

REGISTRY = {
    "m002_01_research_llm": research_summarize_llm.build_agent,  # LLM-orchestrated
    "m002_02_research_seq": research_summarize_seq.build_agent,  # Deterministic sequential
    "m002_03_router_team": router_team.build_agent,  # LLM-orchestrated with router
    "m002_04_parallel_researchers": parallel_researchers.build_agent,  # Researchers in parallel
    "m002_05_critic_loop": critic_loop.build_agent,  # LoopAgent with exit function
}
