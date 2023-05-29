#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import re
import pandas as pd
import random


# In[2]:


# from pathlib import Path

# ROOT = Path(__file__).parent.parent


# In[ ]:





# In[ ]:





# # For trainers

# In[ ]:


def collect_artist_list():
    path = "../discography/"
    dir_list = os.listdir(path)
    artist_list = [re.sub("_discography_allthelyrics.csv", "", d) for d in dir_list if "_discography_allthelyrics.csv" in d]

    return artist_list


# In[ ]:


def collect_discography_df(artist):
    path = "../discography/"
    discography_df = pd.read_csv(path + artist + '_discography_allthelyrics.csv', sep='\t', encoding='utf-8')

    return discography_df

def collect_song_list(artist):
    discography_df = collect_discography_df(artist)
    songs = list(discography_df['song'])

    return songs


# In[ ]:


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


# In[ ]:


# creating the file with lyrics with gaps and the list with correct answers

def add_gaps_to_lyrics(artist, song_title, string_frequency):
    
    discography_df = collect_discography_df(artist)
    song_txt = discography_df[discography_df['song'] == song_title]['lyrics'].iloc[0]
    song_strings = song_txt.split('\n')

    string_counter = 0
    correct_answers = []
    gap_counter = 0
    
    fixed_song_list = []

    for s in song_strings:
        if string_counter % string_frequency == 0:
            gap_counter += 1
            words = s.split(' ')
#             to set random index of deleting word in the string
            deleted_word_no = random.randint(0,len(words)-1)
#             to save deleting word in correct_answers list
            correct_answers.append(str.lower(str.strip(re.sub("[^\w\-\']", " ", words[deleted_word_no]))))
#             to replace deleting word in string s with gaps, but not ' and not - # "\w|-|\'"
            words[deleted_word_no] = "({0})".format(gap_counter) + re.sub("\w|-|\'", "_", words[deleted_word_no])
#             to glue the string back
            fixed_song_list.append(' '.join(words))
        else:
            fixed_song_list.append(s)
        string_counter += 1
    
    with open("lyrics_with_gaps_" + "_".join(song_title.split()) + ".txt", 'w') as file:
        pass
    with open("lyrics_with_gaps_" + "_".join(song_title.split()) + ".txt", 'w') as f:
        for s in fixed_song_list:
            f.write(f"{s}\n")
    
    return correct_answers, gap_counter


# In[ ]:


# processing of your answers

def mark(a, b):
    if a == b:
        return '+'
    else:
        return ''

def answers_processing(correct_answers, gap_counter):

    my_answers = []

    for i in range(gap_counter):
        my_answers.append(str.lower(str.strip(input("{0}:\t ".format(i+1)))))

    print()
    correct_cnt = sum([1 for i in range(gap_counter) if correct_answers[i] == my_answers[i] ])

    shift = max(8, max(map(len, correct_answers)))
    print("\t correct:{0} - my answer:".format(' '*(shift-8)))

    for i in range(gap_counter):
        print("{0}  {1}\t {2} - {3}".format(i+1, mark(correct_answers[i],my_answers[i]), correct_answers[i] + ' '*(shift - len(correct_answers[i])), my_answers[i]))
    print()

    return "Results: {0} from {1} ({2}%)".format(correct_cnt, gap_counter, round(100 * correct_cnt/gap_counter, 1))


# In[ ]:





# In[ ]:


def print_strings_with_pattern(target_word):
    
    artist_list = collect_artist_list()
    target_dict_full = {}
    path = "../discography/"

    for artist in artist_list:
        discography_df = pd.read_csv(path + artist + '_discography_allthelyrics.csv', sep='\t', encoding='utf-8')
        mask = discography_df["lyrics"].str.contains(target_word, na=True)
        if len(discography_df.loc[mask, 'song']) > 0:
            song_list = list(discography_df.loc[mask, 'song'])
            target_dict_full[artist] = song_list
            for song in song_list:
                string_list = list(discography_df[discography_df["song"] == song]["lyrics"].apply(lambda x: x.split('\n')))
                target_string_list = [s for s in string_list[0] if re.findall(target_word, str.lower(s))] # target_word in s
                target_string_list = list(set(target_string_list))
                i = target_dict_full[artist].index(song)
                target_dict_full[artist] = target_dict_full[artist][:i]+[{song: target_string_list}]+target_dict_full[artist][i+1:]

    return target_dict_full


def download_target_strings_to_txt(target_word):
    
    target_dict_full = print_strings_with_pattern(target_word)
    
    with open("lyrics_with_target_word_[" + target_word + "].txt", 'w') as f:
        for artist in target_dict_full.keys():
            for d in target_dict_full[artist]:
                for song in d.keys():
                    for string in d[song]:
                        f.write("{0}\n".format(string))
                        f.write("\t\t\t\t\t\t\t\t\t\t({0}, \"{1}\")\n\n".format(artist, song))


# In[ ]:




