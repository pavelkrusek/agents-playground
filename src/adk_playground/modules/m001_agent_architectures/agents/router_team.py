from google.adk import Agent
from google.adk.tools import AgentTool

from adk_playground.core.settings import MODEL


# Pattern: Router + specialists (classification → call one tool), prompt-based
def build_agent() -> Agent:
    math_expert = Agent(
        name="math_expert",
        model=MODEL,
        description="Handles computations and math reasoning.",
        instruction="Solve the math task step-by-step and return the final numeric result.",
        output_key="final_output",
    )

    code_expert = Agent(
        name="code_expert",
        model=MODEL,
        description="Writes small, correct code snippets.",
        instruction=(
            "Write a minimal, correct code snippet. "
            "Include only the code block (no explanations)."
        ),
        output_key="final_output",
    )

    router = Agent(
        name="router",
        model=MODEL,
        description="Routes the query to the right expert.",
        instruction=(
            "If the user's query is primarily mathematics, call 'math_expert'. "
            "If it's about writing code, call 'code_expert'. "
            "Call exactly one tool and return its result."
        ),
        tools=[AgentTool(agent=math_expert), AgentTool(agent=code_expert)],
        output_key="final_output",
    )
    return router
