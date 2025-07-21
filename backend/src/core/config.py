# conci-ai-assistant/backend/src/core/config.py
# This file defines the application settings using Pydantic-settings.

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    """
    Application settings class.
    Loads environment variables from a .env file (if present)
    and provides default values.
    """
    # FastAPI Application Settings
    APP_NAME: str = "Conci AI Assistant"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API for voice-controlled AI assistant for hotel operations."

    # AI Model Configuration (adjust based on how you integrate actual models)
    # These could be paths to local models or API keys/endpoints for cloud services.
    WHISPER_MODEL_SIZE: str = "small" # Example: "base", "medium", "large"
    MISTRAL_MODEL_ID: str = "mistral-7b-instruct" # Example: a model name or API endpoint
    COQUI_TTS_MODEL_NAME: str = "tts_models/en/ljspeech/fast_pitch" # Example: a Coqui TTS model identifier

    # PMS/POS Mock Settings (useful for initial development without real integrations)
    MOCK_PMS_POS_ENABLED: bool = True

    # Configuration for Pydantic-settings to load from .env file
    # It looks for a .env file in the project root (conci-ai-assistant/)
    # 'extra='ignore'' means it won't raise an error if other env vars are present.
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'),
        extra='ignore'
    )

# Create an instance of the Settings class to be imported and used throughout the application.
settings = Settings()