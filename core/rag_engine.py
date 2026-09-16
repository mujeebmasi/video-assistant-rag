import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from core.vector_store import (
    create_vector_store,
    load_vector_store,
    get_retriever,
    new_collection_name,
)

SYSTEM_PROMPT = """You are an expert meeting assistant. Answer the user's question
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say:
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}"""


def get_llm():
    mistral_api_key = os.getenv("MISTRAL_API_KEY", "").strip()
    if not mistral_api_key:
        raise ValueError("MISTRAL_API_KEY is not set")

    return ChatMistralAI(model =  "mistral-small-latest",
                        api_key = mistral_api_key,
                        temperature = 0.2)

def format_document(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def build_chain_for(vector_store):
    llm = get_llm()
    retriever = get_retriever(vector_store, k=5)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    #Full LCEL Pipeline
    rag_chain_starting_point = {
        "context": retriever | RunnableLambda(format_document),
        "question": RunnablePassthrough()
    }

    return rag_chain_starting_point | prompt | llm | StrOutputParser()

def build_rag_chain(transcript:str, collection_name:str | None = None):
    if collection_name is None:
        collection_name = new_collection_name()
    vector_store = create_vector_store(transcript, collection_name)
    return build_chain_for(vector_store)

def load_rag_chain(collection_name:str):
    vector_store = load_vector_store(collection_name)
    return build_chain_for(vector_store)

def ask_question(rag_chain, question:str) -> str:
    print(f"Asking question: {question}")
    return rag_chain.invoke(question)
