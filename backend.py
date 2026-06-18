import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
# Importamos un generador de embeddings básico en memoria
from langchain_core.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class AITutor:
    def __init__(self):
        # 1. El cerebro (LLM) Gratuito con Groq
        self.llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)
        
        # 2. Embeddings falsos de tamaño 384 (idéntico a MiniLM) para estructurar Chroma en memoria
        self.embeddings = FakeEmbeddings(size=384)
        
        self.vector_store = None
        self.retriever = None

    def ingest_pdf(self, file_path: str):
        """Lee el PDF, lo fragmenta y lo guarda en la base de datos vectorial"""
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        # Guardar en ChromaDB de forma local e instantánea
        self.vector_store = Chroma.from_documents(documents=splits, embedding=self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def get_rag_chain(self):
        """Crea la estructura de la cadena RAG con LCEL"""
        if not self.retriever:
            raise ValueError("Primero debes ingerir un documento PDF.")

        system_prompt = (
            "Eres un tutor de IA experto. Usa los siguientes fragmentos de contexto recuperados "
            "para responder la pregunta del usuario de manera educativa en ESPAÑOL. Si no sabes la respuesta, di que no la sabes.\n\n"
            "Contexto:\n{context}"
        )
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        rag_chain = (
            {
                "context": self.retriever | self.format_docs,
                "input": lambda x: x["input"],
                "chat_history": lambda x: x["chat_history"]
            }
            | qa_prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain