import streamlit as st
import google.generativeai as genai
import base64

st.set_page_config(page_title="Kashif's Elite AI", layout="wide")

# Background logic (wahi purani)
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg(bin_file):
    try:
        bin_str = get_base64(bin_file)
        st.markdown(f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                              url("data:image/jpeg;base64,{bin_str}");
            background-size: cover; background-position: center; background-attachment: fixed;
        }}
        .stChatMessage {{ background: rgba(10,10,10,0.85) !important; border: 1px solid #00f2fe !important; border-radius: 15px !important; }}
        </style>
        ''', unsafe_allow_html=True)
    except: pass

set_bg('kashif_bg.jpeg')

# --- SECURE API SETUP ---
# Ye line aapke Streamlit Secrets se key uthayegi
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key missing! Please add GOOGLE_API_KEY in Streamlit Secrets.")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.write(m["content"])

if p := st.chat_input("Master Kashif, secure mode active..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"): st.write(p)
    
    with st.chat_message("assistant"):
        try:
            r = model.generate_content(f"Act as Kashif's personal AI: {p}")
            st.write(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
        except Exception as e:
            st.error(f"Error: {e}")
