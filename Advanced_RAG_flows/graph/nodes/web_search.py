from typing import Any, Dict

# vogliamo convertire i risultati di ricerca con Tavily in formato Document
from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults
from Advanced_RAG_flows.graph.state import GraphState
from dotenv import load_dotenv
load_dotenv()

web_search_tool = TavilySearchResults(max_results=3)


# definiamo la funzione che va nel nodo e che riceve lo stato del grafo
# si farà la ricerca web e restituiremo un dizionario
def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state['question']
    # i documenti che abbiamo sono i documenti filtrati quindi tutti sono rilevanti
    documents = state['documents']

    # invochiamo il tool
    tavily_results = web_search_tool.invoke({"query": question})

    # ora vogliamo prendere i contenuti dei 3 risultati di ricerca e metterli dentro il page_content di un Document langchain
    joined_tavily_result = "\n".join(
        [result['content'] for result in tavily_results]
    )

    web_results = Document(
        page_content=joined_tavily_result
    )

    # se abbiamo dei documenti rilevanti. aggiungiamo ad essi i risulati della ricerca
    # in modo da avere informazione completa da dare al modello nel contesto
    if documents is not None:
        documents.append(web_results)
    else:  # se non ci sono documenti rilevanti allora passiamo solamente il Document con i risultati del web
        documents = [web_results]

    # infine aggiorniamo lo stato del grafo
    return {"documents": documents, "question": question}





if __name__ == "__main__":
    # scenario in cui non troviamo alcun documento rilevante nel nodo grade_documents
    web_search(
        state={"question": "agent memory", "documents": [], "generation": "", "web_search": True}
    )

