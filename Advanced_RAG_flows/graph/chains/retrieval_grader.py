"""
come input di questo nodo arrivano i documenti retrivati

ora dobbiamo iterare su questi documenti e determinare se sono rilevanti per la
nostra domanda o no.

per far questo scriviamo una chain di classificazione che usa l'output strutturato
dal nostro LLM e lo converte in un pydantic object che conterrà la informazione,
se questo documento è rilevante o meno.


se il documento non è rilevante dobbiamo filtrarlo e rimanere con solo i documenti
che sono rilevanti per la domanda.

se tutti i documenti non sono rilevanti allora poi in un altro nodo successivo si farà la ricerca web,
quindi dobbiamo modificare il flag del web_search a True.

eseguiamo questa chain per ogni documento che recuperiamo
"""
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)


class GradeDocuments(BaseModel):
    """Binary score for relevance check in retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to question, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question. \n
If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)


retrieval_grader = grade_prompt | structured_llm_grader

