from sentence_transformers import SentenceTransformer


def sentence_transformer():
    """Loads the model"""
    model_name = "sentence-transformers/sentence-t5-large"
    return SentenceTransformer(model_name)
