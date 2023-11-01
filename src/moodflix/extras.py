import streamlit as st


def load_extra_html():
    """Loads extra HTML"""
    st.markdown(
        """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    #GithubIcon {
    visibility: hidden;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
