from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from dotenv import load_dotenv

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine
from app.models import Base

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LiveRoom Backend API",
    description="Backend API for LiveRoom AI Companion Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - Production configuration
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://liveroom-ai.vercel.app",  # Your Vercel domain
    "https://www.liveroom-ai.com",     # Your custom domain
]

# In production, use specific origins; in development, allow all
if os.getenv("ENVIRONMENT") == "production":
    cors_origins = allowed_origins
else:
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Trusted host middleware - temporarily disabled due to compatibility issue
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["*"]  # Configure this properly in production
# )

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to LiveRoom Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "liveroom-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
