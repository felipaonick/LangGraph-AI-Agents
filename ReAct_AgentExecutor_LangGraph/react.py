from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent  # prende il prompt, llm, tool e restituisce un oggetto runnable
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI


react_prompt: PromptTemplate = hub.pull("hwchase17/react")


@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled -> multiplied by 3
    """

    return 3 * float(num)


tools = [TavilySearchResults(max_results=1), triple]


llm = ChatOpenAI(model="gpt-4o")

# è un oggetto runnable
# il che significa che possiamo eseguire il metodo .invoke() su di esso. ed otteniamo la risposta del modello
# inoltre prende il prompt react e popola i placeholder presenti nel prompt come: tool_names, e i tools che li forniamo
react_agent_runnable = create_react_agent(llm, tools, react_prompt)


