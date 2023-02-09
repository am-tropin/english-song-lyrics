# English Lyrics: Clustering & Trainer

The project is about processing lyrics of English-speaking artists.

Libraries: numpy, pandas, BeautifulSoup4, requests, re, nltk, sklearn, scipy, matplolib


## Table of contents
- [Datasets](#datasets)
- [Machine learning approach](#machine-learning-approach)
- [The Trainer 1: Fill in the gaps](#the-trainer-1-fill-in-the-gaps)


## Datasets

- The [code](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/eng-lyrics-trainer/discography_collecting.ipynb) collects the [library of discographies](https://github.com/am-tropin/eng-lyrics-trainer/tree/main/discography) from https://www.allthelyrics.com/. 


## Machine learning approach

- The problem is clustering of songs of bands with **Ronnie James Dio**. The given problem was solved by using **the scikit-learn K-means clustering** in the [clustering_of_Dio_bands.ipynb](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/clustering_of_Dio_bands.ipynb) notebook. The result is in the [dio_clusters.csv](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/dio_clusters.csv) file.


## The Trainer 1: Fill in the gaps

- The trainer of listening. You can choose the artist, their song and the frequency of replacing of random words with gaps. Open the lyrics with gaps (in file with a name like "lyrics_with_gaps_###.txt") in a new window. When you're listening the song, fill in the gaps in [this trainer](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/trainer_for_listening.ipynb) and know your score! 


