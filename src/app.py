import streamlit as st
import pandas as pd
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
    
    # Add CSS for better alignment
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] {
            align-items: center;
            gap: 1rem;
        }
        
        div.stButton > button {
            background-color: rgb(229, 9, 20);
            color: white;
            height: 61px !important;  /* Match selectbox height */
            margin-top: 24px;  /* Match selectbox top margin */
            padding: 0 20px;
            border: none;
            border-radius: 4px;
        }
        
        div.stSelectbox > div {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
        }
        
        div.stSelectbox > label {
            background: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Cache the recommender
    @st.cache_resource
    def load_recommender():
        recommender = MovieRecommender()
        recommender.load_and_prepare_data()
        return recommender
    
    # Load recommender with caching
    recommender = load_recommender()
    
    # Search container with better alignment
    col1, col2 = st.columns([5, 1])  # Adjusted ratio
    
    with col1:
        movie_list = recommender.get_all_movie_titles()
        selected_movie = st.selectbox(
            "Type or select a movie you like:",
            movie_list,
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
    main() 