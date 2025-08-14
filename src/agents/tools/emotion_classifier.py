"""
    emotion_classifier.py:
        Классифицирует текст и выдает настроение человека исходя из текста.
        Например если человек пишет так "Мне сегодня было тяжело....." - 
        То LLM выводят "sad".Так мы можем узнать его intent, так же будет легче отвечать ему исходя из его эмоции.
        Поддержать или наоборот играть..
    state: 
        Используем GlobalState чтобы было легче агенту.
        сохраняем на state.emotion чтобы и другие агенты пользовались этим
"""

from langchain_together import Together
from langchain_core.prompts import PromptTemplate

from src.utils.states import GlobalState
from src.utils.configs.settings import load_configs
from src.utils.prompts import classifier_prompt

configs = load_configs()

#llm configs, Оберну потом в configs.yml
llm = Together(
    model=configs["llms"]["classifier_emotion_llm"]["model"], 
    together_api_key=configs["llms"]["together_api_key"],
    max_tokens=configs["llms"]["classifier_emotion_llm"]["max_tokens"], #Мало токенов чтобы не выжирало и просто генерировала только одну слово
    temperature=configs["llms"]["classifier_emotion_llm"]["temperature"]
)

#Prompt 
prompt = PromptTemplate(
    input_variables=["query"],
    template=classifier_prompt
)

#Цепочка действие
chain = prompt | llm


#Сам тулз
def classification_emotion_tool(state: GlobalState) -> GlobalState:
    result = chain.invoke({"query": state.query})
    state.emotion = result.strip()  
    return state


