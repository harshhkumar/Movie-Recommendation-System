#!/usr/bin/env python
# coding: utf-8

# In[67]:


import pandas as pd
import numpy as np
import pickle


# In[68]:


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


# In[69]:


movies.head(1)


# In[70]:


credits.head(1)


# In[71]:


movies = movies.merge(credits,on='title')


# In[72]:


movies.head(1)


# In[73]:


# movie id
# genres
# keywords
# title
# overview
# cast
# crew
movies=movies[['movie_id','genres','keywords','title','overview','cast','crew']]


# In[74]:


movies.head(1)


# In[75]:


movies.isna().sum()


# In[76]:


movies.dropna(inplace=True)


# In[77]:


movies.isna().sum()


# In[78]:


movies.duplicated().sum()


# In[79]:


movies.iloc[0].genres


# In[52]:


#'[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
# ['Action','Adventure','Fantasy','SciFi']


# In[83]:


import ast


# In[85]:


def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
        


# In[86]:


movies['genres']=movies['genres'].apply(convert)


# In[87]:


movies.head(5)


# In[88]:


movies['keywords']=movies['keywords'].apply(convert)


# In[89]:


movies.head(5)


# In[90]:


def convert3(obj):
    L=[]
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L


# In[91]:


movies['cast']=movies['cast'].apply(convert3)


# In[92]:


movies.head(5)


# In[94]:


def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L


# In[95]:


movies['crew']=movies['crew'].apply(fetch_director)


# In[96]:


movies.head(5)


# In[97]:


movies['overview']=movies['overview'].apply(lambda x:x.split())


# In[98]:


movies.head(5)


# In[99]:


movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])


# In[100]:


movies.head(3)


# In[101]:


movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']


# In[102]:


movies.head(3)


# In[103]:


df = movies[['movie_id','title','tags']]
df.head(5)


# In[104]:


df['tags'] = df['tags'].apply(lambda x: " ".join(x))


# In[105]:


df.head(5)


# In[106]:


df['tags'] = df['tags'].apply(lambda x:x.lower())
df.head(5)


# In[107]:


get_ipython().system('pip install nltk')
import nltk


# In[108]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[109]:


def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[110]:


df['tags']=df['tags'].apply(stem)


# In[111]:


df['tags'][0]


# In[112]:


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')


# In[113]:


vectors=cv.fit_transform(df['tags']).toarray()


# In[114]:


vectors


# In[115]:


cv.get_feature_names()


# In[116]:


ps.stem('danced')


# In[117]:


stem('in the 22nd century, a parapleg marin is dispatch to the moon pandora on a uniqu mission, but becom torn between follow order and protect an alien civilization. action adventur fantasi sciencefict cultureclash futur spacewar spacecoloni societi spacetravel futurist romanc space alien tribe alienplanet cgi marin soldier battl loveaffair antiwar powerrel mindandsoul 3d samworthington zoesaldana sigourneyweav jamescameron')


# In[118]:


from sklearn.metrics.pairwise import cosine_similarity


# In[119]:


similarity= cosine_similarity(vectors)


# In[120]:


similarity[0]


# In[121]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]


# In[122]:


def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    for i in movies_list:
        print(df.iloc[i[0]].title)


# In[123]:


recommend('Gandhi')


# In[124]:


recommend('John Carter')


# In[125]:


# Save movies data
movies_dict = movies.to_dict()
pickle.dump(movies_dict, open('movies_dict.pkl', 'wb'))

# Save similarity matrix
pickle.dump(similarity, open('similarity.pkl', 'wb'))


# In[ ]:




