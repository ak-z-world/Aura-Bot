from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "Aura LLM API is running"}
