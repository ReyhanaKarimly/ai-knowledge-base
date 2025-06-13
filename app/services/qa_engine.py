from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.db.database import get_db_connection
from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')  

def answer_question(question):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT chunk_text FROM chunks")
    rows = cursor.fetchall()
    chunks = [row[0] for row in rows]
    chunks = [c for c in chunks if c.strip()] 


    if not chunks:
        return None

    chunk_embeddings = model.encode(chunks, convert_to_numpy=True)
    question_embedding = model.encode([question], convert_to_numpy=True)

    sims = cosine_similarity(question_embedding, chunk_embeddings)[0]

    best_idx = np.argmax(sims)
    return {"answer": chunks[best_idx], "similarity_score": float(sims[best_idx])}
