from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import functions

app = FastAPI(
    title="QuensultingAI Voice Agent API",
    description="Backend API for Retell AI conversation flow",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(functions.router, prefix="/functions", tags=["Functions"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
