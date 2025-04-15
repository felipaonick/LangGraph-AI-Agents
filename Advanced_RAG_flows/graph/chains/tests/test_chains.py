# testiamo la chain e se funziona la mettiamo dentro un nodo del grafo

from dotenv import load_dotenv
from Advanced_RAG_flows.graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from Advanced_RAG_flows.ingestion import retriever
from Advanced_RAG_flows.graph.chains.generation import generation_chain
from dotenv import load_dotenv
load_dotenv()
from pprint import pprint
from Advanced_RAG_flows.graph.chains.hallucination_grader import hallucination_grader
from Advanced_RAG_flows.graph.chains.hallucination_grader import GradeHallucinations
from Advanced_RAG_flows.graph.chains.router import RouteQuery, question_router


def test_retrieval_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    # invochiamo la chain sul documento e sulla domanda
    # la chain verifica se il documento è rilevante in base alla domanda
    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "yes"


def test_retrieval_grader_answer_no() -> None:
    question = "how to make pizza"
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "no"


def test_generation_chain() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"question": question, "context": docs})

    pprint(generation)


def test_hallucination_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({"question": question, "context": docs})

    res: GradeHallucinations = hallucination_grader.invoke({"documents": docs, "generation": generation})

    assert res.binary_score


def test_hallucination_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    res: GradeHallucinations = hallucination_grader.invoke({
        "documents": docs,
        "generation": "In order to make pizza we need to first start with the dough."
    })

    assert not res.binary_score


def test_router_to_vectorstore() -> None:
    question = "agent memory"

    res: RouteQuery = question_router.invoke({"question": question})

    assert res.datasource == "vectorstore"


def test_router_to_websearch() -> None:
    question = "how to make pizza"

    res: RouteQuery = question_router.invoke({"question": question})

    assert res.datasource == "websearch"



