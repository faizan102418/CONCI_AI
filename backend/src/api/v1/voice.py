# conci-ai-assistant/backend/src/api/v1/voice.py
# This file defines API endpoints related to voice interaction and AI processing,
# now integrated with task creation for the dashboard.

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import base64
import io

# Import the AI service and Pydantic models
from ...services.ai_models import ai_service
from ...core.models import VoiceCommandResponse, TextCommandRequest, TextCommandResponse, OperationResponse

# Import the TaskManager service
from ...services.task_manager import task_manager # NEW IMPORT

# Create an API router specific to voice-related endpoints
router = APIRouter()

@router.post("/voice_command/", response_model=VoiceCommandResponse, summary="Process a voice command through ASR, LLM, and TTS")
async def process_voice_command_api(audio_file: UploadFile = File(...)):
    """
    **Endpoint to process a full voice command.**

    Receives an audio file (e.g., from ESP32 or frontend), performs the following:
    1.  **ASR (Automatic Speech Recognition):** Transcribes the audio to text using the AI service.
    2.  **LLM (Large Language Model):** Processes the transcribed text to generate an intelligent text response
        and attempts to identify if a structured task needs to be created.
    3.  **Task Creation:** If a task is identified by the LLM, it's created via the TaskManager.
    4.  **TTS (Text-to-Speech):** Synthesizes speech from the LLM's text response.

    Returns the transcribed text, LLM's text response, and a Base64-encoded audio response.
    """
    if not audio_file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload an audio file."
        )

    try:
        audio_bytes = await audio_file.read()

        # 1. ASR: Transcribe audio to text using the AI service
        transcribed_text = await ai_service.transcribe_audio(audio_bytes)

        # 2. LLM: Process the transcribed text, get response AND potential task
        llm_response_text, task_to_create = await ai_service.get_llm_response(transcribed_text)

        # 3. Task Creation: If LLM identified a task, create it
        if task_to_create:
            print(f"Detected task to create: {task_to_create.dict()}")
            task_manager.create_task(task_to_create)
            # You might want to modify llm_response_text here to confirm task creation
            # e.g., llm_response_text += " I've also created a task for this."

        # 4. TTS: Synthesize speech from the LLM's text response
        audio_response_bytes = await ai_service.synthesize_speech(llm_response_text)

        # Encode the generated audio response to Base64 for sending over JSON
        audio_response_b64 = base64.b64encode(audio_response_bytes).decode('utf-8')

        # Return the structured response
        return VoiceCommandResponse(
            transcribed_text=transcribed_text,
            llm_response_text=llm_response_text,
            audio_response_b64=audio_response_b64
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred during voice command processing: {str(e)}"
        )

@router.post("/text_command/", response_model=TextCommandResponse, summary="Process a text command directly with the LLM")
async def process_text_command_api(request: TextCommandRequest):
    """
    **Endpoint to process a text command directly.**

    Useful for testing the Natural Language Understanding (NLU) and
    Large Language Model (LLM) response generation without needing audio input.
    Also attempts to identify if a structured task needs to be created.

    Expects a JSON body with a 'text' field.
    """
    try:
        # LLM: Process the text command, get response AND potential task
        llm_response_text, task_to_create = await ai_service.get_llm_response(request.text)

        # Task Creation: If LLM identified a task, create it
        if task_to_create:
            print(f"Detected task to create from text: {task_to_create.dict()}")
            task_manager.create_task(task_to_create)
            # You might want to modify llm_response_text here to confirm task creation
            # e.g., llm_response_text += " I've also created a task for this."

        # Return the structured response
        return TextCommandResponse(
            input_text=request.text,
            llm_response_text=llm_response_text
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal server error occurred during text command processing: {str(e)}"
        )