from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def split_text(text, chunk_size=5):
    sentences = text.split(". ")
    chunks = []

    for i in range(0, len(sentences), chunk_size):
        chunk = ". ".join(sentences[i: i + chunk_size])
        chunks.append(chunk)

    return chunks


def semantic_search(query, text):
    chunks = split_text(text)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks + [query])

    query_vec = vectors[-1]
    chunk_vecs = vectors[:-1]

    scores = np.dot(chunk_vecs, query_vec.T).toarray().flatten()

    top_indices = scores.argsort()[::-1][:3]

    return [chunks[i] for i in top_indices]
