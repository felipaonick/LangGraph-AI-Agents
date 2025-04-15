"""
implementiamo una chain che va a determinare se la risposta che otteniamo
dall'LLM si basa sui documenti
"""

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(model="gpt-4o", temperature=0)


class GradeHallucinations(BaseModel):
    """
    Binary score for hallucination present in generation answer.
    """

    binary_score: bool = Field(
        description="Answer is grounded in the facts, 'True' or 'False'"
    )


# anche qui vogliamo che l'uscita dall'LLM sia strutturata
structured_llm_grader = llm.with_structured_output(GradeHallucinations)


system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
Give a binary score 'True' or 'False'. 'True' means that the answer is grounded in / supported by the set of facts."""

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}")
    ]
)


hallucination_grader = hallucination_prompt | structured_llm_grader

