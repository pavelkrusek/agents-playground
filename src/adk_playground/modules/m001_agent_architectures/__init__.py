from .agents import research_summarize_llm, research_summarize_seq, router_team, critic_loop, parallel_researchers, \
    prompt_to_action

REGISTRY = {
    "m001_01_prompt_to_action": prompt_to_action.build_agent,  # Simple prompt to action
    "m001_02_research_llm": research_summarize_llm.build_agent,  # LLM-orchestrated
    "m001_03_research_seq": research_summarize_seq.build_agent,  # Deterministic sequential
    "m001_04_router_team": router_team.build_agent,  # LLM-orchestrated with router
    "m001_05_parallel_researchers": parallel_researchers.build_agent,  # Researchers in parallel
    "m001_06_critic_loop": critic_loop.build_agent,  # LoopAgent with exit function
}
