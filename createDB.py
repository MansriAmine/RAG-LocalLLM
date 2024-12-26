import argparse
import os
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from local_embedding_function import local_embedding_function
from langchain.vectorstores.chroma import Chroma


CHROMA_PATH = "chroma"  # Directory to store Chroma database
DATA_PATH = "data"  # Directory where PDF files are stored

def main():
    # Set up argument parser for command-line options.
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()

    # If --reset flag is used, clear the database.
    if args.reset:
        print("Clearing Database")
        clear_database()

    # Load, split, and add documents to the Chroma database.
    documents = load_documents()  # Load documents from the data directory
    chunks = split_documents(documents)  # Split documents into smaller chunks
    add_to_chroma(chunks)  # Add chunks to Chroma database


def load_documents():
    # Load PDF documents from the DATA_PATH directory.
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    # Split the documents into smaller chunks for easier processing.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Max chunk size
        chunk_overlap=80,  # Overlap between chunks
        length_function=len,  # Use length of text to determine chunk size
        is_separator_regex=False,  # Do not use regex for separators
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):
    # Load the existing Chroma database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=local_embedding_function()
    )

    # Calculate and add unique IDs to the document chunks.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Get existing documents in the database.
    existing_items = db.get(include=[])  # Always include IDs
    existing_ids = set(existing_items["ids"])  # Set of existing IDs
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Filter out chunks that already exist in the database.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    # Add new chunks to the database if any.
    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]  # Get new chunk IDs
        db.add_documents(new_chunks, ids=new_chunk_ids)  # Add new documents
        db.persist()  # Save the changes
    else:
        print("No new documents to add")


def calculate_chunk_ids(chunks):
    # Generate unique IDs for each chunk based on source and page.
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")  # Get source (e.g., file name)
        page = chunk.metadata.get("page")  # Get page number
        current_page_id = f"{source}:{page}"

        # Increment chunk index if page ID is the same as the last one.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Create chunk ID: "source:page:chunk_index"
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id  # Update last page ID

        # Add chunk ID to the chunk metadata.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    # Delete the Chroma database if it exists.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()  # Run the main function
