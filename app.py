import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)


st.title("🎬 Movie Recommendation System")

st.write(
    "Enter a movie title and get similar movie recommendations "
    "using TF-IDF and cosine similarity."
)


# Get movie list from FastAPI
try:
    response = requests.get(f"{API_URL}/movies")

    if response.status_code == 200:
        movies = response.json()["movies"]
    else:
        movies = []

except requests.exceptions.ConnectionError:
    movies = []
    st.error(
        "FastAPI server is not running. "
        "Please start the FastAPI server first."
    )


movie_title = st.selectbox(
    "Select a Movie",
    movies
)


number_of_movies = st.slider(
    "Number of Recommendations",
    min_value=1,
    max_value=20,
    value=5
)


if st.button("Recommend Movies"):

    payload = {
        "title": movie_title,
        "n": number_of_movies
    }

    try:

        response = requests.post(
            f"{API_URL}/recommend",
            json=payload
        )

        result = response.json()

        if result["status"] == "success":

            st.subheader(
                f"Movies similar to {movie_title}"
            )

            for i, movie in enumerate(
                result["recommendations"],
                start=1
            ):
                st.write(f"**{i}. {movie}**")

        else:

            st.error(result["message"])

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to FastAPI server."
        )