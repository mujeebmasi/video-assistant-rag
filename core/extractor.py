#Actionable Items ..(EX: Mujeeb, you have to do this task by 8pm tomorrow), Decisions, Questions 
# Will be stored in this file
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_llm():
    return ChatMistralAI(model =  "mistral-small-latest", MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY"), temperature = 0.2)

def build_chain(system_prompt:str):
    llm = get_llm()
    return (
        RunnablePassthrough() | RunnableLambda(lambda x: {"transcript": x}) 
        | ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{transcript}")   
    ])  | llm | StrOutputParser())
    
def chunk_transcript(transcript: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    return splitter.split_text(transcript)

def extract_actionable_items(transcript:str) -> str:
    system_prompt = "You are a helpful assistant that extracts actionable items from meeting transcripts. Actionable items are specific tasks or actions that need to be taken based on the discussion in the meeting. They should be concise and clearly defined."
    chain = build_chain(system_prompt)
    chunks = chunk_transcript(transcript)
    results = []
    for chunk in chunks:
        result = chain.invoke(chunk)
        results.append(result)

    return "\n".join(results)
def extract_decisions(transcript:str) -> str:
    system_prompt = "You are a helpful assistant that extracts decisions from meeting transcripts. Decisions are conclusions or resolutions reached during the meeting. They should be concise and clearly defined."
    chain = build_chain(system_prompt)
    chunks = chunk_transcript(transcript)
    results = []
    for chunk in chunks:
        result = chain.invoke(chunk)
        results.append(result)
        
    return "\n".join(results)

def extract_questions(transcript:str) -> str:
    system_prompt = "You are a helpful assistant that extracts questions from meeting transcripts. Questions are inquiries or points of clarification raised during the meeting. They should be concise and clearly defined."
    chain = build_chain(system_prompt)
    chunks = chunk_transcript(transcript)
    results = []
    for chunk in chunks:
        result = chain.invoke(chunk)
        results.append(result)

    return "\n".join(results)
