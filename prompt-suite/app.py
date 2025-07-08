import streamlit as st
from graph import refine_prompt
import requests

# --- Custom CSS for modern look ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;500&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%);
    }
    .main-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5em;
        letter-spacing: -1px;
    }
    .prompt-card {
        background: #fff;
        border-radius: 1.2em;
        box-shadow: 0 4px 24px 0 rgba(80, 80, 120, 0.08);
        padding: 2em 2em 1.5em 2em;
        margin-top: 1.5em;
        margin-bottom: 1.5em;
    }
    .refined-label {
        font-size: 1.1rem;
        font-weight: 500;
        color: #6366f1;
        margin-bottom: 0.5em;
    }
    .refined-output {
        font-size: 1.15rem;
        color: #22223b;
        background: #f1f5f9;
        border-radius: 0.8em;
        padding: 1.2em;
        box-shadow: 0 2px 8px 0 rgba(80, 80, 120, 0.06);
        margin-bottom: 0.5em;
        font-family: 'Roboto Mono', monospace;
        white-space: pre-wrap;
    }
    .stTextArea textarea {
        background: #f1f5f9;
        border-radius: 0.8em;
        border: 1.5px solid #c7d2fe;
        font-size: 1.1rem;
        padding: 1.2em;
        box-shadow: 0 2px 8px 0 rgba(80, 80, 120, 0.04);
    }
    .stButton button {
        background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
        color: white;
        border: none;
        border-radius: 0.8em;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.7em 2.2em;
        box-shadow: 0 2px 8px 0 rgba(80, 80, 120, 0.08);
        transition: background 0.2s;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #06b6d4 0%, #6366f1 100%);
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header with gradient and logo ---
st.markdown('<div class="main-header">✨ Proompter</div>', unsafe_allow_html=True)

# --- Lottie Animation (optional, fancy) ---
# You can use a Lottie animation from a CDN or local file
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_kyu7xb1v.json"
try:
    import streamlit_lottie
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    lottie_json = load_lottieurl(lottie_url)
    col1, col2 = st.columns([1, 2])
    with col1:
        streamlit_lottie.st_lottie(lottie_json, height=120, speed=1)
    with col2:
        st.markdown("<div style='margin-top: 1.5em; font-size:1.2rem; color:#475569;'>Refine your AI prompts with style and precision.</div>", unsafe_allow_html=True)
except Exception:
    st.info("[Lottie animation requires streamlit-lottie. Install with pip if you want the animation!]")

# --- Prompt Input Card ---
st.markdown('<div class="prompt-card">', unsafe_allow_html=True)
user_prompt = st.text_area("Enter your prompt:", height=120, key="prompt_input")
st.markdown('</div>', unsafe_allow_html=True)

# --- Generate Button ---
generate = st.button("Generate ✨")

if generate:
    if user_prompt.strip():
        with st.spinner("Refining your prompt..."):
            refined = refine_prompt(user_prompt)
        st.markdown('<div class="prompt-card">', unsafe_allow_html=True)
        st.markdown('<div class="refined-label">Refined Prompt:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="refined-output">{refined}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a prompt.")
