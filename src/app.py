import streamlit as st
import pandas as pd
import requests
from movie_recommender import MovieRecommender

# TMDB API Configuration
TMDB_API_KEY = "3d0b29c95f6d3b53fb6fbecbbb3ea1c6"
TMDB_API_READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDBiMjljOTVmNmQzYjUzZmI2ZmJlY2JiYjNlYTFjNiIsIm5iZiI6MTczNTQ5NTQ2MC42MjQsInN1YiI6IjY3NzE4ZjI0MWYyYzVkOTMwMTkyYTViMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.xQHWAP7kwXX4z-tQsHWsvh1NY0ahXPNRvXiG5we_GEI"

# Page config
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .movie-container {
        background-color: #1a1c24;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        display: flex;
        gap: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Poster container styling */
    .movie-poster-container {
        position: relative;
        width: 220px;
        height: 330px;
        overflow: hidden;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    .movie-poster {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .movie-poster-container:hover .movie-poster {
        transform: scale(1.05);
    }
    
    /* Trailer button styling */
    .trailer-button {
        position: absolute;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 10px;
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
        backdrop-filter: blur(5px);
    }
    
    .trailer-btn:hover {
        background: rgba(229, 9, 20, 0.2);
        border-color: rgba(229, 9, 20, 0.8);
        text-decoration: none;
        color: white;
    }
    
    .trailer-btn::before {
        content: "▶";
        margin-right: 6px;
        font-size: 12px;
    }
    
    /* Recommendation cards styling */
    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px;
        padding: 20px 0;
    }
    
    .recommendation-card {
        background: #1a1c24;
        border-radius: 12px;
        overflow: hidden;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .recommendation-card:hover {
        transform: translateY(-5px);
    }
    
    .recommendation-poster {
        width: 100%;
        height: 300px;
        object-fit: cover;
    }
    
    .recommendation-content {
        padding: 15px;
    }
    
    /* More details button styling */
    .more-details-button {
        background: linear-gradient(135deg, #2C3E50, #3498DB);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.9em;
        transition: all 0.3s ease;
        display: inline-block;
        margin-top: 10px;
    }
    
    .more-details-button:hover {
        background: linear-gradient(135deg, #3498DB, #2C3E50);
        transform: scale(1.05);
    }
    
    /* Movie details styling */
    .movie-details {
        flex: 1;
        padding: 10px;
    }
    
    .movie-title {
        font-size: 2em;
        margin-bottom: 15px;
        color: #ffffff;
    }
    
    .movie-info {
        background: rgba(255,255,255,0.05);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    
    .movie-overview {
        line-height: 1.6;
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
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
    except Exception as e:
        st.error(f"Error fetching poster: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_movie_trailer(movie_id):
    headers = {
        "Authorization": f"Bearer {TMDB_API_READ_ACCESS_TOKEN}",
        "accept": "application/json"
    }
    
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/videos",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        videos = data.get('results', [])
        trailers = [v for v in videos if v['type'].lower() == 'trailer' 
                   and v['site'].lower() == 'youtube'
                   and v.get('official', True)]
        
        if trailers:
            return f"https://www.youtube.com/watch?v={trailers[0]['key']}"
    return None

def main():
    st.title("🎬 Movie Recommendation System")
    
    # Load recommender
    recommender = load_recommender()
    
    # Search container
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            movie_list = recommender.get_all_movie_titles()
            selected_movie = st.selectbox(
                "Type or select a movie you like:",
                movie_list,
                label_visibility="collapsed"
            )
        
        with col2:
            show_rec = st.button('Show Recommendations', use_container_width=True)
    
    # Show selected movie details (only when recommendations are not shown)
    if selected_movie and not show_rec:
        movie_details = recommender.get_movie_details(selected_movie)
        trailer_url = get_movie_trailer(movie_details['id'])
        
        st.markdown("""
            <div class="movie-container">
                <div class="movie-poster-container">
                    <img src="{}" class="movie-poster">
                </div>
                <div class="movie-details">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                        <h2 style="margin: 0;">{}</h2>
                        <a href="{}" target="_blank" class="trailer-btn">Watch Trailer</a>
                    </div>
                    <p><strong>Rating:</strong> ⭐ {}/10</p>
                    <p><strong>Release Date:</strong> {}</p>
                    <p><strong>Genres:</strong> {}</p>
                    <p><strong>Cast:</strong> {}</p>
                    <p><strong>Overview:</strong><br>{}</p>
                </div>
            </div>
        """.format(
            get_movie_poster(movie_details['id']),
            movie_details['title'],
            trailer_url if trailer_url else "#",
            movie_details['vote_average'],
            movie_details['release_date'][:4],
            movie_details['genres'],
            movie_details['cast'],
            movie_details['overview']
        ), unsafe_allow_html=True)
    
    # Show recommendations when button is clicked
    if show_rec and selected_movie:
        with st.spinner('Finding similar movies...'):
            recommendations = recommender.get_recommendations(selected_movie)
            
            if recommendations is not None:
                st.subheader("You might also like:")
                
                cols = st.columns(5)
                for idx, (col, (_, movie)) in enumerate(zip(cols, recommendations.iterrows())):
                    with col:
                        # Add error handling for movie poster
                        try:
                            poster_url = get_movie_poster(movie['id'])
                            if poster_url:
                                st.image(poster_url, use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/400x600?text=No+Poster", use_container_width=True)
                        except Exception as e:
                            st.image("https://via.placeholder.com/400x600?text=No+Poster", use_container_width=True)
                            
                        st.markdown(f"**{movie['title']}**")
                        st.markdown(f"⭐ {movie['vote_average']}/10")
                        st.markdown(f"📅 {movie['release_date'][:4]}")
                        
                        with st.expander("More Details"):
                            st.write(f"**Cast:** {movie['cast']}")
                            st.write(f"**Genres:** {movie['genres']}")
                            st.write(movie['overview'])

@st.cache_resource
def load_recommender():
    recommender = MovieRecommender()
    recommender.load_and_prepare_data()
    return recommender

if __name__ == "__main__":
    main() 