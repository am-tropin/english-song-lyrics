#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[1]:


import os
import re
import pandas as pd


# In[2]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# # 1. Choosing the song for comparison

# In[3]:


# printing a list of titles in lexicographic order with division by the first letter

def print_lexic_order_with_first_letter(list_list):
    list_list = sorted(list_list)
    first_letter = ''
    for s in list_list:
        if s[0] != first_letter:
            first_letter = s[0]
            print()
            print(str.upper(first_letter))
        print(s)
    return 1


# In[4]:


'''
To view the collection
'''

path = "discography/"
dir_list = os.listdir(path)
artist_list = [re.sub("_discography_allthelyrics.csv", "", d) for d in dir_list if "_discography_allthelyrics.csv" in d]

print_lexic_order_with_first_letter(artist_list)


# In[5]:


'''
To choose the artist
'''

target_artist = 'florence_the_machine'
# 'florence_the_machine'


# In[6]:


discography_df = pd.read_csv('discography/' + target_artist + '_discography_allthelyrics.csv', sep='\t', encoding='utf-8')
discography_df.head()


# In[7]:


'''
To view the discography
'''

songs = list(discography_df['song'])

print_lexic_order_with_first_letter(songs)


# In[8]:


'''
To choose the song:
'''

target_song = 'No Light No Light'


# In[ ]:





# # 2. Creating the full lyrics base

# In[9]:


full_discography_list = []

for artist in artist_list:
    discography_df = pd.read_csv('discography/' + artist + '_discography_allthelyrics.csv', sep='\t', encoding='utf-8')
    discography_df['artist'] = artist
    discography_df['key'] = discography_df.apply(lambda x: x['artist'] + '__' + '_'.join(x['album'].split()) + '__' + '_'.join(x['song'].split()), axis=1)
# .strip(",[]()-?!'")
    full_discography_list.append(discography_df)
    
full_discography_df = pd.concat(full_discography_list, axis=0)[['key', 'artist', 'album', 'song', 'lyrics', 'link']]
# full_discography_df
    


# In[10]:


full_discography_df2 = full_discography_df.set_index('key')
full_discography_df2.head()


# In[11]:


target_lyrics_df = full_discography_df2[
    (full_discography_df2['artist'] == target_artist) &
#     full_discography_df2[''] == album_title &
    (full_discography_df2['song'] == target_song)
]

target_key = target_lyrics_df.index[0]
target_key


# In[ ]:





# # 3. Text-based Recommender

# In[12]:


def to_recommend_lyrics(df, target_key):
    # Instantiate the vectorizer object and transform the plot column
    vectorizer = TfidfVectorizer(max_df=0.7, min_df=2)
    vectorized_data = vectorizer.fit_transform(df['lyrics'])

    # Create Dataframe from TF-IDFarray
    tfidf_df = pd.DataFrame(vectorized_data.toarray(), columns=vectorizer.get_feature_names_out())

    # Assign the movie titles to the index and inspect
    tfidf_df.index = df.index

    # Create the array of cosine similarity values
    cosine_similarity_array = cosine_similarity(tfidf_df)

    # Wrap the array in a pandas DataFrame
    cosine_similarity_df = pd.DataFrame(cosine_similarity_array, index=tfidf_df.index, columns=tfidf_df.index)

    # Find the values for the movie Rio
    cosine_similarity_series = cosine_similarity_df.loc[target_key]

    # Sort these values highest to lowest
    ordered_similarities = cosine_similarity_series.sort_values(ascending=False)

    return ordered_similarities



# In[13]:


def top_of_similarity(similar_df, threshold):
    similar_df_head = similar_df[similar_df.values >= threshold]
    similar_df_head2 = pd.DataFrame(similar_df_head)
    similar_df_head2.columns = ['similarity_score']
    
    return similar_df_head2


# In[14]:


similar_df = to_recommend_lyrics(full_discography_df2, target_key)

similar_df_head2 = top_of_similarity(similar_df, 0.2)
similar_df_head2.join(full_discography_df2).reset_index(drop=True)[['similarity_score','artist','album','song']]


# In[37]:


def top_recommended_lyrics(artist, song, n):
    """Returns list of Top-`n` song lyrics which are most similar to song 
    with `artist` artist name and `song` song name.
    
    Args:
        artist (str): The artist name.
        song (str): The song name.
        n (int): The number of most similar songs.
    
    Returns:
        DataFrame
    """
    target_lyrics_df = full_discography_df2[
        (full_discography_df2['artist'] == artist) &
        (full_discography_df2['song'] == song)
    ]
    target_key = target_lyrics_df.index[0]
    similar_df = pd.DataFrame(to_recommend_lyrics(full_discography_df2, target_key)).rename(columns={target_key:'similarity_score'})
    similar_df2 = similar_df.join(full_discography_df2).reset_index(drop=True)[['similarity_score','artist','album','song']]

    return similar_df2[similar_df2.index.isin(list(range(1, n+1)))]


# In[38]:


top_recommended_lyrics(target_artist, target_song, 5)


# # 4. User-profile Recommender

# In[ ]:


'''
define the set of your favourite songs
and 
learn the most similar songs from the rest of the full discography
'''


# In[79]:


my_favourite_songs_list = [
    ['queen', "", "Don't Stop Me Now"],
    ['queen', "", "Under Pressure"],
    ['lana_del_rey', "", "Blue Jeans"],
    ['rainbow', "", "Stargazer"],
    ['guns_n_roses', "", "You Could Be Mine"]
]


# In[82]:


my_favourite_songs_df = pd.DataFrame(my_favourite_songs_list)
my_favourite_songs_df.columns = ['artist', 'album_0', 'song']
my_favourite_songs_df = my_favourite_songs_df.drop(['album_0'], axis=1)
my_favourite_songs_df


# In[102]:


df3 = full_discography_df2.merge(my_favourite_songs_df, how='inner', on=['artist', 'song'])
df3['key'] = df3.apply(lambda x: x['artist'] + '__' + '_'.join(x['album'].split()) + '__' + '_'.join(x['song'].split()), axis=1)
df3 = df3.set_index('key')
# df3.index

my_favourite_songs = list(df3.index)
my_favourite_songs


# In[107]:


def to_recommend_lyrics_by_set(df, target_list):
    vectorizer = TfidfVectorizer(max_df=0.7, min_df=2)
    vectorized_data = vectorizer.fit_transform(df['lyrics'])

    # Create Dataframe from TF-IDFarray
    tfidf_df = pd.DataFrame(vectorized_data.toarray(), columns=vectorizer.get_feature_names_out())

    # Assign the movie titles to the index and inspect
    tfidf_df.index = df.index

    # Create a subset of only the movies the user has enjoyed
    movies_enjoyed_df = tfidf_df.reindex(target_list)

    # Generate the user profile by finding the average scores of movies they enjoyed
    user_prof = movies_enjoyed_df.mean()

    # Find subset of tfidf_df that does not include movies in list_of_movies_enjoyed
    tfidf_subset_df = tfidf_df.drop(target_list, axis=0)

    # Calculate the cosine_similarity and wrap it in a DataFrame
    similarity_array = cosine_similarity(user_prof.values.reshape(1, -1), tfidf_subset_df)
    similarity_df = pd.DataFrame(similarity_array.T, index=tfidf_subset_df.index, columns=["similarity_score"])

    # Sort the values from high to low by the values in the similarity_score
    sorted_similarity_df = similarity_df.sort_values(by="similarity_score", ascending=False)

    return sorted_similarity_df



# In[109]:


similar_by_set_df = to_recommend_lyrics_by_set(full_discography_df2, my_favourite_songs)

similar_df_head3 = top_of_similarity(similar_by_set_df, 0.3)
similar_df_head3.join(full_discography_df2).reset_index(drop=True)[['similarity_score','artist','album','song']]


# In[ ]:





# In[ ]:





# In[ ]:




