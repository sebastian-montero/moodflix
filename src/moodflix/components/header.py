import streamlit as st
import base64
from pathlib import Path

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path, size):
    return f"<img src='data:image/png;base64,{img_to_bytes(img_path)}' class='img-fluid' width='{size}'>"

def header(title):
        # st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
        # st.columns([1,3,1])[1].markdown("<h3 style='text-align: center;'>A movie recommendation engine in tune with your mood.</h3>", unsafe_allow_html=True)
        # st.markdown(f"<p style='text-align: center;'>{img_to_html('img/pop.PNG')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'>{img_to_html('img/logo.png', 300)}</p>", unsafe_allow_html=True)
        st.columns([1,3,1])[1].markdown("<h3 style='text-align: center;'>A movie recommendation engine in tune with your mood 🍿</h3>", unsafe_allow_html=True)
        # st.markdown(f"<p style='text-align: center;'>{img_to_html('img/pop.png', 100)}</p>", unsafe_allow_html=True)