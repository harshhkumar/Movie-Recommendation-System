import streamlit as st
import pandas as pd
<<<<<<< HEAD
import pickle
import requests
import os
import ast

# Load data function
def load_data():
    try:
        # Check if pickle files exist, if not create them
        if not (os.path.exists('data/movies_dict.pkl') and os.path.exists('data/similarity.pkl')):
            from movie_recommender import create_similarity_matrix
            movies_dict, _ = create_similarity_matrix()
        else:
            movies_dict = pickle.load(open('data/movies_dict.pkl', 'rb'))
        
        movies_df = pd.DataFrame(movies_dict)
        return movies_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

class MovieRecommender:
    def __init__(self, movies_df):
        self.movies_df = movies_df
        try:
            if not os.path.exists('data/similarity.pkl'):
                from movie_recommender import create_similarity_matrix
                _, self.similarity = create_similarity_matrix()
            else:
                self.similarity = pickle.load(open('data/similarity.pkl', 'rb'))
        except Exception as e:
            st.error(f"Error loading similarity matrix: {str(e)}")
            self.similarity = None

    def get_recommendations(self, movie_name):
        try:
            movie_index = self.movies_df[self.movies_df['title'] == movie_name].index[0]
            distances = self.similarity[movie_index]
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
            
            recommended_movies = []
            for i in movies_list:
                movie_id = self.movies_df.iloc[i[0]].id
                recommended_movies.append({
                    'id': movie_id,
                    'title': self.movies_df.iloc[i[0]].title,
                    'vote_average': self.movies_df.iloc[i[0]].vote_average,
                    'release_date': self.movies_df.iloc[i[0]].release_date,
                    'cast': self.movies_df.iloc[i[0]].cast,
                    'overview': self.movies_df.iloc[i[0]].overview
                })
            
            return pd.DataFrame(recommended_movies)
        except Exception as e:
            st.error(f"Error getting recommendations: {str(e)}")
            return None

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8"
        response = requests.get(url)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return None

def get_movie_details(movie_df_row):
    """Get complete movie details including poster and trailer"""
    try:
        movie_id = movie_df_row['id']
        # Get movie details and videos
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&append_to_response=credits,videos"
        response = requests.get(url)
        data = response.json()
        
        # Get trailer
        trailer = None
        for video in data.get('videos', {}).get('results', []):
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                trailer = f"https://www.youtube.com/watch?v={video['key']}"
                break
        
        poster_path = data.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        
        genres = ", ".join([genre['name'] for genre in data.get('genres', [])])
        cast = ", ".join([cast['name'] for cast in data.get('credits', {}).get('cast', [])[:5]])
        
        return {
            'poster_url': poster_url,
            'title': movie_df_row['title'],
            'rating': movie_df_row['vote_average'],
            'release_date': movie_df_row['release_date'],
            'genres': genres,
            'cast': cast,
            'overview': movie_df_row['overview'],
            'trailer_url': trailer
        }
    except Exception as e:
        st.error(f"Error fetching movie details: {str(e)}")
        return None

def main():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
                        url('https://wallpaperaccess.com/full/3658597.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
=======
import requests
from movie_recommender import MovieRecommender

# TMDB API Configuration
TMDB_API_KEY = "3d0b29c95f6d3b53fb6fbecbbb3ea1c6"
TMDB_API_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDBiMjljOTVmNmQzYjUzZmI2ZmJlY2JiYjNlYTFjNiIsInN1YiI6IjY1OWQ2NjQ3Y2E0ZjY3MDFmZDVkZjEwYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dNZI1WkeIVJ1Nx2AoCXDWFn-yUiCELHVxG7823HFIzQ"

# Page config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Netflix style
st.markdown("""
    <style>
    .movie-container {
        display: flex;
        gap: 20px;
        margin: 20px 0;
    }
    .movie-poster-container {
        flex: 0 0 300px;
    }
    .movie-poster {
        width: 100%;
        border-radius: 10px;
    }
    .movie-details {
        flex: 1;
    }
    .trailer-btn {
        background: rgba(229, 9, 20, 0.1);
        color: white;
        padding: 8px 20px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 500;
        font-size: 14px;
        display: inline-flex;
        align-items: center;
        border: 1px solid rgba(229, 9, 20, 0.6);
        transition: all 0.2s ease;
    }
    .trailer-btn:hover {
        background: rgba(229, 9, 20, 0.2);
        border-color: rgba(229, 9, 20, 0.8);
        text-decoration: none;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def get_movie_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY}
        )
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        return None
    except:
        return None

def get_movie_trailer(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos",
            params={"api_key": TMDB_API_KEY}
        )
        data = response.json()
        for video in data.get('results', []):
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                return f"https://www.youtube.com/watch?v={video['key']}"
        return None
    except:
        return None

def main():
    st.title("🎬 Movie Recommendation System")
    
    # Add CSS for perfect vertical alignment
    st.markdown("""
        <style>
        /* Container styling */
        .search-container {
            display: flex;
            align-items: center;
            padding: 1rem 0;
        }
        
        /* Remove extra padding/margin from selectbox */
        div[data-testid="stSelectbox"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        
        /* Button styling */
        div.stButton > button {
            margin-top: 0 !important;
            height: 42px !important;
            background-color: rgb(229, 9, 20);
            color: white;
            border: none;
        }
        
        /* Label styling */
        .search-label {
            margin-bottom: 0 !important;
>>>>>>> 5ebf180189222cc4bbc525e4f2297c612ef13038
        }
        </style>
    """, unsafe_allow_html=True)
    
<<<<<<< HEAD
    st.title('Movie Recommender System')
    
    # Load data
    movies_df = load_data()
    if movies_df is None:
        st.error("Failed to load movie data. Please check your data files.")
        return
        
    recommender = MovieRecommender(movies_df)
    
    # Movie selection
    selected_movie = st.selectbox(
        'Select or type a movie name',
        options=movies_df['title'].values,
        index=None,
        placeholder="Choose a movie..."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        search_movie = st.button('Search Movie')
    with col2:
        show_rec = st.button('Show Recommendations')
    
    # Movie details
    if search_movie and selected_movie:
        with st.spinner('Loading movie details...'):
            movie_row = movies_df[movies_df['title'] == selected_movie].iloc[0]
            movie_details = get_movie_details(movie_row)
            
            if movie_details:
                # Create two columns for poster and details
                poster_col, details_col = st.columns([1, 2])
                
                with poster_col:
                    if movie_details['poster_url']:
                        st.image(movie_details['poster_url'])
                    else:
                        st.markdown("🎬 No poster available")
                
                with details_col:
                    # Title and trailer button in same line
                    title_col, trailer_col = st.columns([3, 1])
                    with title_col:
                        st.header(movie_details['title'])
                    with trailer_col:
                        if movie_details['trailer_url']:
                            st.markdown(f"[![Watch Trailer](https://img.shields.io/badge/Watch-Trailer-red?style=for-the-badge&logo=youtube)]({movie_details['trailer_url']})")
                    
                    st.markdown(f"**Rating:** ⭐ {movie_details['rating']:.1f}/10")
                    st.markdown(f"**Release Date:** {movie_details['release_date']}")
                    st.markdown(f"**Genres:** {movie_details['genres']}")
                    st.markdown(f"**Cast:** {movie_details['cast']}")
                    st.markdown(f"**Overview:** {movie_details['overview']}")

    # Recommendations
    if show_rec and selected_movie:
        with st.spinner('Loading recommendations...'):
            recommendations = recommender.get_recommendations(selected_movie)
            
            if recommendations is not None and not recommendations.empty:
                st.subheader("You might also like:")
                cols = st.columns(5)
                
                for idx, (_, movie) in enumerate(recommendations.iterrows()):
                    with cols[idx]:
                        poster_url = fetch_poster(movie['id'])
                        if poster_url:
                            st.image(poster_url)
                        st.markdown(f"**{movie['title']}**")
                        st.markdown(f"⭐ {movie['vote_average']:.1f}/10")

if __name__ == '__main__':
=======
    # Cache the recommender
    @st.cache_resource
    def load_recommender():
        recommender = MovieRecommender()
        recommender.load_and_prepare_data()
        return recommender
    
    # Load recommender with caching
    recommender = load_recommender()
    
    # Search container with perfect alignment
    st.markdown('<p class="search-label">Type or select a movie you like:</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        movie_list = recommender.get_all_movie_titles()
        selected_movie = st.selectbox(
            label="Select a movie",
            options=movie_list,
            label_visibility="collapsed",
            key="movie_select"
        )
    
    with col2:
        show_rec = st.button(
            'Show Recommendations', 
            use_container_width=True,
            key="rec_button"
        )

    # Cache movie details
    @st.cache_data
    def get_cached_movie_details(movie_id):
        return get_movie_poster(movie_id), get_movie_trailer(movie_id)
    
    # Show selected movie details
    if selected_movie and not show_rec:
        movie_details = recommender.get_movie_details(selected_movie)
        poster_url, trailer_url = get_cached_movie_details(movie_details['id'])
        
        st.markdown(f"""
            <div class="movie-container">
                <div class="movie-poster-container">
                    <img src="{poster_url}" class="movie-poster">
                </div>
                <div class="movie-details">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                        <h2 style="margin: 0;">{movie_details['title']}</h2>
                        <a href="{trailer_url if trailer_url else '#'}" target="_blank" class="trailer-btn">Watch Trailer</a>
                    </div>
                    <p><strong>Rating:</strong> ⭐ {movie_details['vote_average']}/10</p>
                    <p><strong>Release Date:</strong> {movie_details['release_date'][:4]}</p>
                    <p><strong>Genres:</strong> {movie_details['genres']}</p>
                    <p><strong>Cast:</strong> {movie_details['cast']}</p>
                    <p><strong>Overview:</strong><br>{movie_details['overview']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Show recommendations with optimization
    if show_rec and selected_movie:
        with st.spinner('Finding similar movies...'):
            recommendations = recommender.get_recommendations(selected_movie)
            if recommendations is not None:
                st.subheader("You might also like:")
                
                # Pre-fetch all posters
                posters = {}
                for _, movie in recommendations.iterrows():
                    poster_url, _ = get_cached_movie_details(movie['id'])
                    posters[movie['id']] = poster_url
                
                # Display recommendations
                cols = st.columns(5)
                for idx, (col, (_, movie)) in enumerate(zip(cols, recommendations.iterrows())):
                    with col:
                        if posters.get(movie['id']):
                            st.image(posters[movie['id']], use_container_width=True)
                        st.markdown(f"**{movie['title']}**")
                        st.markdown(f"⭐ {movie['vote_average']:.1f}/10")
                        
                        if st.button(f"More Info", key=f"more_info_{idx}"):
                            st.write(f"**Release:** {movie['release_date'][:4]}")
                            st.write(f"**Cast:** {movie['cast'][:100]}...")
                            st.write(movie['overview'][:200] + "...")

if __name__ == "__main__":
>>>>>>> 5ebf180189222cc4bbc525e4f2297c612ef13038
    main() 