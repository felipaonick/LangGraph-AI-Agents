from typing import List, TypedDict
from langchain.schema import Document

class GraphState(TypedDict):
    """
    include tutti gli stati che necessitiamo per l'esecuzione del grafo.
    vogliamo tenere la domanda nel nostro stato perché facciamo sempre riferimento ad essa
    sia per determinare se i documenti retrivati sono rilevanti per la domanda, sia per stabilire
    se dobbiamo cercare su internet.
    Inoltre vogliamo salvare i documenti retrivati che ci aiutano a rispondere alla domanda retrivati dal documento o dalla ricerca sul internet

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str
    generation:  str
    web_search: bool
    documents: List[Document]

