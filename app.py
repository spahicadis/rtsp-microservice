import rtsp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import redis

rtsp.read_frames()

r = redis.Redis(host='192.168.1.100', port=6379, decode_responses=True)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/frames/{id}")
def read_redis(id: str):
    redis_value = r.get(id)
    return json.loads(redis_value)


## app.get id za svaki parking
## Querya u redisu npr podatke o tom parkingu i returna nazad kroz SSE ili WebSockets. Moramo ovo izbrainstormatigit

