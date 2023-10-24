import os
import scrape_to_txt

from langchain.document_loaders import ReadTheDocsLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone

from const import INDEX_NAME

pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")


def ingest_docs() -> None:
    scrape_to_txt.read_web_pages()

    loader = TextLoader('mail')

    # raw_documets = loader.load()

    docs_list = []
    for file in os.listdir('mail'):
        # if file.endswith('.txt'):
        text_path = 'mail/' + file
        loader = TextLoader(text_path)
        docs_list.extend(loader.load())


    print(f"loaded {len(docs_list)} documents")
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=20, chunk_overlap=5, separators=["\n\n", "\n" " ", ""]
    # )

    text_splitter = CharacterTextSplitter(
        chunk_size=600, chunk_overlap=10
    )

    documents = text_splitter.split_documents(documents=docs_list)
    print(f"splitted into {len(documents)} chucks")

    # # get the url
    # for doc in documents:
    #     old_path = doc.metadata["source"]
    #     new_url = old_path.replace("langchain-docs", "https:/")
    #     doc.metadata.update({"source": new_url})

    print(f"going to insert {len(documents)} to PineCone")
    embeddings = OpenAIEmbeddings()
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("**** Added to Pinecone vectorsstore vectores")




if __name__ == "__main__":
    ingest_docs()
