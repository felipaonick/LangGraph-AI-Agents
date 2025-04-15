from dotenv import load_dotenv

load_dotenv()

from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph

# StateGraph è un grafo in cui i nodi si comunicano leggendo e scrivendo in uno
# stato condiviso. Questo stato condiviso può essere qualsiasi cosa che definiamo.
# Questo spazio deve essere descritto con lo schema, che è un dizionario di Type

# quando creiamo un oggetto della classe StateGraph dobbiamo assegnarli uno schema
# che deve essere un dizionario di Types


from nodes import execute_tools, run_agent_reasoning_engine
from state import AgentState


AGENT_REASON = "agent_reason"
ACT = "act"


# definiamo una funzione che funzionerà come arco condizionale
def should_continue(state: AgentState) -> str:
    if isinstance(state['agent_outcome'], AgentFinish):
        return END
    else:
        return ACT


# definiamo il nostro grafo
# è un StateGraph dove lo inizializziamo con lo stato dell'agente che abbiamo cretao
flow = StateGraph(AgentState)


# aggiungiamo il primo nodo al grafo
flow.add_node(AGENT_REASON, run_agent_reasoning_engine)
# vogliamo anche stabilirlo come nodo di entrata nel nostro grafo
flow.set_entry_point(AGENT_REASON)

# mettiamo il nodo ACT che esegue la funzione execute_tools
flow.add_node(ACT, execute_tools)

# definiamo l'arco condizionale tra il nodo di reasoning e il nodo che esegue i tools ACT o il nodo finale END
flow.add_conditional_edges(AGENT_REASON, should_continue)

# mettiamo l'arco tra il nodo ACT e AGENT_REASON
# volgiamo sempre andare all'agente di reasoning, dopo l'esecuzione del nodo ACT,
# poiché l'agente deciderà se abbiamo sufficiente informazione per terminare l'esecuzione o se dobbiamo fare un'altra iterazione
flow.add_edge(ACT, AGENT_REASON)


app = flow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":

    print("Hello RaAct with LangGraph")

    res = app.invoke(
        input={"input": "what is the weather in sf? List it and then Triple it"}
    )

    print(f"{res['agent_outcome'].return_values['output']}")

