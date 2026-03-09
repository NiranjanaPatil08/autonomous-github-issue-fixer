def get_relevant_chunks(vectorstore, query, k=5):

    docs = vectorstore.similarity_search(query, k=k)

    return docs
