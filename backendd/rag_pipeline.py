import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from embeddings import get_embeddings
from config import GROQ_API_KEY, MODEL_NAME
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)


def load_and_index(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local("vectorstore")


def load_vectorstore():
    if not os.path.exists("vectorstore"):
        raise Exception("❌ No vectorstore found. Upload PDF first.")

    embeddings = get_embeddings()
    return FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )


def ask_llm(context, question):
    prompt = f"""
You are an interview preparation assistant.

Context:
{context}

Question:
{question}

Give a clear explanation with examples.
"""

    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def ask_question(query):
    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(query, k=3)

    if not docs:
        return "No relevant data found. Please upload PDF."

    context = "\n".join([doc.page_content for doc in docs])

    return ask_llm(context, query)