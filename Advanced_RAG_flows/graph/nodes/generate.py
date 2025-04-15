"""
creiamo il nodo che utilizza la chain per la generazione della risposta finale
"""

from typing import Any, Dict

from Advanced_RAG_flows.graph.chains.generation import generation_chain
from Advanced_RAG_flows.graph.state import GraphState


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    generation = generation_chain.invoke({
        "context": documents, "question": question
    })

    # aggiorniamo lo stato del grafo
    return {"documents": documents, "question": question, "generation": generation}

