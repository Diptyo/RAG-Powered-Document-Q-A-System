# result.py

from RAG import graph

result = graph.invoke({"question": "What is Task Decomposition?"})

# Pretty-print context chunks
print("📄 Retrieved Context:\n")
for i, doc in enumerate(result["context"], 1):
    source = doc.metadata.get("source", "unknown")
    print(f"  [{i}] (source: {source})")
    print(f"      {doc.page_content[:200].strip()}...")
    print()

print(f"💡 Answer:\n{result['answer']}")
