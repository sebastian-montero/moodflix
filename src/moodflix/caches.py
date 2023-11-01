import json

import hnswlib
import streamlit as st

from moodflix.transformer import sentence_transformer


@st.cache_resource(show_spinner="Loading index... 🍿")
def load_index():
    """Loads the index from idx.bin"""
    idx = hnswlib.Index(space="cosine", dim=768)
    idx.load_index("data/idx.bin")
    idx.set_ef(1000)
    return idx


@st.cache_data(show_spinner="Loading movies... 🍿")
def load_data():
    """Loads the movie objects from movie_objs.json"""
    return json.load(open("data/movie_objs.json", "r"))  # pylint: disable=unspecified-encoding


@st.cache_resource(show_spinner="Loading model... 🍿")
def load_model():
    """Loads the model"""
    return sentence_transformer()
