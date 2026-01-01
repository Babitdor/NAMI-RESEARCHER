import os
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    DirectoryLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
DOCUMENT_DIR = "./documents"
CHROMA_DB_DIR = "./knowledge"


def load_documents():
    """Load documentes from the documents directory."""
    print("---> Loading Documents... ")

    documents = []

    # Load PDFs
    pdf_loader = DirectoryLoader(
        path=DOCUMENT_DIR, glob="**/*.pdf", loader_cls=PyMuPDFLoader, show_progress=True  # type: ignore
    )

    documents.extend(pdf_loader.load())

    # Load Texts
    txt_loader = DirectoryLoader(
        path=DOCUMENT_DIR, glob="**/*.txt", loader_cls=TextLoader, show_progress=True
    )

    documents.extend(txt_loader.load())

    print(f" Loaded {len(documents)} document pages")
    return documents


def split_document(documents):
    """Split documents into smaller chunks"""
    print("---> Splitting documents into chuncks ")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    chunks = text_splitter.split_documents(documents=documents)
    print(f"---> Created {len(chunks)} chunks")
    return chunks


def create_vectorstore(chunks):
    """Create Vector store from document chunks"""
    print("---> Creating embeddings and vector store...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )

    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=CHROMA_DB_DIR
    )

    print(f"Vector store created with {vectorstore._collection.count()} vectors")
    return vectorstore


def main():
    """Main Ingestion Pipeline"""
    print("---> Starting Document ingestion...\n")

    os.makedirs(DOCUMENT_DIR, exist_ok=True)

    if not any(os.scandir(DOCUMENT_DIR)):
        print(f" No documents found in {DOCUMENT_DIR}")
        print("Please add some PDF or TXT files to the documents folder")
        return

    documents = load_documents()
    chunks = split_document(documents)
    vectorstore = create_vectorstore(chunks=chunks)

    print("\n✨ Ingestion complete!")


if __name__ == "__main__":
    main()
