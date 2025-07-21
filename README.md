CONCI AI Assistant
Overview
The CONCI AI Assistant is an innovative project designed to streamline hotel operations using voice commands and artificial intelligence. It acts as an intelligent assistant for both guests and hotel staff, automating common requests and providing a centralized dashboard for task management.

The project is structured into three main components: a FastAPI backend, a React web frontend, and ESP32-S3 firmware for voice interaction.

Features
Voice Command Processing:

ASR (Automatic Speech Recognition): Transcribes spoken guest requests into text using the Whisper AI model.

LLM (Large Language Model) Integration: Processes transcribed text to understand intent, generate intelligent responses, and identify actionable tasks using the Mistral 7B model.

TTS (Text-to-Speech): Synthesizes spoken responses from the LLM back to the user using the Coqui TTS model.

PMS/POS System Integration (Mock): Simulates interactions with Property Management Systems (PMS) and Point of Sale (POS) systems for tasks like spa bookings and HotSOS maintenance task creation.

Centralized Receptionist Dashboard:

Displays guest requests identified by the AI in real-time.

Allows receptionists to view, assign, and update the status of tasks (e.g., pending, assigned, completed, cancelled).

Manages a list of mock staff members for task assignment.

ESP32-S3 Integration (Conceptual): Outlines the firmware logic for an ESP32-S3 device to act as the voice interface in guest rooms, featuring:

Wake word detection ("Hey Conci").

Audio capture and streaming to the backend.

Audio playback of AI-generated responses.

Architecture
The project follows a modular architecture:

Backend (FastAPI - Python):

Provides RESTful API endpoints for voice processing, PMS/POS interactions, and dashboard management.

Hosts the AI models (Whisper, Mistral, Coqui TTS).

Manages in-memory task data for the dashboard.

Frontend (React - TypeScript/Vite):

A web-based user interface for demonstrating text and voice interactions with the AI.

Includes a dedicated "Receptionist Dashboard" to visualize and manage tasks.

Embedded (ESP32-S3 - C/C++/ESP-IDF):

(Conceptual) Firmware for the ESP32-S3 microcontroller to handle real-world voice input and output.

conci-ai-assistant/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── dashboard.py       # API routes for task management
│   │   │       ├── pms_pos.py         # API routes for mock PMS/POS
│   │   │       └── voice.py           # API routes for voice/text commands
│   │   ├── core/
│   │   │   ├── config.py            # Application settings
│   │   │   └── models.py            # Pydantic data models
│   │   ├── services/
│   │   │   ├── ai_models.py         # AI model wrappers (Whisper, Mistral, Coqui TTS)
│   │   │   ├── mock_pms_pos.py      # Mock PMS/POS service
│   │   │   └── task_manager.py      # In-memory task management service
│   │   └── main.py                  # FastAPI application entry point
│   └── requirements.txt             # Python dependencies
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   └── Dashboard.tsx        # Receptionist Dashboard UI component
│   │   ├── App.css                  # Main application CSS (Tailwind directives)
│   │   ├── App.tsx                  # Main React component
│   │   ├── main.tsx                 # React entry point
│   │   └── index.css                # Global CSS (Tailwind directives)
│   ├── .env                         # Frontend environment variables
│   ├── index.html
│   ├── package.json                 # Node.js dependencies
│   ├── postcss.config.js            # Tailwind CSS PostCSS config
│   ├── tailwind.config.js           # Tailwind CSS configuration
│   ├── tsconfig.json
│   └── vite.config.ts
├── embedded/
│   └── esp32-s3/
│       └── src/
│           └── main/                # ESP32-S3 firmware source (C/C++)
│               ├── main.c           # Main firmware logic
│               ├── CMakeLists.txt
│               └── sdkconfig
├── .gitignore
└── README.md

Setup and Running the Project
Follow these steps to get the CONCI AI Assistant running on your local machine.

Prerequisites
Git: For cloning the repository.

Python 3.9+: For the FastAPI backend.

Node.js (LTS recommended) & npm: For the React frontend.

ESP-IDF (Optional): If you plan to work with the ESP32-S3 firmware.

1. Clone the Repository
git clone https://github.com/faizan102418/CONCI_AI.git
cd CONCI_AI

2. Backend Setup (FastAPI)
Navigate to the backend directory:

cd backend

Create a Python virtual environment:

python -m venv venv

Activate the virtual environment:

Windows (PowerShell):

.\venv\Scripts\Activate.ps1

macOS/Linux:

source venv/bin/activate

Install Python dependencies:

pip install -r requirements.txt

Note: This step will download large AI models (Whisper, Mistral, Coqui TTS). This can take a considerable amount of time and requires significant disk space and RAM. If you encounter ModuleNotFoundError for soundfile or TypeError related to ctypes in whisper, ensure ffmpeg is installed on your system and its bin directory is added to your system's PATH.

Create a .env file for backend settings:
In the backend/ directory, create a file named .env (this file is ignored by Git for security reasons). You can leave it empty for now, as default values are provided in backend/src/core/config.py.

3. Frontend Setup (React)
Navigate to the frontend directory:

cd ../frontend

Install Node.js dependencies:

npm install

This will install React, Vite, Axios, Tailwind CSS, and other necessary packages.

Create a .env file for frontend settings:
In the frontend/ directory, create a file named .env.
Add the following line to specify your backend API URL:

VITE_APP_API_BASE_URL=http://localhost:8000/api/v1

Initialize Tailwind CSS configuration:

Install Tailwind CSS CLI (if not already working via npm install):

npm install -D tailwindcss postcss autoprefixer

Generate Tailwind config files:

npx tailwindcss init -p

This command creates tailwind.config.js and postcss.config.js in your frontend/ directory.

Configure tailwind.config.js: Open frontend/tailwind.config.js and ensure the content array includes paths to your React components:

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

Update CSS entry points: Ensure frontend/src/App.css and frontend/src/index.css have the Tailwind directives at the top:

@tailwind base;
@tailwind components;
@tailwind utilities;
/* ... rest of your CSS */

Note: If you faced persistent issues with Tailwind CSS setup, the UI might appear unstyled. The core functionality will still work.

4. ESP32-S3 Firmware Setup (Conceptual)
This section outlines the steps for the embedded development. Actual implementation requires hardware and familiarity with ESP-IDF.

Install ESP-IDF: Follow the official ESP-IDF Programming Guide for your operating system.

Hardware Connections: Connect your I2S microphone and I2S DAC to your ESP32-S3 development board.

Implement Firmware Logic:

Navigate to embedded/esp32-s3/src/main/.

Implement wifi_manager.c, audio_capture.c, wake_word.c, http_client.c, and audio_playback.c based on ESP-IDF examples and the conceptual main.c provided in the project.

Configure CMakeLists.txt and sdkconfig to include necessary components.

Build and Flash: Use idf.py build and idf.py flash from the embedded/esp32-s3/ directory.

Monitor: Use idf.py monitor for debugging serial output.

How to Run the Application
To run the full application, you need to start both the backend and frontend servers in separate terminal windows/tabs.

Start the Backend Server:

Open a new terminal/tab.

Navigate to conci-ai-assistant/backend/.

Activate your virtual environment:

Windows (PowerShell): .\venv\Scripts\Activate.ps1

macOS/Linux: source venv/bin/activate

Run the FastAPI application:

uvicorn src.main:app --reload

The server will start on http://127.0.0.1:8000. Wait for the AI models to load (indicated by "All AI models loaded successfully!" in the terminal).

Start the Frontend Development Server:

Open another new terminal/tab.

Navigate to conci-ai-assistant/frontend/.

Run the React development server:

npm run dev

The frontend will typically be served on http://localhost:5173/.

Access the Application:
Open your web browser and go to http://localhost:5173/.

Using the Demo UI
Text Interaction: Type commands (e.g., "I need a towel in room 203", "Fix the light in room 101") and click "Send Text Command". Observe the AI's response and check the Receptionist Dashboard for new tasks.

Voice Interaction: Click "Start Recording Voice Command", speak your request, then click "Stop Recording". The AI will transcribe, respond, and (if applicable) create a task. You should hear the AI's response (if TTS is working).

Mock PMS/POS Forms: Use the "Mock Spa Booking" and "Mock HotSOS Task Creation" forms to simulate direct system integrations.

Receptionist Dashboard: View newly created tasks, assign them to staff, and update their status (e.g., "Mark as Completed"). The dashboard automatically polls for updates.

Future Enhancements
Database Integration: Replace the in-memory task manager with a persistent database (e.g., PostgreSQL, MongoDB) for real-world data storage.

Real PMS/POS APIs: Integrate with actual hotel management and task systems.

Advanced LLM Capabilities: Implement more sophisticated NLU and dialogue management for complex guest interactions.

Improved ESP32 Firmware: Robust error handling, over-the-air (OTA) updates, and more efficient audio processing.

Authentication & Authorization: Secure API endpoints and dashboard access for different user roles.

Real-time Updates: Use WebSockets for immediate dashboard updates instead of polling.

Custom Wake Word Training: Train a highly accurate "Hey Conci" wake word model for the ESP32.

License
This project is open-source and available under the MIT License. See the LICENSE file for more details.
