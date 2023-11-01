from sentence_transformers import SentenceTransformer


def sentence_transformer():
    """Loads the model""" ""
    return SentenceTransformer("sentence-transformers/sentence-t5-base")
