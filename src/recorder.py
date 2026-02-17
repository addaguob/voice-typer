import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os

class AudioRecorder:
    def __init__(self, fs=16000):
        self.fs = fs
        self.recording = []
        self.is_recording = False
        self.stream = None

    def start(self):
        if self.is_recording:
            return
        print("Recording started...")
        self.is_recording = True
        self.recording = []
        # Non-blocking stream
        self.stream = sd.InputStream(samplerate=self.fs, channels=1, callback=self.callback)
        self.stream.start()

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.recording.append(indata.copy())

    def stop(self):
        if not self.is_recording:
            return None
        print("Recording stopped.")
        self.is_recording = False
        self.stream.stop()
        self.stream.close()
        
        # Concatenate and save
        if not self.recording:
            return None
            
        audio_data = np.concatenate(self.recording, axis=0)
        
        # Create temp file
        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        wav.write(path, self.fs, audio_data)
        return path
