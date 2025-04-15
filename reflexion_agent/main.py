from dotenv import load_dotenv
from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import START, END, MessageGraph

from chains import revisor, first_responder
from tool_executor import execute_tools

load_dotenv()


MAX_ITERATIONS = 2
builder = MessageGraph()

# aggiungiamo il nodo al nostro grafo
builder.add_node("draft", first_responder)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor)

# una volta crearti i nodi dobbiamo creare gli archi
# arco che collega il primo nodo che produce la bozza e il nodo che esegue il tool
builder.add_edge(start_key="draft", end_key="execute_tools")

# arco che collega l'uscita dal tool e il nodo di revisione
builder.add_edge(start_key="execute_tools", end_key="revise")


# creiamo la funzione che fa il loop
# che si esegue dopo il nodo revisor
# dove ci troviamo in un bivio:
# 1. o Abbiamo la risposta finale
# 2. o eseguiamo un'altra iterazione di esecuzione del tool e del nodo revisione
def event_loop(state: List[BaseMessage]) -> str:
    # contiamo le chiamate al nodo che esegue il tool per vedere quante volte è stato fatto il loop
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations > MAX_ITERATIONS:
        return END  # nodo finale
    return "execute_tools"


# arco tra nodo revise e la funzione event loop nel caso ci siano state al massimo due iterazioni
builder.add_conditional_edges("revise", event_loop)

# settiamo il nodo iniziale
builder.set_entry_point("draft")

# otteniamo il grafo eseguibile
graph = builder.compile()

print(graph.get_graph().draw_ascii())

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    print("Hello Reflexion Agent!")

    res = graph.invoke(
        "Write about AI-Powered SOC / autonomous soc problem domain, list startups that do that nad raised capital."
    )

    print(res)



