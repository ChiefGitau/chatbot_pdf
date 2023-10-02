import os

from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

from const import INDEX_NAME

pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")


def ingest_docs() -> None:
    loader = ReadTheDocsLoader(
        path="langchain-docs/langchain-docs/api.python.langchain.com/en/latest"
    )
    raw_documets = loader.load()
    print(f"loaded {len(raw_documets)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", " ", ""]
    )
    documents = text_splitter.split_documents(documents=raw_documets)
    print(f"splitted into {len(documents)} chucks")

    # get the url
    for doc in documents:
        old_path = doc.metadata["source"]
        new_url = old_path.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"going to insert {len(documents)} to PineCone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents[3969:], embeddings, index_name=INDEX_NAME)
    print("**** Added to Pinecone vectorsstore vectores")


if __name__ == "__main__":
    ingest_docs()
