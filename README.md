# English Song Lyrics: Clustering, Recommender & Trainers

The project is about processing lyrics of English-speaking artists.

Libraries: numpy, pandas, BeautifulSoup4, requests, re, nltk, sklearn, scipy, matplolib

[![Code Climate](https://codeclimate.com/github/am-tropin/english-song-lyrics.svg)](https://codeclimate.com/github/am-tropin/english-song-lyrics)


## Table of contents
- [Datasets](#datasets)
- [Machine learning approaches](#machine-learning-approaches)
- [The Trainer 1: Fill in the gaps](#the-trainer-1-fill-in-the-gaps)
- [The Trainer 2: Find the signal word](#the-trainer-2-find-the-signal-word)


## Datasets

- The [code](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/eng-lyrics-trainer/discography_collecting.ipynb) collects the [library of discographies](https://github.com/am-tropin/eng-lyrics-trainer/tree/main/discography) from https://www.allthelyrics.com/. 


## Machine learning approaches

- The first problem is **clustering** of songs of bands with **Ronnie James Dio**. The given problem was solved by using **the scikit-learn K-means clustering** in the [clustering_of_Dio_bands.ipynb](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/clustering_of_Dio_bands.ipynb) notebook. The result is in the [dio_clusters.csv](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/dio_clusters.csv) file.

- The second problem is building a **text-based recommender** by one or a few songs. The given problem was solved by using **the scikit-learn cosine similarity and Tf-idf vectorizer** in the [recommender_lyrics.ipynb](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/recommender_lyrics.ipynb) notebook.

### Run locally:

1. Clone the project:
```bash
  git clone https://github.com/am-tropin/english-song-lyrics
```

2. Go to the project directory:
```bash
  cd english-song-lyrics
```

<!-- Create vitual enviroment and install dependencies
```bash
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
``` -->

3. Start the server:
```bash
  uvicorn main:app --reload
```

4. Enter an artist name from the list above in the terminal, for example:
```bash
  florence_the_machine
```

5. Copy a song name from the list above in the terminal, for example:
```bash
  No Light No Light
```

6. Go to web-browser 
```bash
  http://127.0.0.1:8000/docs/
```
and use the following box: 
- **Get Top Recommended Lyrics**. Type artist and song names, and amount of songs in the future top list.

Or 

5. Go to web-browser and use the following link to get the same info after typing the parameters:

```bash
  http://127.0.0.1:8000/top/_
```

Or 

6. Go to web-browser and use the following type of links to get the same info in clear dictionary view:

```bash
  http://127.0.0.1:8000/top_html/florence_the_machine_No Light No Light_8
```



## The Trainer 1: Fill in the gaps

- The trainer of listening. You can choose the artist, their song and the frequency of replacing random words with gaps. Open the lyrics with gaps (in file with a name like "lyrics_with_gaps_###.txt") in a new window. When you're listening to the song, fill in the gaps in [this trainer](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/trainer_for_listening.ipynb) and know your score! 


## The Trainer 2: Find the signal word

- The trainer of grammar. You can find all uses of the signal word in lyrics in our song collection. Set the signal word in [this trainer](https://github.com/am-tropin/eng-lyrics-trainer/blob/main/trainer_for_searching.ipynb) and know how to use it correctly! 


