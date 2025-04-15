"""
in questa sezione tratteremo anche le interruzioni e la gestione di una base
di dati per memorizzare gli stati del nostro grafo.

IL seguente grafo è un grafo semplice senza l'impiego di llms.
si inizia col nodo __start__ poi eseguiamo il nodo "step_1" che stampa
poi facciamo una interrupt prima di ottenere lo human_feedback
prendiamo gli human_feedback ed aggiorniamo il nostro stato con essi
poi continuiamo l'esecuzione andando al nodo "step_3" per poi terminare

questo per mostrare come possiamo arrestare il flusso prendere dei feedback dall'utente
e le memorizzazioni nel data base
"""
import sqlite3
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
# MemorySaver è un checkpoint che memorizza lo stato dopo l'esecuzione di ogni nodo
# tuttavia lo memorizza in memoria in maniera effimera quindi scomparirà dopo l'esecuzione del nostro grafo
from langgraph.checkpoint.memory import MemorySaver
# per memorizzare in maniera persistente lo stato del grafo
# e far si che non si perda quando inizio una nuova esecuzione del grafo
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
load_dotenv()


# definiamo lo stato del grafo
class State(TypedDict):
    input: str
    user_feedback: str


# definiamo o ra i nodi
def step_1(sate: State) -> None:
    print("---Step 1---")


def human_feedback(state: State) -> None:
    print("---human_feedback---")


def step_3(state: State) -> None:
    print("---Step 3---")


builder = StateGraph(State)

builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)

# archi
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge("step_3", END)

# memorizziamo gli stati del grafo durante la su esecuzione
# memory = MemorySaver()

# invece di usare MemorySaver() che salva gli stati del grafo in maniera effimera
# usiamo il db sqlite
# prima creiamo una connessione ad una base di dati SQLite
# nella variabile database possiamo mettere un URL che indica il db al quale vogliamo connetterci
# se invece mettiamo una stringa .sqlite si crea un db locale nel nostro filesystem
# inoltre vogliamo abilitare check_same_thread=False
# in questo modo possiamo fare operazioni sul DB anche se andiamo ad eseguire thread diversi
conn = sqlite3.connect(database="checkpoints.sqlite", check_same_thread=False)

# ora creiamo la variabile memory che però stavolta è associata a SqliteSaver()
memory = SqliteSaver(conn)


# prima di eseguire il nodo human_feedback, arrestiamo l'esecuzione del grafo
# poiché memorizziamo gli stati quando ci arrestiamo possiamo prendere l'input dell'user
# per far si che ricevano lo human_feedback
# poi possiamo riprendere l'esecuzione del nostro grafo esattamente dove ci siamo fermati.
graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])

# il caso d'uso qui è che quando abbiamo applicazioni user_oriented e vogliamo
# integrare lo human_feedback questa è una tecnica molto utile

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":

    thread = {"configurable": {"thread_id": "777"}}
    #
    # initial_input = {"input": "hello world"}
    #
    # # transmittiamo gli eventi del grafo
    # for event in graph.stream(initial_input, thread, stream_mode="values"):
    #     print(event)
    #
    # # dopo che il grafo si interrompe vediamo se stampa qual'è il prossimo nodo
    # print(graph.get_state(thread).next)

    # diamo l'input dello user
    user_input = input("Tell me how you want to update the state: ")

    # ora che abbiamo l'user input vogliamo aggiornare lo stato del grafo
    # quindi andiamo ad aggiornare anche il thread ID
    graph.update_state(
        thread,
        values={"user_feedback": user_input},
        as_node="human_feedback"
    )

    print("---State after update---")
    print(graph.get_state(thread))
    print(graph.get_state(thread).next)

    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)






