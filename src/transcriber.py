import whisper
import os

class Transcriber:
    def __init__(self, model_name="turbo"):
        print(f"Loading Whisper model '{model_name}'...")
        self.model = whisper.load_model(model_name)
        print("Model loaded.")

    def transcribe(self, audio_path):
        if not audio_path or not os.path.exists(audio_path):
            return ""
        
        result = self.model.transcribe(audio_path)
        return result["text"].strip()
