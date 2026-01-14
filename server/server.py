from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import pytesseract
from PIL import ImageGrab
import base64
import io
import speech_recognition as sr
from pydub import AudioSegment

app = FastAPI()

# Allow local connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyDevz1Zxj17nh3YYAZw_sHd7w5goSUWqhg")

recognizer = sr.Recognizer()  # single recognizer

@app.websocket("/")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")
            content = data.get("content", "")
            
            # ----------------------------
            # AUDIO MESSAGE
            # ----------------------------
            if msg_type == "audio":
                # decode base64
                audio_bytes = base64.b64decode(content)
                audio_file = io.BytesIO(audio_bytes)
                
                # convert to WAV
                audio_segment = AudioSegment.from_file(audio_file)
                wav_file = io.BytesIO()
                audio_segment.export(wav_file, format="wav", codec="pcm_s16le")
                wav_file.seek(0)

                # transcribe
                with sr.AudioFile(wav_file) as source:
                    audio_data = recognizer.record(source)
                    try:
                        transcription = recognizer.recognize_google(audio_data)
                        print(f"[Audio Transcription] {transcription}")  # log only
                    except sr.UnknownValueError:
                        transcription = "[Could not transcribe audio]"
                        print("[Audio Transcription] Could not transcribe audio")
                    except sr.RequestError as e:
                        transcription = f"[Speech API error: {e}]"
                        print(f"[Audio Transcription] Speech API error: {e}")

                # send transcription back to overlay
                await ws.send_text(f"[Audio] {transcription}")

            # ----------------------------
            # TEXT MESSAGE
            # ----------------------------
            elif msg_type == "text":
                user_text = content

                # grab screen ONLY for text messages
                screen_text = pytesseract.image_to_string(ImageGrab.grab())

                # build Gemini prompt
                prompt = f"User query:\n{user_text}\n\nScreen contents:\n{screen_text}"

                # generate response
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )

                await ws.send_text(response.text)

            else:
                # ignore unknown types
                await ws.send_text("[Server] Unknown message type")

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print("Server Error:", e)
