from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app: FastAPI):
    origins: list = [
        "http://localhost:4200",
    ]
    app.add_middleware(
       CORSMiddleware,
       allow_origins=origins,
       allow_methods=["*"],
       allow_headers=["*"],
    )