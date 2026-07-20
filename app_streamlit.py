import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_chroma import Chroma

# ..........................
# Configuración de la página.
# ..........................

st.set_page_config(page_title="Agente A.T.I.C.", page_icon="🤖")
st.title("🤖 Agente de Políticas A.T.I.C.")

# ==========================
# Variables de entorno.
# ==========================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    # Usar los "secrets" de Streamlit Cloud (importante para el deploy)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        st.error("No se encontró la GOOGLE_API_KEY. Configúrala en .env o en los secrets de Streamlit.")
        st.stop()


# ==========================
# Carga y preparación dcto.
# ==========================
@st.cache_resource(show_spinner="Cargando documento y preparando el agente...")
def cargar_agente():
    loader = PyPDFLoader("ATIC.pdf")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="chroma_db",
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        temperature=0,
        google_api_key=api_key,
    )

    return retriever, llm


retriever, llm = cargar_agente()


# ................................................
# Función para extraer texto limpio de la respuesta
# .................................................
def extraer_texto(respuesta):
    if isinstance(respuesta.content, list):
        return respuesta.content[0]["text"]
    return respuesta.content


# ==========================
# Historial de chat (memoria de la sesión)
# ==========================
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial previo
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# ==========================
# Input de chat
# ==========================
pregunta = st.chat_input("Escribe tu pregunta sobre las políticas de A.T.I.C...")

if pregunta:
    # Mostrar y guardar la pregunta del usuario
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Buscar contexto relevante
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resultados = retriever.invoke(pregunta)
            contexto = "\n\n".join([doc.page_content for doc in resultados])

            prompt = f"""
Eres un asistente virtual experto en las políticas de A.T.I.C. 
Si el usuario te saluda, responde amablemente y brevemente.

Si no es un saludo, responde únicamente utilizando la información del contexto. 
Si la respuesta no aparece en el documento, responde exactamente: 
'No encuentro esa información en el documento, por favor reformula tu pregunta o escribenos a soporte@atic.com.


Contexto:
{contexto}

Pregunta:
{pregunta}
"""

            respuesta = llm.invoke(prompt)
            texto = extraer_texto(respuesta)

            st.markdown(texto)

    #....................................
    # Guardar respuesta en el historial
    #....................................
    st.session_state.mensajes.append({"role": "assistant", "content": texto})