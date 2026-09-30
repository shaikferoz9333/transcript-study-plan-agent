import uuid

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from document_processor import (
    load_document,
    split_documents,
)


EMBEDDING_MODEL = "all-minilm:latest"

CHROMA_DIRECTORY = "./chroma_database"


def create_vector_store(file_paths):
    all_documents = []

    for file_path in file_paths:

        documents = load_document(
            file_path
        )

        for document in documents:

            document.metadata[
                "source_file"
            ] = str(file_path)

        all_documents.extend(
            documents
        )

    if not all_documents:
        raise ValueError(
            "No documents were loaded."
        )

    chunks = split_documents(
        all_documents
    )

    if not chunks:
        raise ValueError(
            "No document chunks were created."
        )

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    collection_name = (
        "student_material_"
        + uuid.uuid4().hex[:10]
    )

    vector_store = Chroma(
        collection_name=collection_name,

        embedding_function=embeddings,

        persist_directory=CHROMA_DIRECTORY,
    )

    vector_store.add_documents(
        chunks
    )

    return vector_store


def retrieve_material(
    vector_store,
    query,
    k=5,
):
    if vector_store is None:
        raise ValueError(
            "Vector store is not initialized."
        )

    return vector_store.similarity_search(
        query,
        k=k,
    )