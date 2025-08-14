"""
    lt_memory:
        Долгосрочный память для Агентов.
        Ищет данные в векторных базах данных PGVECTOR
"""

import datetime
from langchain_community.vectorstores import PGVector
from langchain_together import TogetherEmbeddings

from src.db.create_db import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from src.utils.states import GlobalState, LongTermMemory

embeddings = TogetherEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

connection_string = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
vectorstore = PGVector(
    connection_string=connection_string,
    embedding=embeddings,
    table_name="lt_memory"
)


"""Сохраняет запрос и эмоцию в долгосрочную память"""
def save_to_lt_memory(state: GlobalState):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vectorstore.add_texts(
        texts=[state.query],
        ids=[f"{state.user_id}_{timestamp}"],
        metadatas=[{"user_id": state.user_id, "emotion": state.emotion, "timestamp": timestamp}]
    )




"""Извлекает записи из долгосрочной памяти"""
def get_lt_memory(state: GlobalState) -> GlobalState:
    """Извлекает записи из долгосрочной памяти"""
    results = vectorstore.similarity_search(state.query)
    memory_texts = []
    emotions = []

    for doc in results:
        memory_texts.append(doc.page_content)
        if doc.metadata and "emotion" in doc.metadata:
            emotions.append(doc.metadata["emotion"])

    state.long_memory = LongTermMemory(
        memory="\n".join(memory_texts),
        emotion="\n".join(emotions) if emotions else ""
    )
    return state



"""Удаляет все записи пользователя"""
def clear_lt_memory(state: GlobalState):
    vectorstore.delete(where={"user_id": state.user_id})
