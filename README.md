 Tu Tutor de IA Inteligente (RAG) Hecho con Vibe Coding

 https://ai-tutor-rag-mi-primera-ia.streamlit.app/

EduMind es una aplicación web interactiva que transforma cualquier documento PDF en un tutor educativo personalizado. Utilizando una arquitectura **RAG (Retrieval-Augmented Generation)**, la IA procesa el documento, indexa su conocimiento en una base de datos vectorial en memoria y responde preguntas manteniendo el contexto del chat.

Desarrollado de forma eficiente utilizando modelos Open-Source de última generación.

---

## 🛠️ Tecnologías Utilizadas

* **Frontend:** Streamlit
* **Orquestación de IA:** LangChain (Sintaxis moderna LCEL)
* **Cerebro (LLM):** ChatGroq (`llama-3.1-8b-instant`)
* **Base de Datos Vectorial:** FAISS
* **Procesamiento:** PyPDFLoader

---

## 🚀 Características Clave

* **Indexación Instantánea:** Sube cualquier archivo PDF y procesa el texto en chunks optimizados en segundos.
* **Arquitectura 100% Gratuita:** Implementado con el ecosistema de Groq para evitar costos de infraestructura o APIs de pago.
* **Historial de Conversación:** La IA recuerda el contexto completo del hilo del chat educativo.
* **Estructura Ligera:** Diseñado para ejecutarse de forma nativa sin requerir gigabytes de librerías locales de Machine Learning.


## 🧠 Arquitectura del Sistema y Proceso de Desarrollo

Para lograr un sistema eficiente, rápido y 100% gratuito, el proyecto fue diseñado para esquivar la sobrecarga de librerías locales pesadas (como PyTorch) y dependencias de pago, consolidando un flujo de trabajo moderno y optimizado.

### 📦 El Mapa de Dependencias

* **`streamlit`**: Framework encargado de renderizar la interfaz gráfica del chat y el cargador de archivos en tiempo real.
* **`langchain` / `langchain-core`**: Motor de orquestación de IA que gestiona el pipeline mediante la sintaxis moderna **LCEL** (LangChain Expression Language).
* **`langchain-groq`**: Conector oficial para la comunicación con la API de Groq.
* **`chromadb`** ha dado problemas en producción por lo que hemos cambiado a FAISS
* **`pypdf`**: Herramienta encargada de la extracción de texto puro desde el archivo PDF cargado.
* **`python-dotenv`**: Componente de seguridad que inyecta la API Key desde el archivo `.env` sin exponerla en el código fuente.

---

### 🛠️ Flujo de Procesamiento RAG (Paso a Paso)

El ciclo de vida del dato dentro de **EduMind** se compone de las siguientes etapas:

1. **Aislamiento del Entorno:** Configuración de un entorno virtual (`venv`) adaptado de forma dinámica para resolver conflictos de dependencias nativas en entornos Windows con versiones de Python de última generación (Python 3.14).
2. **Extracción y Fragmentación:** Al subir el PDF, `PyPDFLoader` extrae el texto completo. Posteriormente, `RecursiveCharacterTextSplitter` lo segmenta en *chunks* optimizados de 1000 caracteres con un solapamiento (*overlap*) de 200 caracteres para asegurar que no se pierda información en los cortes.
3. **Indexación en Memoria:** Los fragmentos se estructuran matemáticamente mediante un formateador vectorial ligero (`FakeEmbeddings`) de tamaño 384 dimensiones y se almacenan inmediatamente en un índice local de `ChromaDB`, configurando un objeto `retriever` para búsquedas semánticas ultrarrápidas.
4. **Orquestación LCEL (Pipeline de IA):** Se implementó una cadena de ejecución declarativa uniendo las entradas con el operador pipe (`|`):
   * Se recupera el contexto relevante del PDF mediante el input del usuario.
   * Se combina el contexto junto al historial de chat en un `ChatPromptTemplate` adaptado para un rol de tutor educativo.
   * Se procesa todo en el LLM open-source de velocidad extrema `llama-3.1-8b-instant` a través de **Groq**.
   * Se parsea la salida a texto limpio con `StrOutputParser`.
5. **Persistencia del Estado:** Utilizando el `st.session_state` de Streamlit, la aplicación conserva el historial de la conversación en memoria, permitiendo que la IA recuerde el contexto completo del hilo educativo sin necesidad de re-indexar el PDF en cada interacción.
