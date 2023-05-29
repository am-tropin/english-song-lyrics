#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[16]:


import nltk
stopwords = nltk.corpus.stopwords.words('english')


# In[3]:


# import sys
# sys.path.append('../')
from functions.function_store import print_lexic_order_with_first_letter, collect_artist_list, collect_song_list, collect_full_discography


# # 1. Choosing the song for comparison

# In[4]:


'''
To view the collection
'''

# path = "discography/"
artist_list = collect_artist_list()

print_lexic_order_with_first_letter(artist_list)


# In[5]:


'''
To choose the artist
'''

target_artist = 'florence_the_machine'
# 'florence_the_machine'


# In[39]:


print()
print("Enter an artist name from the list above:")
target_artist = input()


# In[6]:


'''
To view the discography
'''

print_lexic_order_with_first_letter(collect_song_list(target_artist))


# In[7]:


'''
To choose the song:
'''

target_song = 'No Light No Light'


# In[15]:


# print()
# print("Enter an song name from the list above:")
# target_song = input()


# In[8]:


# for user-based recommender

target_songs_list = [
    ['queen', "Don't Stop Me Now"],
    ['queen', "Under Pressure"],
    ['lana_del_rey', "Blue Jeans"],
    ['rainbow', "Stargazer"],
    ['guns_n_roses', "You Could Be Mine"]
]


# # 2. Text-based Recommender

# In[17]:


def to_recommend_lyrics(df, column, target_key):
    # Instantiate the vectorizer object and transform the plot column
    vectorizer = TfidfVectorizer(max_df=0.7, min_df=2, stop_words=stopwords)
    vectorized_data = vectorizer.fit_transform(df[column])

    # Create Dataframe from TF-IDFarray
    tfidf_df = pd.DataFrame(vectorized_data.toarray(), columns=vectorizer.get_feature_names_out())

    # Assign the song titles to the index and inspect
    tfidf_df.index = df.index

    # Create the array of cosine similarity values
    cosine_similarity_array = cosine_similarity(tfidf_df)

    # Wrap the array in a pandas DataFrame
    cosine_similarity_df = pd.DataFrame(cosine_similarity_array, index=tfidf_df.index, columns=tfidf_df.index)

    # Find the values for the target song
    cosine_similarity_series = cosine_similarity_df.loc[target_key]

    # Sort these values highest to lowest
    ordered_similarities = cosine_similarity_series.sort_values(ascending=False)

    return ordered_similarities


# In[18]:


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
    full_discography_df2 = collect_full_discography()
    target_key = full_discography_df2[
        (full_discography_df2['artist'] == artist) &
        (full_discography_df2['song'] == song)
    ].index[0] # select only one key in case of song duplicates
    
    similar_df = pd.DataFrame(to_recommend_lyrics(full_discography_df2, 'lyrics', target_key)).rename(columns={target_key:'similarity_score'})
    similar_df2 = similar_df.join(full_discography_df2).reset_index(drop=True)[['similarity_score','artist','album','song']]

    return similar_df2[similar_df2.index.isin(list(range(1, n+1)))]


# In[19]:


top_recommended_lyrics(target_artist, target_song, 5)


# # 3. User-profile Recommender

# In[20]:


def to_recommend_lyrics_by_set(df, column, target_list):
    # Instantiate the vectorizer object and transform the plot column
    vectorizer = TfidfVectorizer(max_df=0.7, min_df=2, stop_words=stopwords)
    vectorized_data = vectorizer.fit_transform(df[column])

    # Create Dataframe from TF-IDFarray
    tfidf_df = pd.DataFrame(vectorized_data.toarray(), columns=vectorizer.get_feature_names_out())

    # Assign the song titles to the index and inspect
    tfidf_df.index = df.index
    
    # Create a subset of only the songs the user has enjoyed
    songs_enjoyed_df = tfidf_df.reindex(target_list)

    # Generate the user profile by finding the average scores of songs they enjoyed
    user_prof = songs_enjoyed_df.mean()

    # Find subset of tfidf_df that does not include songs in target_list
    tfidf_subset_df = tfidf_df.drop(target_list, axis=0)

    # Calculate the cosine_similarity and wrap it in a DataFrame
    similarity_array = cosine_similarity(user_prof.values.reshape(1, -1), tfidf_subset_df)
    similarity_df = pd.DataFrame(similarity_array.T, index=tfidf_subset_df.index, columns=["similarity_score"])

    # Sort the values from high to low by the values in the similarity_score
    sorted_similarity_df = similarity_df.sort_values(by="similarity_score", ascending=False)

    return sorted_similarity_df


# In[21]:


def top_recommended_lyrics_by_set(user_list, n):
    """Returns list of Top-`n` song lyrics which are most similar to songs 
    with artist name and song name from `user_list`.
    
    Args:
        user_list (list): 
        n (int): The number of most similar songs.
    
    Returns:
        DataFrame
    """
    full_discography_df2 = collect_full_discography()
    my_favourite_songs = []

    for row in user_list:
        target_key = full_discography_df2[
            (full_discography_df2['artist'] == row[0]) &
            (full_discography_df2['song'] == row[1])
        ].index[0] # select only one key in case of song duplicates
        my_favourite_songs.append(target_key)
    
    similar_df = pd.DataFrame(to_recommend_lyrics_by_set(full_discography_df2, 'lyrics', my_favourite_songs)).rename(columns={target_key:'similarity_score'})
    similar_df2 = similar_df.join(full_discography_df2).reset_index(drop=True)[['similarity_score','artist','album','song']]

    return similar_df2[similar_df2.index.isin(list(range(n)))]


# In[22]:


top_recommended_lyrics_by_set(target_songs_list, 5)


# In[ ]:





# In[ ]:




