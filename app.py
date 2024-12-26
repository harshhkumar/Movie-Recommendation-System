import streamlit as st
import pandas as pd
import pickle
import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

# Download NLTK data
nltk.download('punkt')

# Page Config
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        padding: 0.5rem 1rem;
        font-size: 16px;
        border-radius: 5px;
    }
    .movie-rec {
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<p class="big-font">🎬 Movie Recommender System</p>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    movies_list = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies_list, similarity

try:
    movies_list, similarity = load_data()
    movies = pd.DataFrame(movies_list)

    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies

    # Main content
    st.write("### Welcome! 👋")
    st.write("Select a movie you like and get personalized recommendations!")
    
    # Movie selection
    selected_movie = st.selectbox(
        'Type or select a movie from the dropdown',
        movies['title'].values
    )

    # Recommendation button
    if st.button('Show Recommendations'):
        with st.spinner('Finding best matches for you...'):
            recommendations = recommend(selected_movie)
            
            st.write("### Based on your selection, you might like:")
            for i, movie in enumerate(recommendations, 1):
                st.markdown(f'<div class="movie-rec">🎬 {i}. {movie}</div>', unsafe_allow_html=True)

except Exception as e:
    st.error("Some error occurred while loading the data. Please check if all required files are present.")
    st.error(f"Error details: {str(e)}")