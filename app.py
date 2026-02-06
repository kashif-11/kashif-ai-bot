import streamlit as st
import google.generativeai as genai
import base64

# --- 1. Page Config ---
st.set_page_config(page_title="Kashif's Elite AI", page_icon="🤖", layout="wide")

# --- 2. Perfect Background Adjustment ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_perfect_bg(bin_file):
    try:
        bin_str = get_base64(bin_file)
        st.markdown(f'''
        <style>
        .stApp {{
            /* This ensures the image covers the whole screen perfectly */
            background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                              url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center 20%; /* Adjusted to show your face/upper body */
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        
        /* Neon Floating Marquee */
        .marquee-container {{
            width: 100%; overflow: hidden; border: 2px solid #00f2fe;
            border-radius: 15px; background: rgba(0, 0, 0, 0.9);
            padding: 12px 0; margin-bottom: 25px; box-shadow: 0 0 20px #00f2fe;
        }}
        .marquee-text {{
            display: inline-block; white-space: nowrap;
            animation: marquee 15s linear infinite;
            color: #00f2fe; font-size: 26px; font-weight: bold;
            text-shadow: 0 0 10px #00f2fe;
        }}
        @keyframes marquee {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

        /* Clean Chat Bubbles */
        .stChatMessage {{ 
            background: rgba(10, 10, 10, 0.85) !important; 
            border: 1px solid rgba(0, 242, 254, 0.4) !important; 
            border-radius: 20px !important;
            color: white !important;
        }}
        </style>
        <div class="marquee-container"><div class="marquee-text">👑 Developed by Kashif Iqbal — Your Smart Assistant is Ready 👑</div></div>
        ''', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Image Error: Make sure 'kashif_bg.jpeg' is in the folder.")

# Apply the background
set_perfect_bg('kashif_bg.jpeg')

# --- 3. API Setup (Fixed for your New Key) ---
API_KEY = "AIzaSyB6oTez-0yuTwEbioy7IOWMJqQ1RvwUC1g"
genai.configure(api_key=API_KEY)

# Using the most compatible way to find a model
@st.cache_resource
def load_model():
    try:
        # This list picks the first model your key is allowed to use
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return None

model = load_model()

# --- 4. Sidebar ---
with st.sidebar:
    st.title("🤖 Kashif's AI")
    if model:
        st.success("✅ System Online")
    else:
        st.error("❌ Connecting...")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Master Kashif, how can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                response = model.generate_content(f"You are Kashif's AI assistant. {prompt}")
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Still connecting to Google. Please wait 1 minute.")