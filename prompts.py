# prompts.py

from langchain import hub

# Pull the standard RAG prompt from LangChain Hub.
# For non-US LangSmith endpoints, add: api_url="https://api.smith.langchain.com"
prompt = hub.pull("rlm/rag-prompt")

if __name__ == "__main__":
    example_messages = prompt.invoke(
        {"context": "(context goes here)", "question": "(question goes here)"}
    ).to_messages()

    assert len(example_messages) == 1
    print(example_messages[0].content)
