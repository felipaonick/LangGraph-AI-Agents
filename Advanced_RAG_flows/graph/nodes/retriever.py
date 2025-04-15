from typing import Any, Dict

# l'input per i nostri nodi
from Advanced_RAG_flows.graph.state import GraphState

# importiamo anche il retriever dal VS
from Advanced_RAG_flows.ingestion import retriever


# funzione del nodo retrieve
# restituisce un dizionario per aggiornare lo stato
def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    question = state['question']

    documents = retriever.invoke(question)

    # con l'output vogliamo aggiornare solo il campo dei documents
    # e aggiungiamo anche la domanda originale solo per precauzione ma non sarebbe necessario
    # i documenti retrievati sono Document di langchain
    return {"documents": documents, "question": question}



