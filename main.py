#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from lyrics_recommender import top_recommended_lyrics

# API
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates


# In[ ]:


app = FastAPI()
templates = Jinja2Templates(directory="templates/")


@app.get("/")
async def root():
    return "Welcome to the English Song Lyrics Recommender!"


# without html

@app.get("/range_calendar/{artist}_{song}_{n}")
async def get_top_recommended_lyrics(artist: str, song: str, n: int):
    return top_recommended_lyrics(artist, song, n).transpose().to_dict()


# with html

@app.get("/top_html/{artist}_{date2}")
async def get_top_recomm_lyrics(artist: str, song: str, n: int):
    return {"Anniversaries in the range:": top_recommended_lyrics(artist, song, n)}

@app.get("/top/{form}")
def form_post_top(request: Request):
    result = "Type artist name (in lower case, with _ instead of spaces) and song name"
    return templates.TemplateResponse('form_song_recommender.html', context={'request': request, 'result': result})

@app.post("/top/{form}")
def form_post_top(request: Request, artist: str = Form(...), song: str = Form(...), n: int = Form(...)):
    result = top_recommended_lyrics(artist, song, n)
    return templates.TemplateResponse('form_song_recommender.html', context={'request': request, 'result': result.to_html()})


