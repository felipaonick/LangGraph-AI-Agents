"""
creiamo il nodo che esegue la chain retrieval_grader per valutare se un documento
è pertinente alla question o meno.
Dunque filtriamo i documenti tenendo solo quelli pertinenti scartando quelli non pertinenti
se nessun documento è pertinente setta il campo web_search dello stato del grafo in base a questo risultato
che entrerà in input al prossimo nodo
"""

from typing import Any, Dict
from Advanced_RAG_flows.graph.state import GraphState
from Advanced_RAG_flows.graph.chains.retrieval_grader import retrieval_grader


# la chain retrieval_grader controlla un documento per volta
# quindi necessitaimo di una funzione che controlli tutti i documenti retrievati
def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")

    question = state['question']
    documents = state['documents']

    # per aggiungere i documenti rilevanti
    filtered_list = []
    # se troviamo un documento che è irrilevante lo cambiamo a True
    web_search = False

    for doc in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": doc.page_content}
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_list.append(doc)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            web_search = True
            continue  # passa all'iterazione successiva

    # infine aggiorniamo lo stato del grafo
    return {"documents": filtered_list, "question": question, "web_search": web_search}









