import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_chroma import Chroma

# ==========================
# Cargar variables de entorno
# ==========================
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("No existe GOOGLE_API_KEY en el archivo .env")

print("Cargando PDF...")

loader = PyPDFLoader("ATIC.pdf")
documents = loader.load()

print("Dividiendo documento...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

docs = text_splitter.split_documents(documents)

print("Creando embeddings...")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=api_key,
)

print("Creando base vectorial...")

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="chroma_db",
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

print("Cargando Gemini...")

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0,
    google_api_key=api_key,
)

print("\nAgente listo.\n")

while True:

    pregunta = input("Pregunta: ")

    if pregunta.lower() == "salir":
        break

    resultados = retriever.invoke(pregunta)

    contexto = "\n\n".join(
        [doc.page_content for doc in resultados]
    )

    prompt = f"""
Eres un asistente virtual experto en las políticas de A.T.I.C. 
Si el usuario te saluda, responde amablemente y brevemente.

Si no es un saludo, responde únicamente utilizando la información del contexto. 
Si la respuesta no aparece en el documento, responde exactamente: 
'No encuentro esa información en el documento, por favor reformula tu pregunta o escribenos a soporte@atic.com.'

Contexto:
{contexto}

Pregunta:
{pregunta}
"""

    respuesta = llm.invoke(prompt)

    print("\nRespuesta:\n")
    if isinstance(respuesta.content, list):
        texto = respuesta.content[0]['text']
    else:
        texto = respuesta.content
    print(texto)
    print("-" * 70)