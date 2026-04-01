# RAG.py

from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from prompts import prompt
from vector_store import vector_store
from llm import llm
from langgraph.graph import START, StateGraph


# ── State schema ────────────────────────────────────────────────────────────
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# ── Step 1: Retrieval ────────────────────────────────────────────────────────
def retrieve(state: State) -> dict:
    retriever = vector_store.as_retriever()
    # .invoke() is the current API; get_relevant_documents() is deprecated
    docs = retriever.invoke(state["question"])
    return {"context": docs}


# ── Step 2: Generation ──────────────────────────────────────────────────────
def generate(state: State) -> dict:
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({
        "question": state["question"],
        "context": docs_content,
    })
    response = llm.invoke(messages)
    return {"answer": response.content}


# ── Step 3: Build graph ─────────────────────────────────────────────────────
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


# ── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    question = "What are the main challenges of building LLM agents?"
    result = graph.invoke({"question": question})
    print("📌 Final Answer:\n")
    print(result["answer"])
