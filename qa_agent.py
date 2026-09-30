from pathlib import Path

from langchain_ollama import ChatOllama

from rag import retrieve_material


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "qwen3:0.6b"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        temperature=0.1,
    )


# ============================================================
# SOURCE NAME
# ============================================================

def source_name(metadata):
    path = metadata.get(
        "source_file",
        "Uploaded material"
    )

    return Path(
        str(path)
    ).name


# ============================================================
# MATERIAL ANSWER
# ============================================================

def answer_from_material(
    vector_store,
    question,
):
    if vector_store is None:
        raise ValueError(
            "Material retriever is not available."
        )

    if not question or not question.strip():
        raise ValueError(
            "Please enter a question."
        )

    # --------------------------------------------------------
    # Retrieve relevant chunks
    # --------------------------------------------------------

    documents = retrieve_material(
        vector_store,
        question,
        k=5,
    )

    if not documents:

        return {
            "answer": (
                "I could not find relevant information "
                "in the uploaded material."
            ),
            "sources": [],
        }

    # --------------------------------------------------------
    # Build grounded context
    # --------------------------------------------------------

    context_parts = []

    sources = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        content = (
            document.page_content
            .strip()
        )

        if not content:
            continue

        source = source_name(
            document.metadata
        )

        sources.append(source)

        context_parts.append(
            f"""
SOURCE {index}: {source}

{content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    # --------------------------------------------------------
    # Grounded prompt
    # --------------------------------------------------------

    prompt = f"""
You are an academic assistant.

Answer the student's question using ONLY
the uploaded material provided below.

Do not invent facts.

If the answer is not present in the material,
clearly say:

"I could not find that information in the
uploaded material."

Keep the answer clear and useful for a student.

Question:
{question}

Uploaded material:
{context}

Answer:
"""

    # --------------------------------------------------------
    # ChatOllama
    # --------------------------------------------------------

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    answer = response.content

    if not answer:
        answer = (
            "I could not generate an answer "
            "from the uploaded material."
        )

    return {
        "answer": answer.strip(),

        "sources": list(
            dict.fromkeys(
                sources
            )
        ),
    }