from pydantic import BaseModel, Field
from typing import Optional

class LongTermMemory(BaseModel):
    memory: str
    emotion: Optional[str] = Field(default="", description="Эмоция, связанная с воспоминанием")

class ShortTermMemory(BaseModel):
    memory: str

class GlobalState(BaseModel):
    user_id: str = Field(description="ID пользователя")
    query: str = Field(description="Запрос пользователя")
    answer: str = Field(description="Ответ от LLM")
    emotion: str = Field(description="Эмоция от пользователя")
    short_memory: Optional[ShortTermMemory] = Field(description="Краткосрочная память")
    long_memory: Optional[LongTermMemory] = Field(description="Долгосрочная память")

