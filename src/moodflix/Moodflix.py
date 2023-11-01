import streamlit as st
from moodflix.components.header import header, img_to_html
import random
from sentence_transformers import SentenceTransformer
import hnswlib
import json 
import logging

def init_logging():
    logger = logging.getLogger("custom")
    if logger.handlers: 
        return
    logger.propagate = False
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

LOGGER = logging.getLogger("custom")

st.set_page_config(page_title="Moodflix", page_icon="🍿", layout="centered", menu_items={
        'Report a bug': "https://github.com/sebastian-montero/moodflix/issues",
        'About': "Built by Sebastian Montero to try and stop endless discussions about what movie to watch."
    })

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
    unsafe_allow_html=True
)


MOODS = [
    "cold autumn day, seeking a film to warm the heart with my loved ones",
    "bright summer morning, in the mood for an adventure flick",
    "rainy afternoon, longing for a deep mystery or drama",
    "lively spring evening, craving a dance or musical film",
    "quiet winter night, ready for a classic or a heartfelt story",
    "sunny day, desiring a light-hearted comedy or romance",
    "misty dawn, setting the scene for a fantasy or epic tale",
    "back from the city, feeling a noir or thriller vibe",
    "lazy sunday afternoon, wanting a family or animated movie",
    "clear starry night, up for a sci-fi or otherworldly journey",
    "feeling the need for some old-school classics",
    "hoping for heartwarming tales with family",
    "seeking an edge-of-the-seat thriller night",
    "craving feel-good comedies and chuckles",
    "desiring epic adventures with grand battles",
    "looking for tales of star-crossed lovers",
    "intrigued by mysteries and detective sagas",
    "yearning for musicals with catchy tunes",
    "eager for animation and childhood wonders",
    "wanting a dive into deep, thought-provoking drama",
    "hankering for spine-chilling horror stories",
    "in the mood for travel and scenic world explorations"
]
ABOUT = """# About
Ever had one of those days where you're thinking, "I'm feeling so blue, a rom-com is just the thing," or "I'm on top of the world, bring on the action"? Well, Moodflix is here to save your movie night. 
Get tailored recommendations based on your current feels. Say goodbye to endless scrolling and hello to the ideal movie match. 
Whether you're in the mood for some drama, thrills, or romance, Moodflix is your new best cinema friend. Let's get those movie vibes going!

## Inspiration
The idea behind Moodflix was sparked by the [Viberary](http://viberary.pizza) website, created by [@vboykis](https://twitter.com/vboykis). 
Viberary uses a similar approach of suggesting books based on the user's vibes. Seeing its potential, I felt a similar concept could be applied to movies. 
So, taking a cue from Viberary, Moodflix was born, aiming to match movies with moods for a tailored viewing experience.

## The Data
The dataset provides metadata about the top 10,000 movies from **The Movie Database (TMDB)**. Encompassing a diverse set of attributes, details such as movie titles, release dates, runtime, genres, production companies, budget, and revenue are included. Key attributes highlighted are the unique identifier (`id`), movie title (`title`), associated genres (`genres`), the original production language (`original_language`), average user rating (`vote_average`), a popularity score based on user engagement (`popularity`), a brief synopsis (`overview`), the production budget in USD (`budget`), the movie's total revenue in USD (`revenue`), the movie's duration in minutes (`runtime`), and its promotional tagline (`tagline`). This data, sourced from TMDB, was retrieved from Kaggle and has been processed for enhanced quality and usability.

**Source:** [Top 10000 popular Movies TMDB](#https://www.kaggle.com/datasets/ursmaheshj/top-10000-popular-movies-tmdb-05-2023)

## Indexing the movies
The ingestion pipelines processes the data and prepares it for similarity-based recommendations. 
It utilizes the `sentence-t5-base` model from SentenceTransformers to convert textual information from movie titles, genres, overviews, and taglines into numerical embeddings. 
These embeddings serve as condensed representations, capturing the content nuances of each film, facilitating efficient similarity comparisons.

To enable rapid similarity searches, the we use the `hnswlib` library to create a search index based on the HNSW (Hierarchical Navigable Small World) algorithm. 
This indexing approach ensures fast and accurate retrieval, making it suitable for real-time movie recommendations. 
Once processed, the structured movie details are stored, and the search index is saved, paving the way for subsequent recommendation operations.

## Searching for similar movies
Upon receiving the user's mood input, we encode the text into a numerical vector embedding. 
This embedding is essentially a dense vector that captures the essence of the user's mood in a format conducive to similarity comparisons. 
The generated embedding is then used as a search query in the `hnswlib` index to perform a k-nearest neighbors search. 
This search retrieves movies with embeddings that are most similar to the mood embedding, ensuring that the movies align closely with the user's specified mood.
"""



@st.cache_resource
def load_index():
    idx = hnswlib.Index(space='cosine', dim=768)
    idx.load_index("idx.bin")
    idx.set_ef(1000)
    return idx

@st.cache_data
def load_data():
    return json.load(open("movie_objs.json", "r"))

@st.cache_resource
def load_model():
    return SentenceTransformer('sentence-transformers/sentence-t5-base')

INDEX = load_index()
MOVIE_DATA = load_data()
MODEL = load_model()

class Main:
    @staticmethod
    def render():
        header("Moodflix")

        with st.sidebar:
            st.markdown(f"<p style='text-align: center;'>{img_to_html('img/pop.png', 200)}</p>", unsafe_allow_html=True)
            st.markdown(ABOUT)
            st.markdown("## Extras")
            with st.expander("Additional parameters", expanded=False):
                if "k" not in st.session_state:
                    st.session_state.k = 50
                st.session_state.k = st.number_input("Approximate nearest neighbours to search", min_value=1, max_value=200, value=st.session_state.k, step=1)

        c1, c2 = st.columns([9, 1], gap="small")
        with c1:
            st.markdown("#### What do you feel like?")
        with c2:
            if "mood" not in st.session_state:
                st.session_state.mood = ""
                
            if st.session_state.mood == "":
                random_mood = ""
            else:
                random_mood = st.session_state.mood
            if st.button("🎲"):
                random_mood = random.choice(MOODS)

        st.session_state.mood = st.text_area("enter_mood", label_visibility="collapsed", value=random_mood, placeholder="click 🎲 to get a random mood", height=50)

        if st.session_state.mood != "":
            LOGGER.info(f"user prompt: {st.session_state.mood}")
            with st.spinner("🍿"):
                embeddings = MODEL.encode([st.session_state['mood']])[0]
                labels, distances = INDEX.knn_query(embeddings, k=st.session_state.k)
                all_genres = [MOVIE_DATA[str(i)]["genres"] for i in labels[0]]
                all_genres = [item for sublist in all_genres for item in sublist]
        
                with st.expander(f"Filters", expanded=False):
                    genre_filter = st.multiselect("Genres", options=list(set(all_genres)), default=list(set(all_genres)))
                    genre_excluded = st.toggle('Hard exclude', value=True)
                    ranking_filter = st.slider("Rating", min_value=0, max_value=10, value=(0,10), step=1)

                st.markdown("#### Here's what we recommend:")
                for label, d in zip(labels[0], distances[0]):
                    if isinstance(MOVIE_DATA[str(label)]["overview"],str):
                        d = int(d*100)/100
                        movie_data = MOVIE_DATA[str(label)]
                        title = movie_data["name"]
                        genres = ", ".join(movie_data["genres"])
                        overview = movie_data["overview"]
                        vote_average = float(movie_data["vote_average"])
                        release_date = int(movie_data["release_date"][0:4]) if isinstance(movie_data["release_date"], str) else "N/A"

                        len_movie_genre = len([x for x in movie_data["genres"] if x in all_genres])
                        len_filtered_genres = len([x for x in movie_data["genres"] if x in genre_filter])

                        genre_bool = len_filtered_genres == len_movie_genre if genre_excluded else len_filtered_genres > 0

                        if vote_average >= ranking_filter[0] and vote_average <= ranking_filter[1]:
                                if genre_bool:
                                    st.markdown(f"##### {title} ({release_date})")
                                    mov1, mov2 = st.columns([3,1])
                                    with mov1:
                                        st.markdown(f"**Plot synopsis:** {overview}")
                                    with mov2:
                                        st.markdown(f"""**Rating:** {vote_average}/10  \n**Genres:** {genres}""")
                                    st.markdown("")
        st.markdown("**Created by [Sebastian Montero](http://www.sebastianmontero.com/)**")


if __name__ == "__main__":
    Main.render()