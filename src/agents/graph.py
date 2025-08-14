from langgraph.graph import START, END, StateGraph

from src.agents.tools.suzy_tool import answer_suzy
from src.memory.st_memory import get_short_term_memory_node
from src.utils.states import GlobalState
from src.agents.tools.emotion_classifier import classification_emotion_tool


class SuzyAIPet:
    def __init__(self) -> None:
        self.graph = self.build_graph()

    def build_graph(self):
        agent = StateGraph(GlobalState)

        agent.add_node("MEMORY", get_short_term_memory_node)
        agent.add_node("CLASSIFIER", classification_emotion_tool)
        agent.add_node("SUZY", answer_suzy)

        agent.add_edge(START, "MEMORY")
        agent.add_edge("MEMORY", "CLASSIFIER")
        agent.add_edge("CLASSIFIER", "SUZY")
        agent.add_edge("SUZY", END)

        return agent.compile()


SuzyAI = SuzyAIPet()


