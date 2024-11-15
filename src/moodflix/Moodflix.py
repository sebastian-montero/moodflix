import random
from dataclasses import dataclass

import streamlit as st

from moodflix.caches import load_data, load_index, load_model
from moodflix.extras import load_extra_html
from moodflix.text import ABOUT, MOODS
from moodflix.utils import center_html, img_to_html

st.set_page_config(page_title="Moodflix", page_icon="🍿", layout="centered")

load_extra_html()


@dataclass
class Movie:
    """Movie class"""

    id: int  # pylint: disable=invalid-name
    name: str
    release_date: str
    overview: str
    tagline: str
    vote_average: float
    genres: list
    original_language: str


class Main:
    """Main class for the app"""

    @staticmethod
    def render_header():
        """Renders the header"""
        st.markdown(center_html("p", img_to_html("im_logo.png", 300)), unsafe_allow_html=True)
        st.columns([1, 3, 1])[1].markdown(center_html("h3", "A movie recommendation engine in tune with your mood."), unsafe_allow_html=True)

    @staticmethod
    def render_sidebar():
        """Renders the sidebar"""
        with st.sidebar:
            st.markdown(center_html("p", img_to_html("im_pop.png", 125)), unsafe_allow_html=True)
            st.markdown(ABOUT)
            with st.expander("Additional parameters", expanded=False):
                if "k" not in st.session_state:
                    st.session_state.k = 50
                st.session_state.k = st.number_input("Approximate nearest neighbours to search", min_value=5, max_value=200, value=st.session_state.k, step=10)

    # pylint: disable=too-many-locals,too-many-statements
    @staticmethod
    def render():
        """Renders the app"""

        index = load_index()
        movies = load_data()
        model = load_model()

        column1, column2 = st.columns([9, 1], gap="small")
        with column1:
            st.markdown("#### What do you feel like?")
        with column2:
            if "mood" not in st.session_state:
                st.session_state.mood = ""

            if st.session_state.mood == "":
                random_mood = ""
            else:
                random_mood = st.session_state.mood
            if st.button("🎲"):
                random_mood = random.choice(MOODS)

        st.session_state.mood = st.text_input(
            "mood",
            label_visibility="collapsed",
            value=random_mood,
            placeholder="click 🎲 to get random moods",
        )

        if st.session_state.mood != "":
            with st.spinner("🍿"):
                embeddings = model.encode([st.session_state["mood"]])[0]
                movie_ids, _ = index.knn_query(embeddings, k=st.session_state.k)
                movie_ids = [str(i) for i in movie_ids[0]]

                all_genres = {j for s in [movies[i]["genres"] for i in movie_ids] for j in s}

                with st.expander("Filters", expanded=False):
                    ranking_filter = st.slider("Rating", min_value=0, max_value=10, value=(0, 10))
                    genre_filter = st.multiselect("Genres", options=all_genres, default=all_genres)
                    genre_excluded = st.toggle("Exclude", value=True)

                st.markdown("#### Here's what we recommend:")
                st.markdown("")
                for movie_id in movie_ids:
                    movie = Movie(**movies[str(movie_id)])

                    if isinstance(movie.overview, str):
                        title = movie.name
                        overview = movie.overview
                        vote_average = movie.vote_average
                        language = movie.original_language
                        release_date = int(movie.release_date[0:4]) if isinstance(movie.release_date, str) else "N/A"

                        len_movie_genre = len([x for x in movie.genres if x in all_genres])
                        len_filtered_genres = len([x for x in movie.genres if x in genre_filter])

                        genre_bool = len_filtered_genres == len_movie_genre if genre_excluded else len_filtered_genres > 0

                        if (ranking_filter[0] <= vote_average <= ranking_filter[1]) and genre_bool:
                            st.markdown(f"##### 🍿  {title} ({release_date})")
                            movie_column1, movie_column2 = st.columns([3, 1.5])
                            with movie_column1:
                                st.markdown(f"**Plot synopsis:** {overview}")
                            with movie_column2:
                                genres_str = ", ".join(movie.genres)
                                st.markdown(f"""**Rating:** {vote_average}/10  \n**Genres:** {genres_str}  \n**Language:** {language}""")
                            st.divider()

    @staticmethod
    def render_footer():
        """Renders the footer"""
        st.markdown("")
        st.markdown(center_html("p", "Created by <a href=https://seb.incendia.dev/>0x736D70</a>"), unsafe_allow_html=True)


if __name__ == "__main__":
    Main.render_header()
    Main.render_sidebar()
    Main.render()
    Main.render_footer()
