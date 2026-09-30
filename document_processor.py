from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


# ---------------------------------------------------------
# LOAD DOCUMENT
# ---------------------------------------------------------

def load_document(file_path: str):
    """
    Load PDF, TXT or Markdown files.

    Text files are loaded with UTF-8 first and then
    Windows encoding as a fallback.
    """

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()


    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    if extension == ".pdf":

        loader = PyPDFLoader(
            str(path)
        )

        return loader.load()


    # -----------------------------------------------------
    # TEXT / MARKDOWN
    # -----------------------------------------------------

    elif extension in [".txt", ".md"]:

        try:

            loader = TextLoader(
                str(path),
                encoding="utf-8"
            )

            return loader.load()

        except Exception:

            # Windows fallback
            loader = TextLoader(
                str(path),
                encoding="cp1252"
            )

            return loader.load()


    # -----------------------------------------------------
    # UNSUPPORTED FILE
    # -----------------------------------------------------

    else:

        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Please upload a PDF, TXT, or MD file."
        )


# ---------------------------------------------------------
# SPLIT DOCUMENTS
# ---------------------------------------------------------

def split_documents(documents):
    """
    Split documents into smaller chunks while keeping
    related information together.
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=800,

        chunk_overlap=150,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]

    )

    return splitter.split_documents(
        documents
    )