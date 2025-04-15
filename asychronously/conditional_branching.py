"""
Tratteremo la ramificazione condizionale con la esecuzione asincrona in LangGraph
Iniziamo con il nodo A poi abbiamo tre conditional edges verso i nodi B, C e D.
Dipendendo dal nostro stato andiamo ad eseguire il nodo B e C o si va a eseguire i nodi C e D in parallelo.
Dopo aver fatto questo andiamo ad eseguire il nodo E.
"""
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, START, END
import operator


class State(TypedDict):
    aggregate: Annotated[list, operator.add]
    # aggiungiamo un attributo allo stato
    # che va a mantenere i nodi che vogliamo eseguire in uno step di ramificazione
    # quindi va a mantenere i nodi B e C oppure va a tenere i nodi C e D in base alla condizione
    # questo valore lo otteniamo dall'user quando invoca il grafo
    which: str


class ReturnNodeValue:

    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State):
        import time
        time.sleep(2)
        print(f"Adding {self._value} to {state['aggregate']}")
        return {"aggregate": [self._value]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_node("e", ReturnNodeValue("I'm E"))
builder.add_edge(START, "a")


# definiamo la funzione che decide verso quali nodi andare se verso B e C o se verso C e D
def route_bc_or_cd(state: State) -> Sequence[str]:
    if state['which'] == "cd":
        return ["c", "d"]
    return ["b", "c"]


# lista che contiene tutti i nodi possibili dal nodo A
intermediates = ["b", "c", "d"]


builder.add_conditional_edges(
    "a",
    route_bc_or_cd,
    # langgraph utilizza il path_map per disegnare il nostro grafo
    path_map=intermediates
)

for node in intermediates:
    builder.add_edge(node, "e")


builder.add_edge("e", END)

graph = builder.compile()


graph.get_graph().draw_mermaid_png(output_file_path="conditional_graph.png")


if __name__ == "__main__":

    graph.invoke({"aggregate": [], "which": "cd"}, {"configurable": {"thread_id": "foo"}})




