from langchain_core.memory import ConversationBufferMemory
from typing import Dict
from src.utils.states import GlobalState, ShortTermMemory


user_memories: Dict[str, ConversationBufferMemory] = {}

"""Получить или создать память пользователя"""
def get_memory(user_id: str) -> ConversationBufferMemory:
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
    return user_memories[user_id]

"""Вернуть историю чата в виде текста"""
def get_memory_content(user_id: str) -> str:
    memory = get_memory(user_id)
    messages = memory.load_memory_variables({}).get("chat_history", [])
    return "\n".join([m.content for m in messages])

"""Обновить short_memory в state"""
def update_short_memory(state: GlobalState) -> GlobalState:
    state.short_memory = ShortTermMemory(memory=get_memory_content(state.user_id))
    return state

"""Очистить short-term память"""
def clear_short_memory(state: GlobalState) -> GlobalState:
    if state.user_id in user_memories:
        user_memories[state.user_id].clear()
    state.short_memory = None
    return state

"""Получить short-term память"""
def get_short_term_memory_node(state: GlobalState) -> GlobalState:
    memory_text = get_memory_content(state.user_id) 
    state.short_memory = ShortTermMemory(memory=memory_text) 
    return state

