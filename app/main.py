from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from components.optimize_time import data_wrangling

import json

app = FastAPI()

# Neccessary for CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TwitterIDAndHandleInput(BaseModel):
    user_id: int
    twitter_handle: str

class TwitterHandleInput(BaseModel):
    twitter_handle: str

@app.get("/")
async def root():
    """
    Verifies the API is deployed, and links to the docs
    """
    return HTMLResponse("""
    <h1>SoMe Data Science API</h1>
    <p>Go to <a href="/docs">/docs</a> for documentation.</p>
    """)

@app.post('/recommend')
async def recommend(user_input: TwitterIDAndHandleInput):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']
    user_id = request_dict['user_id']

    dw = data_wrangling(twitter_handle, 5)
    followers_ids = dw.followers_ids()
    get_follower_data = dw.get_follower_data(followers_ids)
    optimal_time = dw.optimal_time(get_follower_data)

    # optimal_time = "Tue May 26 2020 17:00:00 UTC+0000"

    baseline_time = {"optimal_time": optimal_time}

    # backend_url = 'https://api.so-me.net/api/posts/' + str(user_id)
    # header_data = {'Authorization' : BACKEND_AUTHORIZATION}
    # r = requests.put(backend_url, headers = header_data, json=baseline_time)

    return JSONResponse(content=baseline_time)


@app.post('/topic_model/schedule')
async def schedule(user_input: TwitterHandleInput):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']

    # TODO: Replace dummy data

    dummy_data = {'success': True}

    return JSONResponse(content=dummy_data)


@app.post('/topic_model/status')
async def status(user_input: TwitterHandleInput):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']

    # TODO: Replace dummy data

    dummy_data = {
        'success': True,
        'queued': True,
        'processing': False,
        'model_ready': True
        }

    return JSONResponse(content=dummy_data)


@app.post('/topic_model/get_topics')
async def get_topics(user_input: TwitterHandleInput):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']

    # TODO: Replace dummy data

    dummy_data = {
        'success': True,
        'topics': {
            1: ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "Sed", "at", "nulla", 
            "augue", "Mauris", "eget", "libero", "ac", "felis", "consectetur", "tristique", "in"],
            2: ["et", "libero", "Praesent", "lacerat", "et", "sapien", "quis", "sodales", "Suspendisse", "varius", 
            "bibendum", "suscipit", "Nulla", "quis", "dictum", "sapien", "Phasellus", "venenatis", "dignissim", "turpis"],
            3: ["in", "pharetra", "Cras", "aliquam", "sit", "amet", "nisl", "ut", "venenatis", "Orci", "varius", "natoque", 
            "penatibus", "et", "magnis", "dis", "parturient", "montes", "nascetur", "ridiculus"],
            4: ["mus", "Donec", "ex", "nunc", "pulvinar", "a", "nibh", "vel", "auctor", "laoreet", "justo", 'Sed', 
            "pellentesque", "erat", "odio", "ut", "posuere", "augue", "congue", "id"],
            5: ["Nunc", "mollis", "a", "tortor", "id", "vulputate", "Duis", "auctor", "sapien", "in", "facilisis", "auctor", 
            "In", "ultrices", "leo", "eget", "dolor", "consectetur", "a", "dictum"]
            }
        }

    return JSONResponse(content=dummy_data)