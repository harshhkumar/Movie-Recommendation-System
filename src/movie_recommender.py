import pandas as pd
import numpy as np
<<<<<<< HEAD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import ast

def convert_to_list(obj):
    if isinstance(obj, str):
        try:
            return ast.literal_eval(obj)
        except:
            return []
    return []

def get_crew_director(crew):
    crew_list = convert_to_list(crew)
    for person in crew_list:
        if person.get('job') == 'Director':
            return person.get('name', '')
    return ''

def get_list_items(items, key='name', limit=3):
    item_list = convert_to_list(items)
    return [item.get(key, '') for item in item_list[:limit] if item.get(key)]

def create_similarity_matrix():
    # Read CSV files
    movies = pd.read_csv('data/tmdb_5000_movies.csv')
    credits = pd.read_csv('data/tmdb_5000_credits.csv')
    
    # Merge datasets
    movies = movies.merge(credits, on='title')
    
    # Extract relevant features
    movies['genres'] = movies['genres'].apply(lambda x: ' '.join(get_list_items(x)))
    movies['keywords'] = movies['keywords'].apply(lambda x: ' '.join(get_list_items(x)))
    movies['cast'] = movies['cast'].apply(lambda x: ' '.join(get_list_items(x)))
    movies['crew'] = movies['crew'].apply(get_crew_director)
    
    # Fill NaN values
    movies['overview'] = movies['overview'].fillna('')
    
    # Create tags
    movies['tags'] = (movies['overview'] + ' ' + 
                     movies['genres'] + ' ' + 
                     movies['keywords'] + ' ' + 
                     movies['cast'] + ' ' + 
                     movies['crew']).str.lower()
    
    # Create movie dictionary and save
    movies_dict = movies[['id', 'title', 'tags', 'vote_average', 'release_date', 'cast', 'overview']].to_dict('records')
    pickle.dump(movies_dict, open('data/movies_dict.pkl', 'wb'))
    
    # Create count matrix and similarity
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags'].values).toarray()
    similarity = cosine_similarity(vectors)
    
    # Save similarity matrix
    pickle.dump(similarity, open('data/similarity.pkl', 'wb'))
    
    print("Similarity matrix created successfully!")
    return movies_dict, similarity

if __name__ == "__main__":
    create_similarity_matrix()
=======
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
    
    def get_recommendations(self, title):
        try:
            idx = self.movies_df[self.movies_df['title'] == title].index[0]
            sim_scores = list(enumerate(self.similarity_matrix[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            movie_indices = [i[0] for i in sim_scores[1:6]]
            return self.movies_df.iloc[movie_indices]
        except:
            return None
>>>>>>> 5ebf180189222cc4bbc525e4f2297c612ef13038
