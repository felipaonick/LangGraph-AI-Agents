"""
In produzione dell'applicazione, ci piacerebbe avere la capacità di eseguire task in maniera
asincrona, o avere la capacità di eseguire le cose in parallelo per risparmiare tempo.
Così possiamo restituire una risposta più rapida all'utente.
Per fortuna con langgraph, è molto semplice da fare.
Non necessitiamo di pacchetti come asyncio o multithreading, perché langgraph va a gestire il tutto.
Tutto quello che necessitiamo fare è definire i nostri nodi e archi in un certo modo.

Langgraph può dedurre se si tratta di un flusso asincrono e gestirà il tutto per noi

Vediamo come eseguire i nodi in parallelo
"""
from dotenv import load_dotenv
load_dotenv()

import operator
from typing import Annotated, Any

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    # lo stato sarà una lista di stringhe che vogliamo appendere dopo
    # ogni esecuzione di un nodo
    # l'esecuzione di ciascun nodo è semplice
    # vogliamo solo che ciascun nodo stampi il suo nome all'eseguirsi
    aggregate: Annotated[list, operator.add]


class ReturnNodeValue:

    def __init__(self, node_secret: str):
        self._value = node_secret  # private attribute


    # quando aggiungiamo un nodo al nostro grafo, necessitiamo scrivere
    # una funzione che riceva lo stato come un argomento e aggiorni lo stato

    # il metodo __call__ permette ad una istanza della classe di essere chiamata com una funzione
    def __call__(self, state: State):
        import time
        time.sleep(2) # per vedere come i nodi B e C vengono eseguiti assieme in parallelo
        print(f"Adding {self._value} to {state['aggregate']}")
        return {"aggregate": [self._value]} # aggiunge il _value alla lista

# creaimo il nostro grafo
# con questo grafo vogliamo mostrare come i nodi B e C possono essere eseguiti in parallelo
builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_edge(START, "a")
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "d")
builder.add_edge("c", "d")
builder.add_edge("d", END)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="async.png")

if __name__ == "__main__":

    graph.invoke(input={"aggregate": []}, config={"configurable": {"thread_id": "foo"}})

