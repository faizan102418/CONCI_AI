# CONCI AI Assistant

## Overview
The CONCI AI Assistant is an innovative project designed to streamline hotel operations using voice commands and artificial intelligence. It acts as an intelligent assistant for both guests and hotel staff, automating common requests and providing a centralized dashboard for task management.

The project is structured into three main components: a FastAPI backend, a React web frontend, and ESP32-S3 firmware for voice interaction.

## Features
### Voice Command Processing:
- **ASR (Automatic Speech Recognition):** Transcribes spoken guest requests into text using the Whisper AI model.
- **LLM (Large Language Model) Integration:** Processes transcribed text to understand intent, generate intelligent responses, and identify actionable tasks using the Mistral 7B model.
- **TTS (Text-to-Speech):** Synthesizes spoken responses from the LLM back to the user using the Coqui TTS model.
- **PMS/POS System Integration (Mock):** Simulates interactions with Property Management Systems (PMS) and Point of Sale (POS) systems for tasks like spa bookings and HotSOS maintenance task creation.

### Centralized Receptionist Dashboard:
- Displays guest requests identified by the AI in real-time.
- Allows receptionists to view, assign, and update the status of tasks (e.g., pending, assigned, completed, cancelled).
- Manages a list of mock staff members for task assignment.

### ESP32-S3 Integration (Conceptual):
Outlines the firmware logic for an ESP32-S3 device to act as the voice interface in guest rooms, featuring:
- Wake word detection ("Hey Conci").
- Audio capture and streaming to the backend.
- Audio playback of AI-generated responses.

## Architecture
The project follows a modular architecture:

### Backend (FastAPI - Python):
- Provides RESTful API endpoints for voice processing, PMS/POS interactions, and dashboard management.
- Hosts the AI models (Whisper, Mistral, Coqui TTS).
- Manages in-memory task data for the dashboard.

### Frontend (React - TypeScript/Vite):
- A web-based user interface for demonstrating text and voice interactions with the AI.
- Includes a dedicated "Receptionist Dashboard" to visualize and manage tasks.

### Embedded (ESP32-S3 - C/C++/ESP-IDF):
- (Conceptual) Firmware for the ESP32-S3 microcontroller to handle real-world voice input and output.

## Project Structure
conci-ai-assistant/
├── backend/
│ ├── src/
│ │ ├── api/
│ │ │ └── v1/
│ │ │ ├── dashboard.py # API routes for task management
│ │ │ ├── pms_pos.py # API routes for mock PMS/POS
│ │ │ └── voice.py # API routes for voice/text commands
│ │ ├── core/
│ │ │ ├── config.py # Application settings
│ │ │ ├── models.py # Pydantic data models
│ │ │ └── exceptions.py # Custom exceptions
│ │ ├── services/
│ │ │ ├── ai_models.py # AI model wrappers (Whisper, Mistral, Coqui TTS)
│ │ │ ├── mock_pms_pos.py # Mock PMS/POS service
│ │ │ └── task_manager.py # In-memory task management service
│ │ └── main.py # FastAPI application entry point
│ └── requirements.txt # Python dependencies
├── frontend/
│ ├── public/
│ ├── src/
│ │ ├── assets/
│ │ ├── components/
│ │ │ └── Dashboard.tsx # Receptionist Dashboard UI component
│ │ ├── App.css # Main application CSS (Tailwind directives)
│ │ ├── App.tsx # Main React component
│ │ ├── main.tsx # React entry point
│ │ └── index.css # Global CSS (Tailwind directives)
│ ├── .env # Frontend environment variables
│ ├── index.html
│ ├── package.json # Node.js dependencies
│ ├── postcss.config.js # Tailwind CSS PostCSS config
│ ├── tailwind.config.js # Tailwind CSS configuration
│ ├── tsconfig.json
│ └── vite.config.ts
├── embedded/
│ └── esp32-s3/
│ └── src/
│ └── main/ # ESP32-S3 firmware source (C/C++)
│ ├── main.c # Main firmware logic
│ ├── CMakeLists.txt
│ └── sdkconfig
├── .gitignore
└── README.md

## Setup and Running the Project
Follow these steps to get the CONCI AI Assistant running on your local machine.

### Prerequisites
- Git: For cloning the repository.
- Python 3.9+: For the FastAPI backend.
- Node.js (LTS recommended) & npm: For the React frontend.
- ESP-IDF (Optional): If you plan to work with the ESP32-S3 firmware.

###  Clone the Repository
```bash
git clone https://github.com/faizan102418/CONCI_AI.git
cd CONCI_AI
License
This project is open-source and available under the MIT License. See the LICENSE file for more details.
