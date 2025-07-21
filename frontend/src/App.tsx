// conci-ai-assistant/frontend/src/App.tsx
import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css'; // You will create/update this file for basic styling

// Define the base URL for your FastAPI backend.
// It reads from .env.development or .env.production, or defaults to localhost.
const API_BASE_URL = import.meta.env.VITE_APP_API_BASE_URL || 'http://localhost:8000/api/v1';
function App() {
  // State variables for text interaction
  const [textInput, setTextInput] = useState<string>('');
  const [textResponse, setTextResponse] = useState<string>('');

  // State variables for voice interaction
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [audioResponseUrl, setAudioResponseUrl] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // State variables for PMS/POS forms
  const [spaBookingDate, setSpaBookingDate] = useState<string>('');
  const [spaBookingTime, setSpaBookingTime] = useState<string>('');
  const [spaBookingService, setSpaBookingService] = useState<string>('');
  const [spaBookingCustomerName, setSpaBookingCustomerName] = useState<string>('');
  const [spaBookingResponse, setSpaBookingResponse] = useState<string>('');

  const [hotsosDescription, setHotsosDescription] = useState<string>('');
  const [hotsosPriority, setHotsosPriority] = useState<string>('medium');
  const [hotsosResponse, setHotsosResponse] = useState<string>('');

  // --- Text Interaction Handlers ---
  const handleTextSubmit = async () => {
    setTextResponse("Processing text command...");
    try {
      const response = await axios.post(`${API_BASE_URL}/text_command/`, { text: textInput });
      setTextResponse(response.data.llm_response_text);
    } catch (error) {
      console.error("Error sending text command:", error);
      setTextResponse("Error processing your text command. Please check console for details.");
    }
  };

  // --- Voice Interaction Handlers ---
  const startRecording = async () => {
    try {
      // Request access to the user's microphone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = []; // Clear previous audio chunks

      // Event listener for when audio data is available
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      // Event listener for when recording stops
      mediaRecorderRef.current.onstop = async () => {
        // Create a Blob from the audio chunks (assuming WAV format for simplicity with FastAPI mock)
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setIsRecording(false);
        stream.getTracks().forEach(track => track.stop()); // Stop microphone stream

        // Immediately send the recorded audio to the backend
        await sendAudioToBackend(audioBlob);
      };

      mediaRecorderRef.current.start(); // Start recording
      setIsRecording(true);
      setAudioResponseUrl(null); // Clear previous audio response
      setTextResponse("Recording voice command...");
    } catch (err) {
      console.error('Error accessing microphone:', err);
      setTextResponse("Failed to access microphone. Please check permissions.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop(); // Stop recording
    }
  };

  const sendAudioToBackend = async (blob: Blob) => {
    setTextResponse("Sending audio to backend for processing...");
    try {
      const formData = new FormData();
      formData.append('audio_file', blob, 'recording.wav'); // Append the audio blob as a file

      // Send the audio file to the FastAPI voice command endpoint
      const response = await axios.post(`${API_BASE_URL}/voice_command/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Important for file uploads
        },
      });

      // Update text response with transcribed text and LLM response
      setTextResponse(`Transcribed: "${response.data.transcribed_text}"\nConci: "${response.data.llm_response_text}"`);

      // If the backend returns base64 encoded audio, create a URL to play it
      if (response.data.audio_response_b64) {
        const audioData = `data:audio/wav;base64,${response.data.audio_response_b64}`; // Assume WAV from mock
        setAudioResponseUrl(audioData);
      }
    } catch (error) {
      console.error("Error sending voice command:", error);
      setTextResponse("Error processing your voice command. Please check console for details.");
      setAudioResponseUrl(null);
    }
  };

  // --- PMS/POS Form Handlers ---
  const handleSpaBookingSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission
    setSpaBookingResponse("Attempting to book spa slot...");
    try {
      const response = await axios.post(`${API_BASE_URL}/book_spa_slot/`, {
        date: spaBookingDate,
        time: spaBookingTime,
        service: spaBookingService,
        customer_name: spaBookingCustomerName,
      });
      setSpaBookingResponse(response.data.message);
    } catch (error) {
      console.error("Error booking spa slot:", error);
      setSpaBookingResponse("Error booking spa slot. Please check console for details.");
    }
  };

  const handleHotsosSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission
    setHotsosResponse("Attempting to create HotSOS task...");
    try {
      const response = await axios.post(`${API_BASE_URL}/create_hotsos_task/`, {
        description: hotsosDescription,
        priority: hotsosPriority,
      });
      setHotsosResponse(response.data.message);
    } catch (error) {
      console.error("Error creating HotSOS task:", error);
      setHotsosResponse("Error creating HotSOS task. Please check console for details.");
    }
  };

  return (
    <div className="App p-8 bg-gray-100 min-h-screen font-sans">
      <header className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">Conci AI Assistant Demo</h1>
        <p className="text-lg text-gray-600">Interact with the backend via text, voice, and mock PMS/POS forms.</p>
      </header>

      {/* Text Interaction Section */}
      <section className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">Text Interaction</h2>
        <textarea
          className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
          placeholder="Enter your command here (e.g., 'Book a spa appointment' or 'Fix a light in room 101')..."
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          rows={4}
        ></textarea>
        <button
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-300 ease-in-out"
          onClick={handleTextSubmit}
        >
          Send Text Command
        </button>
        {textResponse && (
          <p className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-md text-blue-800">
            <strong>Response:</strong> {textResponse}
          </p>
        )}
      </section>

      {/* Voice Interaction Section */}
      <section className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">Voice Interaction</h2>
        <button
          className={`w-full py-3 px-4 rounded-md text-white font-bold transition duration-300 ease-in-out ${
            isRecording ? 'bg-red-500 hover:bg-red-600' : 'bg-green-600 hover:bg-green-700'
          }`}
          onClick={isRecording ? stopRecording : startRecording}
          disabled={!navigator.mediaDevices || (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording')}
        >
          {isRecording ? 'Stop Recording (Click to send)' : 'Start Recording Voice Command'}
        </button>
        {audioResponseUrl && (
          <div className="mt-4 text-center">
            <h3 className="text-xl font-medium text-gray-700 mb-2">Listen to Conci's Response:</h3>
            <audio controls src={audioResponseUrl} className="w-full"></audio>
          </div>
        )}
        <p className="mt-4 text-sm text-gray-500 text-center">
          (Microphone access required for voice interaction. Click 'Start Recording' then 'Stop Recording' to send.)
        </p>
      </section>

      {/* Spa Booking Form Section */}
      <section className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">Mock Spa Booking</h2>
        <form onSubmit={handleSpaBookingSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="spaDate" className="block text-gray-700 text-sm font-bold mb-2">Date:</label>
            <input
              type="date"
              id="spaDate"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={spaBookingDate}
              onChange={(e) => setSpaBookingDate(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="spaTime" className="block text-gray-700 text-sm font-bold mb-2">Time:</label>
            <input
              type="time"
              id="spaTime"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={spaBookingTime}
              onChange={(e) => setSpaBookingTime(e.target.value)}
              required
            />
          </div>
          <div className="md:col-span-2">
            <label htmlFor="spaService" className="block text-gray-700 text-sm font-bold mb-2">Service:</label>
            <input
              type="text"
              id="spaService"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Deep Tissue Massage"
              value={spaBookingService}
              onChange={(e) => setSpaBookingService(e.target.value)}
              required
            />
          </div>
          <div className="md:col-span-2">
            <label htmlFor="customerName" className="block text-gray-700 text-sm font-bold mb-2">Customer Name:</label>
            <input
              type="text"
              id="customerName"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Jane Doe"
              value={spaBookingCustomerName}
              onChange={(e) => setSpaBookingCustomerName(e.target.value)}
              required
            />
          </div>
          <div className="md:col-span-2">
            <button
              type="submit"
              className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 transition duration-300 ease-in-out"
            >
              Book Spa Slot
            </button>
          </div>
        </form>
        {spaBookingResponse && (
          <p className="mt-4 p-3 bg-purple-50 border border-purple-200 rounded-md text-purple-800">
            <strong>Response:</strong> {spaBookingResponse}
          </p>
        )}
      </section>

      {/* HotSOS Task Creation Form Section */}
      <section className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-semibold text-gray-700 mb-4">Mock HotSOS Task Creation</h2>
        <form onSubmit={handleHotsosSubmit} className="grid grid-cols-1 gap-4">
          <div>
            <label htmlFor="hotsosDesc" className="block text-gray-700 text-sm font-bold mb-2">Task Description:</label>
            <textarea
              id="hotsosDesc"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Leaking faucet in Room 305. Needs immediate attention."
              value={hotsosDescription}
              onChange={(e) => setHotsosDescription(e.target.value)}
              rows={3}
              required
            ></textarea>
          </div>
          <div>
            <label htmlFor="hotsosPriority" className="block text-gray-700 text-sm font-bold mb-2">Priority:</label>
            <select
              id="hotsosPriority"
              className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={hotsosPriority}
              onChange={(e) => setHotsosPriority(e.target.value)}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <div>
            <button
              type="submit"
              className="w-full bg-orange-600 text-white py-2 px-4 rounded-md hover:bg-orange-700 transition duration-300 ease-in-out"
            >
              Create HotSOS Task
            </button>
          </div>
        </form>
        {hotsosResponse && (
          <p className="mt-4 p-3 bg-orange-50 border border-orange-200 rounded-md text-orange-800">
            <strong>Response:</strong> {hotsosResponse}
          </p>
        )}
      </section>
    </div>
  );
}

export default App;