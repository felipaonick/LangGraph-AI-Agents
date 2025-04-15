from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader  # per caricare documenti da internet
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/"
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]  # lista di Document

# ora vogliamo splittare il contenuto dei Documenti in chucks
# from_tiktoken_encoder()
# per dividere il testo in blocchi di token invece che in caratteri o parole.
# chunk_size=250 significa che ogni blocco avrà al massimo 250 token.
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)

# i chucks sono ancora dei Document
docs_splits = text_splitter.split_documents(docs_list)

# ora siamo pronti per indexarli in ChromaDB
# vectorstore = Chroma.from_documents(
#     documents=docs_splits,
#     collection_name="rag-chroma",
#     embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
#     persist_directory="./.chroma"
# )


# creiamo il retriever dal ChromaDB
retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
).as_retriever()


