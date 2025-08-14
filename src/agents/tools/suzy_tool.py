"""
    suzy_tool.py:
        Основной мозг Сюзи.
"""

from langchain_together import Together
from langchain_core.prompts import PromptTemplate

from src.utils.states import GlobalState
from src.utils.prompts import suzy_prompt
from src.utils.configs.settings import load_configs

config = load_configs()

llm = Together(
    model=config["llms"]["suzy"]["model"], 
    temperature=config["llms"]["suzy"]["temperature"],
    max_tokens=config["llms"]["suzy"]["max_tokens"],
    together_api_key=config["llms"]["together_api_key"]
)

prompt = PromptTemplate(
    input_variables=["emotion", "query", "context"],
    template=suzy_prompt
)

chain = prompt | llm

def answer_suzy(state: GlobalState) -> GlobalState:
    context = getattr(state.short_memory, "memory", "")
    result = chain.invoke({
        "query": state.query,
        "emotion": state.emotion,
        "context": context
    })
    state.answer = result.strip() if isinstance(result, str) else str(result)
    return state
