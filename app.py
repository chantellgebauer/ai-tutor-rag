import streamlit as st
import os
from backend import AITutor

st.set_page_config(page_title="EduMind: Tu Tutor de IA", page_icon="🤖")
st.title("🤖 EduMind: Tutor de IA Inteligente")
st.write("Sube un PDF y chatea con él. ¡La IA recordará todo el contexto!")

# Inicializar la sesión del Tutor y el Historial en Streamlit
if "tutor" not in st.session_state:
    st.session_state.tutor = AITutor()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_procesado" not in st.session_state:
    st.session_state.pdf_procesado = False

# Sidebar para subir archivos
with st.sidebar:
    st.header("1. Carga tu conocimiento")
    uploaded_file = st.file_uploader("Sube un archivo PDF", type=["pdf"])
    
    if uploaded_file and not st.session_state.pdf_procesado:
        with st.spinner("Procesando y vectorizando el PDF..."):
            # Guardar archivo temporalmente
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Ingestar en el backend
            st.session_state.tutor.ingest_pdf(temp_path)
            st.session_state.pdf_procesado = True
            
            # Eliminar archivo temporal
            os.remove(temp_path)
            st.success("¡PDF indexado con éxito!")

# Área de Chat
st.header("2. Chatea con el Tutor")

# Mostrar mensajes anteriores guardados en el historial
for message in st.session_state.chat_history:
    role = "user" if message.__class__.__name__ == "HumanMessage" else "assistant"
    with st.chat_message(role):
        st.write(message.content)

# Entrada del usuario
if user_query := st.chat_input("¿Qué deseas aprender hoy de este documento?"):
    if not st.session_state.pdf_procesado:
        st.warning("Por favor, sube un archivo PDF primero en la barra lateral.")
    else:
        # 1. Mostrar de inmediato la pregunta del usuario en la pantalla
        with st.chat_message("user"):
            st.write(user_query)
        
        # 2. Obtener la cadena LCEL desde nuestro backend
        rag_chain = st.session_state.tutor.get_rag_chain()
        
        # 3. Generar la respuesta del asistente con animación de carga
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                answer = rag_chain.invoke({
                    "input": user_query,
                    "chat_history": st.session_state.chat_history
                })
                st.write(answer)
        
        # 4. Guardar ambas interacciones en el historial usando el formato de LangChain
        from langchain_core.messages import HumanMessage, AIMessage
        st.session_state.chat_history.extend([
            HumanMessage(content=user_query),
            AIMessage(content=answer)
        ])