import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv # Importar esto

# Cargar las variables del archivo .env
load_dotenv()

st.title("🤖 Mi Chatbot con IA")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    # Ahora la clave se lee del sistema, no está escrita aquí
    api_key=os.environ.get("GROQ_API_KEY") 
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                # 2. CAMBIO DE MODELO (Usamos Llama 3 gratis)
                model="llama-3.3-70b-versatile", 
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        except Exception as e:
            st.error(f"Error: {e}")