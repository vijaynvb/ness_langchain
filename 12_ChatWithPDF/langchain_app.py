# implementation of ChatWithPDF using LangChain and expose methods to streamlit app

import os
import tempfile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock
from langchain_community.document_loaders import PyPDFLoader
from langgraph.checkpoint.memory import InMemorySaver


# Load environment variables from .env file
load_dotenv()

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv('AWS_ACCESS_KEY_ID')
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv('AWS_SECRET_ACCESS_KEY')
os.environ["AWS_DEFAULT_REGION"] =os.getenv('AWS_DEFAULT_REGION')

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        temp_path = None
        try:
            # Streamlit uploads are in-memory objects; PyPDFLoader needs a file path.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(pdf.getvalue())
                temp_path = temp_file.name

            pdf_loader = PyPDFLoader(temp_path)
            for page in pdf_loader.load():
                text += page.page_content or ""
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
    )
    return text_splitter.split_text(text)


def get_vectorstore(text_chunks):

    embedding = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0"
    )
    return FAISS.from_texts(texts=text_chunks, embedding=embedding)


SYSTEM_PROMPT = """You are a professional assistant that answers questions about uploaded PDF documents.

Rules:
- ALWAYS call the `search_documents` tool first before answering any question, even greetings.
- Use the retrieved content from the tool to form your answer.
- If the tool returns no relevant information, say: "I'm sorry, I don't have enough information based on the provided documents."
- If the question is clearly outside the scope of the documents, politely say so.
- Do not answer from your own knowledge — always ground your response in the retrieved document content.
- Keep your response concise and under 100 words.
"""

def get_conversation_chain(vectorstore):
    

    llm = ChatBedrock(
        model_id="mistral.mistral-7b-instruct-v0:2",
        temperature=0.5
    )
    retriever = vectorstore.as_retriever()
    @tool
    def search_documents(query: str) -> str:
        """Search the uploaded PDF documents for relevant information."""
        docs = retriever.get_relevant_documents(query)
        if not docs:
            return "No relevant information found in the uploaded documents."
        return "\n\n".join(
            f"[Chunk {i+1}]:\n{doc.page_content}"
            for i, doc in enumerate(docs)
        )
    agent = create_agent(
        model=llm,
        tools=[search_documents],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
    )

    return agent