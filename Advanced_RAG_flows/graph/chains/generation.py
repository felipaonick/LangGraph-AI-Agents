"""
implementiamo l'ultimo nodo del grafo che sarà quello che da la risposta finale
Eseguiamo questo nodo dopo aver recuperato la informazione, i documenti rilevanti, dopo aver filtrato i documenti che non
erano rilevanti per la nostra question, e dopo aver aggiunto anche eventuali risultati di ricerche sul web

ora che abbiamo tutti i documenti, possiamo aumentare il contesto e quindi generare una risposta

qui inviamo tutto all'LLM per far si che risponda
"""
from langchain import hub
# converte l'output del LLM in una stringa
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
prompt = hub.pull("rlm/rag-prompt")  # con question e context

generation_chain = prompt | llm | StrOutputParser()


