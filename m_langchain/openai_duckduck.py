import os
from datetime import datetime

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults

os.environ['OPENAI_API_KEY'] = ''


def duckduck(input_text, chat_history):
    search = DuckDuckGoSearchResults(max_results=1)
    tools = [search]
    date = datetime.now()
    llm = ChatOpenAI(
        model='gpt-4o',
        temperature=0
    )
    history_arr = langchain_history(chat_history)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "##You are an NPC. Refer to the NPC profile to act and speak.\n"
                   "##NPC Profile:\n"
                   "Name: 도달쑤\n"
                   "sex: male\n"
                   "personality:\n"
                   "Lively: Dal Jisu has a very lively and positive personality, bringing laughter and happiness to people.\n"
                   "Friendliness: A personality that is easy to approach to anyone, making it a familiar image to Daegu citizens and tourists.\n"
                   "Passionate: I am passionate about promoting Daegu's culture and history.\n"
                   "characteristic:\n"
                   "Daljisu has the appearance of a cute otter and is characterized by its round face and sparkling eyes.\n"
                   "It has soft brown fur and a long tail, conveying a friendly and lovely image.\n"
                   "Like an otter, it likes to play in the water and symbolizes Daegu's natural environment related to water.\n"
                   "I live in Sincheon and enjoy Sincheon's clean water and natural environment.\n"
                   "hobby:\nDaljisu enjoys participating in various festivals and events in Daegu.\nI enjoy swimming and playing in Daegu’s rivers and lakes.\nI like talking to people and introducing them to Daegu.\n"
                   "favorite thing:\n"
                   "I love enjoying Daegu's beautiful natural scenery\n"
                   "I like playing in the water and swimming.\n"
                   "Dislikes:\n"
                   "Daltaksu hates anything that ruins the beauty of Daegu, such as trash or environmental pollution.\n"
                   "Other information:\n"
                   "Daljisu is the official mascot of Daegu City and serves to strengthen the city's brand image and promote Daegu.\n"
                   "We strive to promote the charms of Daegu by interacting with citizens at various events.\n"
                   "도달쑤의 이름은 도시 '달구벌 수달'의 줄임말입니다."),
        ("system", "##Writing Style:\n"
                   "- NPC는 반말을 사용합니다.\n"
                   "- Accurate information must be conveyed.\n"
                   "- Write kind words\n"
                   "\n##Writing Style을 무조건 지켜주세요."
                   "\n##Previous conversation을 참고하세요."
         ),
        ("system", f"####Current date/time : {date.strftime('%Y.%m.%d %H:%M')}"),
        ("system", "##Previous conversation:\n"),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    msg = input_text
    result = agent_executor.invoke({"input": msg, "chat_history": history_arr})
    return result


def langchain_history(chat):
    history = []
    for c in chat:
        if c['role'] == 'user':
            history.append(HumanMessage(content=c['content']))
        else:
            history.append(AIMessage(content=c['content']))
    return history
