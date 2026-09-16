import os
import uuid

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DB_DIR = "vector_db"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def new_collection_name() -> str:
    # Every analysed video gets its own collection. Chroma adds to a collection
    # instead of replacing it, so when every video shared one name the chunks
    # piled up together and the chatbot answered from the wrong video.
    return f"meeting_{uuid.uuid4().hex[:12]}"

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={
            "device": "cuda"
            if os.getenv("USE_CUDA", "false").lower() == "true"
            else "cpu"
        },
    )
    
def create_vector_store(transcripts, collection_name):
    print(f"Creating vector store in collection {collection_name}...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(transcripts)
    docs = [
        Document(page_content=chunk, metadata={"source": f"chunk_{i}"})
        for i, chunk in enumerate(chunks)
    ]
    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=CHROMA_DB_DIR
    )
    return vector_store

def load_vector_store(collection_name):
    print(f"Loading vector store from collection {collection_name}...")
    embeddings = get_embeddings()
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    return vector_store

def get_retriever(vector_store, k=5):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k})