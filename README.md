Agente RAG: Asistente de Políticas A.T.I.C.
Este proyecto es un sistema de Generación Aumentada por Recuperación (RAG) diseñado para optimizar la consulta de documentación interna. Permite a los colaboradores realizar preguntas en lenguaje natural sobre las políticas de la empresa sin necesidad de navegar manualmente a través de archivos extensos.

Arquitectura Técnica
El agente está construido sobre los siguientes pilares tecnológicos:

Lenguaje: Python.
Orquestación: LangChain (para gestionar la lógica del agente y la memoria).
Procesamiento de Documentos: PyPDFLoader (carga de documentos) y RecursiveCharacterTextSplitter (segmentación en chunks).
Base de Datos Vectorial: ChromaDB (almacenamiento y recuperación de embeddings).
Modelo de Lenguaje: Google Gemini 1.5 Flash (vía langchain-google-genai).
Interfaz de Usuario: Streamlit (para una experiencia de chat web interactiva).

Despliegue en la Nube
El proyecto fue desplegado en Streamlit Community Cloud.Nota técnica: Se optó por esta solución en lugar de OCI (Oracle Cloud Infrastructure) debido a restricciones de validación bancaria en la plataforma OCI, garantizando así un despliegue ágil, seguro y 100% funcional para la evaluación del desafío.

Cómo ejecutar el proyecto
Requisitos previos
Tener instalado Python.
Obtener una API Key gratuita de Google AI Studio.
Pasos para ejecución local
Clona este repositorio:

Bash

git clone https://github.com/tu-usuario/proyecto-agente.git
Instala las dependencias:

Bash

pip install -r requirements.txt
Crea un archivo .env en la raíz con tu clave:

Plaintext

GOOGLE_API_KEY=tu_clave_aqui
Ejecuta la aplicación:

Bash

streamlit run app_streamlit.py


Ejemplos de uso
El agente es capaz de responder preguntas precisas como:

"¿Cuál es el plazo que tiene un cliente para presentar un reclamo?"
"¿A qué correo electrónico se deben enviar las consultas de privacidad?"
"¿Cuál es el RUT de A.T.I.C.?"
