from sentence_transformers import SentenceTransformer

def compare(sent1, sent2):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    sentences = [sent1, sent2]
    embeddings = model.encode(sentences)
    return model.similarity(embeddings, embeddings)

    