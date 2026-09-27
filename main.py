from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI(
    title="Movie Recommendation API",
    description="Content-Based Movie Recommendation System",
    version="1.0"
)


# Load saved files
tfidf_matrix = pickle.load(
    open("models/tfidf_matrix.pkl", "rb")
)

indices = pickle.load(
    open("models/indices.pkl", "rb")
)

df = pickle.load(
    open("models/df.pkl", "rb")
)

tfidf = pickle.load(
    open("models/tfidf.pkl", "rb")
)


class MovieRequest(BaseModel):
    title: str
    n: int = 10


@app.get("/")
def home():
    return {
        "message": "Movie Recommendation API is running"
    }


@app.get("/movies")
def get_movies():
    return {
        "movies": df["title"].tolist()
    }


@app.post("/recommend")
def recommend_movies(request: MovieRequest):

    title = request.title

    if title not in indices:
        return {
            "status": "error",
            "message": "Movie not found"
        }

    idx = indices[title]

    similarity_scores = cosine_similarity(
        tfidf_matrix[idx],
        tfidf_matrix
    ).flatten()

    similar_indices = similarity_scores.argsort()[::-1][1:request.n + 1]

    recommendations = df.iloc[similar_indices]["title"].tolist()

    return {
        "status": "success",
        "movie": title,
        "recommendations": recommendations
    }