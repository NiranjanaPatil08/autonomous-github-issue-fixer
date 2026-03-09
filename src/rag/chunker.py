from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = []

    for doc in documents:
        splits = text_splitter.split_text(doc["content"])

        for split in splits:
            chunks.append({
                "content": split,
                "file_path": doc["file_path"]
            })

    return chunks
