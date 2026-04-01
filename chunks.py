# chunks.py

import bs4
import nltk
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import NLTKTextSplitter

# Ensure the NLTK sentence tokenizer data is available
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


def get_chunks():
    """Load the target webpage and split it into overlapping sentence-aware chunks."""
    bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} document(s). Total characters: {len(docs[0].page_content)}")

    text_splitter = NLTKTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    all_splits = text_splitter.split_documents(docs)
    print(f"✅ Split into {len(all_splits)} chunks.")
    return all_splits


if __name__ == "__main__":
    chunks = get_chunks()
    print(chunks[0].page_content[:300])
