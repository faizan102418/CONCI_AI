# conci-ai-assistant/backend/src/services/ai_models.py
# This file provides a service wrapper for actual AI model integrations (ASR, LLM, TTS),
# now with enhanced LLM logic to identify and structure tasks.
# soundfile dependency has been removed.

import asyncio
import base64
import io
import numpy as np
# import soundfile as sf # REMOVED: No longer needed
import re

# Import actual AI model libraries
import whisper # ASR
from transformers import pipeline # LLM (Mistral)
from TTS.api import TTS # Coqui TTS

# Import settings and new TaskCreateRequest model
from ..core.config import settings
from ..core.models import TaskCreateRequest

class AIService:
    """
    Manages the integration and interaction with various AI models:
    Whisper (ASR), Mistral 7B (LLM), and Coqui TTS (TTS).
    Models are loaded during application startup.
    """
    def __init__(self):
        self.whisper_model = None
        self.mistral_pipeline = None
        self.coqui_tts_model = None
        self.models_loaded = False

    async def load_models(self):
        """
        Loads the Whisper, Mistral, and Coqui TTS models.
        This is an asynchronous operation and will be called once at application startup.
        """
        if self.models_loaded:
            print("AI models already loaded.")
            return

        print("Loading AI models for the first time. This may take a while...")

        try:
            # --- Load Whisper ASR Model ---
            print(f"Loading Whisper ASR model ({settings.WHISPER_MODEL_SIZE})...")
            self.whisper_model = whisper.load_model(settings.WHISPER_MODEL_SIZE, device="cpu")
            print("Whisper ASR model loaded.")

            # --- Load Mistral LLM Model ---
            print(f"Loading Mistral LLM ({settings.MISTRAL_MODEL_ID})...")
            self.mistral_pipeline = pipeline(
                "text-generation",
                model=settings.MISTRAL_MODEL_ID,
                device="cpu"
            )
            print("Mistral LLM loaded.")

            # --- Load Coqui TTS Model ---
            print(f"Loading Coqui TTS model ({settings.COQUI_TTS_MODEL_NAME})...")
            self.coqui_tts_model = TTS(
                model_name=settings.COQUI_TTS_MODEL_NAME,
                progress_bar=False,
                gpu=False
            )
            print("Coqui TTS model loaded.")

            self.models_loaded = True
            print("All AI models loaded successfully!")

        except Exception as e:
            print(f"Error loading AI models: {e}")
            raise

    async def transcribe_audio(self, audio_bytes: bytes) -> str:
        """
        Transcribes raw audio bytes into text using the Whisper ASR model.
        """
        if not self.models_loaded:
            await self.load_models()

        print("AIService: Transcribing audio with Whisper...")
        try:
            audio_file = io.BytesIO(audio_bytes)
            result = self.whisper_model.transcribe(audio_file)
            transcribed_text = result["text"]
            print(f"Whisper Transcribed: '{transcribed_text}'")
            return transcribed_text
        except Exception as e:
            print(f"Error during Whisper transcription: {e}")
            raise

    async def get_llm_response(self, text_input: str) -> tuple[str, Optional[TaskCreateRequest]]:
        """
        Generates a text response using the Mistral 7B LLM.
        Also attempts to identify and structure a task from the input text.
        Returns a tuple: (conversational_response_text, TaskCreateRequest_object_if_identified).
        """
        if not self.models_loaded:
            await self.load_models()

        print(f"AIService: Getting LLM response for: '{text_input}' with Mistral...")
        task_to_create: Optional[TaskCreateRequest] = None
        llm_response_text: str = ""

        try:
            text_input_lower = text_input.lower()
            room_match = re.search(r'(room|rm)\s*(\d+)', text_input_lower)
            room_number = room_match.group(2) if room_match else None

            if "towel" in text_input_lower or "towels" in text_input_lower or "linens" in text_input_lower:
                llm_response_text = f"Certainly, I'll send fresh towels to room {room_number if room_number else 'your room'}. Is there anything else?"
                task_to_create = TaskCreateRequest(
                    guest_request=text_input,
                    room_number=room_number,
                    category="Housekeeping",
                    priority="medium",
                )
            elif "fix" in text_input_lower or "broken" in text_input_lower or "maintenance" in text_input_lower:
                llm_response_text = f"I've noted a maintenance request for room {room_number if room_number else 'your room'}. Could you describe the issue briefly?"
                task_to_create = TaskCreateRequest(
                    guest_request=text_input,
                    room_number=room_number,
                    category="Maintenance",
                    priority="high" if "urgent" in text_input_lower else "medium",
                )
            elif "food" in text_input_lower or "drink" in text_input_lower or "room service" in text_input_lower:
                llm_response_text = f"Certainly, what would you like to order from room service for room {room_number if room_number else 'your room'}?"
                task_to_create = TaskCreateRequest(
                    guest_request=text_input,
                    room_number=room_number,
                    category="Room Service",
                    priority="medium",
                )
            elif "spa booking" in text_input_lower or "spa appointment" in text_input_lower:
                llm_response_text = "Certainly, I can help with a spa booking. What service are you interested in and what is your name?"
                task_to_create = None # Handled by separate endpoint
            elif "create task" in text_input_lower or "hotsos" in text_input_lower:
                llm_response_text = "I can create a HotSOS task. Please describe the task."
                task_to_create = None # Handled by separate endpoint
            else:
                prompt = f"### Instruction:\n{text_input}\n\n### Response:\n"
                response = self.mistral_pipeline(
                    prompt,
                    max_new_tokens=100,
                    num_return_sequences=1,
                    do_sample=True,
                    temperature=0.7
                )
                llm_response_text = response[0]['generated_text'].replace(prompt, '').strip()
                print(f"Mistral LLM Response: '{llm_response_text}'")

            print(f"LLM determined task_to_create: {task_to_create.dict() if task_to_create else 'None'}")
            return llm_response_text, task_to_create

        except Exception as e:
            print(f"Error during Mistral LLM generation or task extraction: {e}")
            return "I apologize, I'm having trouble understanding that request right now.", None

    async def synthesize_speech(self, text_to_speak: str) -> bytes:
        """
        Synthesizes speech from text using the Coqui TTS model.
        Returns audio bytes in WAV format.
        """
        if not self.models_loaded:
            await self.load_models()

        print(f"AIService: Synthesizing speech for: '{text_to_speak}' with Coqui TTS...")
        try:
            audio_numpy_array = self.coqui_tts_model.tts(text=text_to_speak)
            # We can't use soundfile here anymore.
            # For a true playable WAV, you'd need to manually construct the WAV header
            # and concatenate it with the raw audio data (from numpy array).
            # For now, we'll return a very minimal, non-playable WAV header
            # or you could return just the raw audio data (without header)
            # and handle it on the frontend if it's expecting raw.

            # Returning a minimal WAV header for compatibility, but it won't play the actual speech.
            # This is a placeholder for when you might add a different audio encoding library.
            print("Coqui TTS synthesis complete (returning dummy WAV header).")
            return b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xAC\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
        except Exception as e:
            print(f"Error during Coqui TTS synthesis: {e}")
            raise

# Instantiate the AI Service.
ai_service = AIService()