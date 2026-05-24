from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassThrough, RunnableLambda
import os

def get_llm():
    return ChatMistralAI(model =  "mistral-small-latest", MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY"), temperature = 0.3)
    
def split_transcript(transcript:str) -> list:
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
    return splitter.split_text(transcript)

def summarize_transcript(transcript:str) -> str:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that summarizes meeting transcripts."),
        ("human", "Summarize the following transcript:\n{transcript}")
    ])
    chain = prompt | llm | StrOutputParser()
    
    chunks = split_transcript(transcript)
    chunk_summaries = []  #basically acts like a context memory . used when the transcript is TOO BIGGG
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = chain.invoke({"transcript": chunk})
        chunk_summaries.append(summary)
        
    combines = "\n\n".join(chunk_summaries)
    
    prompt_for_combined = ChatPromptTemplate.from_messages([
        ("system", "You are a expert summarizer assistant combine these partial summaries into one final summary in bullet points."), 
        ("human", "Summarize the following combined summaries:\n{combined_summaries}")
    ])
    chain_for_combined = (RunnablePassThrough() | RunnableLambda(lambda x: {"combined_summaries": x}) | prompt_for_combined | llm | StrOutputParser())
    
    return chain_for_combined.invoke(combines)

def generate_title(transcript: str) -> str:
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that generates concise and descriptive titles for meeting transcripts."),
        ("human", "Generate a concise and descriptive title for the following transcript:\n{transcript}")
    ])
    
    chain_for_title = (RunnablePassThrough() | RunnableLambda(lambda x: {"transcript": x}) | prompt | llm | StrOutputParser())
    
    return chain_for_title.invoke(transcript)