import pandas as pd
import ast
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import hnswlib
import json

model = SentenceTransformer('sentence-transformers/sentence-t5-base')

def main():
    movies = pd.read_csv('top_1000_popular_movies_tmdb.csv',lineterminator='\n')

    movie_objs = {}
    all_embeddings = []
    ids = []
    for i in tqdm(movies.to_dict('records')[0:1000]):
        ids.append(i['id'])
        title = i['title']
        genres = ast.literal_eval(i['genres'])
        overview = i['overview']
        tagline = i['tagline']

        movie_objs[i['id']] = {
            "id": i['id'],
            "name":title,
            "release_date": i['release_date'],
            "overview": overview,
            "tagline": tagline,
            "vote_average": i['vote_average'],
            'genres': genres,
        }
        embedding_txt = f"""
        Movie title: {title}
        Movie genres are {genres}
        Overview: {overview}. {tagline}
        """ 
        embeddings = model.encode([embedding_txt])[0]
        all_embeddings.append(embeddings)

    p = hnswlib.Index(space = 'cosine', dim = len(all_embeddings[0])) # possible options are l2, cosine or ip
    p.init_index(max_elements = len(ids), ef_construction = 200, M = 16)
    p.add_items(all_embeddings, ids)
    p.set_ef(100) 
    p.save_index("idx.bin")

    with open('movie_objs.json', 'w') as f:
        json.dump(movie_objs, f)

if __name__ == '__main__':
    main()