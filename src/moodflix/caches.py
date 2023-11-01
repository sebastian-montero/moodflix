import json
import time

import hnswlib
import streamlit as st

from moodflix.transformer import sentence_transformer

TIME = 1


@st.cache_resource(show_spinner="Loading index... 🍿")
def load_index():
    """Loads the index from idx.bin"""
    time.sleep(TIME)
    idx = hnswlib.Index(space="cosine", dim=768)
    idx.load_index("data/idx.bin")
    idx.set_ef(1000)
    return idx


@st.cache_data(show_spinner="Loading movies... 🍿")
def load_data():
    """Loads the movie objects from movie_objs.json"""
    time.sleep(TIME)
    return json.load(open("data/movie_objs.json", "r"))  # pylint: disable=unspecified-encoding


@st.cache_resource(show_spinner="Loading model... 🍿")
def load_model():
    """Loads the model"""
    time.sleep(TIME)
    return sentence_transformer()
