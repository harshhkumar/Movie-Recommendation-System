import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.credits_df = None
        self.similarity_matrix = None
        
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
        
        # Add empty poster_path column if it doesn't exist
        if 'poster_path' not in self.movies_df.columns:
            self.movies_df['poster_path'] = ''
        
        # Combine features for recommendation
        self.movies_df['combined_features'] = self.movies_df['overview'] + ' ' + self.movies_df['genres']
        
        # Create similarity matrix
        tfidf = TfidfVectorizer(stop_words='english')
        feature_vectors = tfidf.fit_transform(self.movies_df['combined_features'])
        self.similarity_matrix = cosine_similarity(feature_vectors)
        
    def get_recommendations(self, movie_title):
        try:
            idx = self.movies_df[self.movies_df['title'] == movie_title].index[0]
            sim_scores = list(enumerate(self.similarity_matrix[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:6]
            movie_indices = [i[0] for i in sim_scores]
            return self.movies_df[['id', 'title', 'genres', 'vote_average', 'release_date', 
                                 'cast', 'overview']].iloc[movie_indices]
        except IndexError:
            return None
            
    def get_all_movie_titles(self):
        return self.movies_df['title'].tolist()
        
    def get_movie_details(self, movie_title):
        return self.movies_df[self.movies_df['title'] == movie_title].iloc[0]
