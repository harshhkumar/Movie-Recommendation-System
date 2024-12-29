# 🎬 Movie Recommendation System

A content-based movie recommendation system that suggests similar movies based on your selection. Built with Streamlit and powered by the TMDB dataset, it uses natural language processing and cosine similarity to find movie recommendations.

## 🛠️ How It Works

### Content-Based Filtering
The system uses content-based filtering which recommends movies based on their similarity to a movie the user likes. The similarity is calculated using:

1. **Text Processing**:
   - Movie descriptions and genres are combined
   - TF-IDF (Term Frequency-Inverse Document Frequency) vectorization is applied
   - This converts text data into numerical vectors

2. **Similarity Calculation**:
   - Cosine similarity is computed between all movies
   - Creates a similarity matrix for quick recommendations
   - Movies with highest similarity scores are recommended

### TMDB API Integration
- Fetches real-time movie posters
- Gets official movie trailers
- Ensures up-to-date movie information

## ✨ Features

1. **Movie Search**
   - Search from 5000+ movies
   - Auto-complete suggestions
   - Quick selection interface

2. **Movie Details**
   - High-quality movie posters
   - Release year
   - Rating
   - Cast information
   - Genre details
   - Movie overview

3. **Trailer Integration**
   - Direct YouTube trailer links
   - Watch without leaving the app

4. **Smart Recommendations**
   - 5 similar movie suggestions
   - Based on movie content and features
   - Instant results

5. **User Interface**
   - Netflix-inspired design
   - Responsive layout
   - Smooth animations
   - Dark theme

## 🌐 Live Demo

Try the app here: [Movie Recommender](https://filmfinder-ai.streamlit.app/)

## 📊 Datasets Used

The system uses the TMDB 5000 Movie Dataset:

1. **tmdb_5000_movies.csv**
   - Movie titles
   - Overview
   - Genres
   - Release dates
   - Ratings
   - Other metadata

2. **tmdb_5000_credits.csv**
   - Cast information
   - Crew details
   - Movie IDs
   - Character names

