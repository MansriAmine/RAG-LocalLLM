import os
import shutil
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from local_embedding_function import local_embedding_function
from langchain.vectorstores.chroma import Chroma

def process_pdf_to_chroma(pdf_path, chroma_path="chroma"):
    """
    Process a PDF file, split its content into chunks, and add the chunks to a Chroma database.

    Args:
        pdf_path (str): Path to the PDF file.
        chroma_path (str): Path to the Chroma database directory. Defaults to "chroma".
    """
    def load_pdf(pdf_path):
        # Load the PDF file as a document.
        document_loader = PyPDFLoader(pdf_path)
        return document_loader.load()

    def split_documents(documents):
        # Split the documents into smaller chunks for easier processing.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # Max chunk size
            chunk_overlap=100,  # Overlap between chunks
            length_function=len,  # Use length of text to determine chunk size
            is_separator_regex=False,  # Do not use regex for separators
        )
        return text_splitter.split_documents(documents)

    def calculate_chunk_ids(chunks):
        # Generate unique IDs for each chunk based on source and page.
        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source", "unknown")  # Get source (e.g., file name)
            page = chunk.metadata.get("page", "unknown")  # Get page number
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

    def add_to_chroma(chunks):
        # Load the Chroma database, creating it if necessary.
        db = Chroma(
            persist_directory=chroma_path, embedding_function=local_embedding_function()
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
        if new_chunks:
            print(f"Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]  # Get new chunk IDs
            db.add_documents(new_chunks, ids=new_chunk_ids)  # Add new documents
            db.persist()  # Save the changes
        else:
            print("No new documents to add")

    # Ensure the Chroma database directory exists.
    if not os.path.exists(chroma_path):
        os.makedirs(chroma_path)

    # Load, split, and add the PDF to the Chroma database.
    print(f"Processing PDF: {pdf_path}")
    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)
    add_to_chroma(chunks)

# Example usage:
# process_pdf_to_chroma(file_path)
