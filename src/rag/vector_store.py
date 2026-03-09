from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings



def build_vector_store(chunks):

    texts = [c["content"] for c in chunks]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(texts, embeddings)

    return vectorstore
