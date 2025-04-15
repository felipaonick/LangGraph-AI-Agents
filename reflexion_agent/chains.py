import datetime
import uuid

from dotenv import load_dotenv
from langgraph.prebuilt import ToolExecutor

load_dotenv()
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser, PydanticToolsParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from schemas import Reflection, AnswerQuestion, ReviseAnswer
from langchain_core.runnables import RunnableLambda


search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)
# vogliamo che le chiamate al tool tavily avvengano in parallelo non sicrone
# ToolExecutor ha un metodo batch che prende tutte le invocazioni del tool e le riunisce tutte
# il ToolExecutor con il metodo batch esegue semplicemente tutte le invocazioni al tool in parallelo
tool_executor = ToolExecutor([tavily_tool])

llm = ChatOpenAI(
    model="gpt-4o",
    # openai_api_key="ollama",
    # openai_api_base="http://localhost:11434/v1"
    )

parser = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])


def process_first_responder_output(first_responder_output):
    """Converte l'output di first_responder (AIMessage) in un AIMessage con tool_calls"""

    if not isinstance(first_responder_output, AIMessage):
        raise ValueError(f"Errore: output di first_responder non è AIMessage! Ricevuto: {type(first_responder_output)}")

    # ✅ Accedi correttamente ai dati
    answer = first_responder_output.tool_calls[0]['args']['answer']  # Il testo generato dall'LLM
    tool_calls = first_responder_output.tool_calls  # Lista di tool_calls generati

    # ✅ Controllo se tool_calls è una lista valida
    if not tool_calls or not isinstance(tool_calls, list):
        raise ValueError("Errore: tool_calls non è presente o non è una lista!")

    # ✅ Estrarre il primo tool_call
    tool_call = tool_calls[0]  # L'LLM dovrebbe generare solo un tool_call alla volta
    tool_args = tool_call.get("args", {})  # Ottieni gli argomenti passati al tool

    # ✅ Correggi il problema di `search_queries` dentro `reflection`
    reflection = tool_args.get("reflection", {})
    search_queries = tool_args.get("search_queries", [])  # reflection.pop("search_queries", [])  # 🔥 Estraggo `search_queries` se è stato messo dentro reflection

    # 🔥 Se `search_queries` non esiste ancora, assegna un valore predefinito
    if not isinstance(search_queries, list):
        search_queries = []

    # 🔥 Creiamo un AIMessage corretto con tool_calls
    ai_message = AIMessage(
        content=answer,
        tool_calls=[
            {
                "name": "AnswerQuestion",
                "args": {
                    "answer": answer,
                    "reflection": reflection,  # ✅ Ora senza `search_queries` dentro
                    "search_queries": search_queries  # ✅ Ora è sempre nella posizione giusta
                },
                "id": str(uuid.uuid4())  # Generiamo un nuovo ID
            }
        ]
    )
    return ai_message


# Creiamo un oggetto Runnable che può essere concatenato nella pipeline
process_first_responder_runnable = RunnableLambda(process_first_responder_output)


actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are expert researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer."""),
        MessagesPlaceholder(variable_name="messages")  # history
    ]
).partial(time=lambda: datetime.datetime.now().isoformat())


first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer."
)


first_responder = (first_responder_prompt_template
                   | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion") # vincola il modello ad usare sempre il tool)
                   # | parser_pydantic
                   | process_first_responder_runnable
                   )


revise_instructions = """Revise your answer using the new information.
- You should use the previous critique to add important to your answer.
    - You MUST include numerical citations in your revised answer to ensure it can be verified.
    - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
        - [1] https://example.com
        - [2] https://example.com
-You should use the previous critique to remove superfluous information from your answer and and make SURE it is more than 250 words.
"""

revisor = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")


if __name__ == "__main__":

    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous soc problem domain,"
        " list startups that do that and raised capital."
    )

    chain = (
        first_responder_prompt_template
        | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
        | parser_pydantic
    )

    response = chain.invoke(input={"messages": [human_message]})

    print(response)
