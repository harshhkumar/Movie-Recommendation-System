import pandas as pd
import numpy as np
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
