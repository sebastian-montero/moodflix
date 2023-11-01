import ast
import json

import hnswlib
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

MODEL = SentenceTransformer(open("model.txt").readlines()[0])


def main():
    """Builds the index and saves it to idx.bin and movie_objs.json"""
    movies = pd.read_csv("top_1000_popular_movies_tmdb.csv", lineterminator="\n")

    movie_objs = {}
    all_embeddings = []
    ids = []
    for i in tqdm(movies.to_dict("records")):
        ids.append(i["id"])
        title = i["title"]
        genres = ast.literal_eval(i["genres"])
        overview = i["overview"]
        tagline = i["tagline"]
        original_language = i["original_language"]

        movie_objs[i["id"]] = {
            "id": i["id"],
            "name": title,
            "release_date": i["release_date"],
            "overview": overview,
            "tagline": tagline,
            "vote_average": i["vote_average"],
            "genres": genres,
            "original_language": original_language,
        }
        embedding_txt = f"""
        Movie genres are {genres}
        Overview: {overview}. {tagline}
        Movie Language: {original_language}
        """
        embeddings = MODEL.encode([embedding_txt])[0]
        all_embeddings.append(embeddings)

    p = hnswlib.Index(space="cosine", dim=len(all_embeddings[0]))  # pylint: disable=invalid-name
    p.init_index(max_elements=len(ids), ef_construction=1000, M=50)
    p.add_items(all_embeddings, ids)
    p.save_index("data/idx.bin")

    with open("data/movie_objs.json", "w") as f:  # pylint: disable=invalid-name, unspecified-encoding
        json.dump(movie_objs, f)


if __name__ == "__main__":
    main()
