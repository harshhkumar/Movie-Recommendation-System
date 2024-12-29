import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import streamlit as st

class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.credits_df = None
        self.similarity_matrix = None
        
    @st.cache_data
    def load_and_prepare_data(self):
        # Load data
        self.movies_df = pd.read_csv('./data/tmdb_5000_movies.csv')
        self.credits_df = pd.read_csv('./data/tmdb_5000_credits.csv')
        
        # Merge dataframes
        self.movies_df = self.movies_df.merge(self.credits_df, on='title')
        
        # Clean genres
        self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
        self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x: ' '.join(x))
        
        # Clean cast
        self.movies_df['cast'] = self.movies_df['cast'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)][:5])
        self.movies_df['cast'] = self.movies_df['cast'].apply(lambda x: ', '.join(x))
        
        # Clean overview
        self.movies_df['overview'] = self.movies_df['overview'].fillna('')
        
        # Combine features for recommendation
        self.movies_df['combined_features'] = self.movies_df['overview'] + ' ' + self.movies_df['genres']
        
        # Create similarity matrix
        tfidf = TfidfVectorizer(stop_words='english')
        feature_vectors = tfidf.fit_transform(self.movies_df['combined_features'])
        self.similarity_matrix = cosine_similarity(feature_vectors)
    
    def get_all_movie_titles(self):
        return self.movies_df['title'].tolist()
    
    def get_movie_details(self, title):
        return self.movies_df[self.movies_df['title'] == title].iloc[0]
    
    @st.cache_data
    def get_recommendations(self, title):
        try:
            idx = self.movies_df[self.movies_df['title'] == title].index[0]
            sim_scores = list(enumerate(self.similarity_matrix[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            movie_indices = [i[0] for i in sim_scores[1:6]]
            return self.movies_df.iloc[movie_indices]
        except:
            return None
