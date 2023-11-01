from sentence_transformers import SentenceTransformer


def sentence_transformer():
    """Loads the model"""
    model_name = open("model.txt").readlines()[0]
    return SentenceTransformer(model_name)
