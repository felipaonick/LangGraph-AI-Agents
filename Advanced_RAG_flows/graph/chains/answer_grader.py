"""
implementiamo la chain che crea la risposta e determina se la risposta
risponde o meno alle domande dell'utente
"""

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


class GradeAnswer(BaseModel):

    binary_score: bool = Field(
        description="Answer addresses the question, 'True' or 'False'"
    )


llm = ChatOpenAI(model="gpt-4o", temperature=0)

structured_llm_grader = llm.with_structured_output(GradeAnswer)


system = """You are a grader assessing whether an answer addresses / resolves a question \n
Give a binary score 'True' or 'False'. 'True' means that the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}")
    ]
)


answer_grader = answer_prompt | structured_llm_grader

