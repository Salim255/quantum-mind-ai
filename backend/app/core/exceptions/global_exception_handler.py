from fastapi import FastAPI
from app.core.settings import Settings

class GlobalExceptionHandler:
    def __init__(self, app: FastAPI, settings: Settings):
        pass