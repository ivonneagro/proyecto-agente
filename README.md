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

Clona el repositorio:
git clone [https://github.com/ivonneagro/proyecto-agente.git](https://github.com/ivonneagro/proyecto-agente.git)

Instala las dependencias:
pip install -r requirements.txt

Crea un archivo .env en la raíz con tu clave:
GOOGLE_API_KEY=tu_clave_aqui

Ejecuta la aplicación:
streamlit run app_streamlit.py


Ejemplos de uso
El agente es capaz de responder preguntas precisas como:

"¿Puedo devolver un producto?"
"¿cuales son los requisitos para solicitar la devolución?"
"¿Qué sucede con los datos que entrego ?"

Ejemplos de respuestas
El agente es capaz de entregar las siguientes respuestas:

"Los requisitos para solicitar una devolución o reclamo son los siguientes:

Presentar el comprobante de compra o un antecedente que permita identificar la transacción.
El producto deberá conservar, en la medida que sea razonablemente posible, su empaque original, identificación, lote y fecha de vencimiento.
En casos de reclamo por calidad de productos parcialmente consumidos, el cliente debe conservar una porción representativa (muestra suficiente) del producto junto con su empaque original. La aceptación de este tipo de reclamos estará sujeta a la evaluación técnica de A.T.I.C.."


"Sí, es posible. Toda solicitud de devolución, reclamo, reposición o compensación deberá ser presentada por el cliente dentro del plazo de 7 días corridos contados desde la recepción de la mercadería. Además, cuando proceda el retracto, el producto deberá restituirse en buen estado, con sus elementos originales, salvo el deterioro propio de una revisión razonable. Las devoluciones se rigen por la Política de Devoluciones, Reclamos, Reposiciones y Notas de Crédito."
