"""
creaimo i nodi e li colleghiamo creando il grafo
"""
from dotenv import load_dotenv

from langgraph.graph import END, StateGraph
from Advanced_RAG_flows.graph.consts import RETRIEVE, GENERATE, GRADE_DOCUMENTS, WEBSEARCH
from Advanced_RAG_flows.graph.nodes import generate, retrieve, web_search, grade_documents
from Advanced_RAG_flows.graph.state import GraphState
from Advanced_RAG_flows.graph.chains.hallucination_grader import hallucination_grader
from Advanced_RAG_flows.graph.chains.answer_grader import answer_grader
from Advanced_RAG_flows.graph.chains.router import RouteQuery, question_router

load_dotenv()


# definiamo un'altra funzione per il conditional edge
# che va a stabilire se la risposta del modello è basata sui
# documenti o se rifare una ricerca web
# oppure se la risposta non c'entra niente e quindi è una allucinazione
def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state['generation']

    score = hallucination_grader.invoke({"documents": documents, "generation": generation})

    """
    hallucination_grade = score.binary_score
    if hallucination_grade: # è True
        # esegui qualcosa
    """
    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS (hallucinations)---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"  # bisogna fare la ricerca web
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS (no hallucinations)---")
        return "not supported"  # bisogna rigenerare la risposta


# definiamo la funzione per decidere se andare nel nodo web_search (quando ci sono documenti non rilvanti per la question)
# o se andare direttamente al nodo generate
def decide_to_generate(state):
    print("---ASSES GRADED DOCUMENTS---")

    if state['web_search']:
        # vado nel nodo web_search
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return WEBSEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE


def route_question(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state["question"]
    source: RouteQuery = question_router.invoke({"question": question})
    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE


workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(WEBSEARCH, web_search)
workflow.add_node(GENERATE, generate)

workflow.set_conditional_entry_point(
    route_question,
    path_map={
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE
    }
)

workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(GRADE_DOCUMENTS, decide_to_generate,
                               path_map={
                                   WEBSEARCH: WEBSEARCH,
                                   GENERATE: GENERATE
                               })
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    path_map={
        "not support": GENERATE,  # allucinazioni quindi rigenera
        "useful": END,
        "not useful": WEBSEARCH  # la risposta non soddisfa la domanda dell'utente quindi -> ricerca web
    }
)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="adaptive-self-rag-graph.png")


