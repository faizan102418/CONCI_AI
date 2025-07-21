# conci-ai-assistant/backend/src/main.py
# Main FastAPI application entry point, now including the dashboard router.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os

# --- Local imports ---
# Import ALL API routers, including the new dashboard router
from .api.v1 import voice, pms_pos, dashboard # ADDED 'dashboard'

# Import application settings
from .core.config import settings

# Import AI service (for loading models at startup)
from .services.ai_models import ai_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function defines the startup and shutdown events for your FastAPI application.
    It's used here to load AI models when the application starts.
    """
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    # Load AI models using the service
    await ai_service.load_models()
    yield  # The application will run until this point
    print(f"{settings.APP_NAME} shutting down...")
    # Add any cleanup tasks here if necessary

# Initialize the FastAPI application with settings
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan # Attach the lifespan context manager
)

# --- CORS Configuration ---
# Define origins that are allowed to make requests to your FastAPI backend.
origins = [
    "http://localhost",
    "http://localhost:5173",  # Your React frontend's development URL
    "http://127.0.0.1:5173",  # Another common localhost variant
    # Add other frontend deployment URLs here when you deploy your app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- END CORS Configuration ---

# --- Include API Routers ---
# Attach the defined API routers to the main FastAPI application.
app.include_router(voice.router, prefix="/api/v1", tags=["Voice Interaction"])
app.include_router(pms_pos.router, prefix="/api/v1", tags=["PMS/POS Integration"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard Management"]) # NEW ROUTER INCLUSION

@app.get("/", summary="Check API health")
async def read_root():
    """
    Root endpoint to verify that the FastAPI application is running.
    Returns a simple message.
    """
    return {"message": f"{settings.APP_NAME} is running!"}

# This block allows you to run the application directly using 'python main.py'
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)