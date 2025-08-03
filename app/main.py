from fastapi import FastAPI
from app.routers.chatbot import router

app = FastAPI()
app.include_router(router)