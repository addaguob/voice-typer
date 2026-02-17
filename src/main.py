import os
import time
import signal
import keyboard
import sounddevice as sd
import numpy as np
from recorder import AudioRecorder
from transcriber import Transcriber
from typer import Typer
from threading import Thread

# Global state
recorder = AudioRecorder()
transcriber: Transcriber | None = None # Load lazily or on startup
typer_obj = Typer()
is_processing = False

def handle_signal(signum, frame):
    """Handle external signals to toggle recording."""
    print(f"Received signal {signum}, toggling...")
    on_activate()

def play_sound(freq=440, duration=0.1):
    """Play a simple beep sound."""
    fs = 44100
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    try:
        sd.play(wave, fs)
        sd.wait()
    except Exception as e:
        print(f"Warning: Audio device unavailable for playback ({e}). Skipping beep.")
        time.sleep(duration)

def notify(title, message):
    """Send a system notification."""
    try:
        # Use a more robust way to send notifications, handling sudo/DBus issues if possible.
        # Or just suppress stderr to avoid confusion.
        os.system(f'notify-send "{title}" "{message}" 2>/dev/null')
    except Exception:
        pass

def load_transcriber():
    global transcriber
    transcriber = Transcriber(model_name="small.en")

def process_audio(audio_file):
    global is_processing
    try:
        print(f"Audio saved to {audio_file}")
        notify("Voice Typer", "Processing audio...")
        if transcriber:
            text = transcriber.transcribe(audio_file)
            print(f"Transcribed: {text}")
            if text:
                # Type the text
                typer_obj.type_text(text + " ")
                notify("Voice Typer", "Finished typing.")
            else:
                notify("Voice Typer", "No speech detected.")
    except Exception as e:
        print(f"Error during processing: {e}")
        notify("Voice Typer", f"Error: {e}")
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)
        is_processing = False
        play_sound(880, 0.1) # Double beep to signify end
        play_sound(880, 0.1)

def on_activate():
    global is_processing
    
    if recorder.is_recording:
        print("Stop command received.")
        play_sound(440, 0.1)  # Low beep for stop
        audio_file = recorder.stop()
        if audio_file:
            is_processing = True
            # Run processing in a separate thread
            t = Thread(target=process_audio, args=(audio_file,))
            t.start()
    else:
        if is_processing:
            print("Still processing previous audio, please wait.")
            play_sound(200, 0.2) # Error beep
            return
        # Start recording
        print("Start command received.")
        play_sound(880, 0.1) # High beep for start
        try:
            recorder.start()
            notify("Voice Typer", "Listening...")
        except Exception as e:
            msg = f"Failed to start recording: {e}"
            print(msg)
            notify("Voice Typer", msg)
            play_sound(200, 0.5) # Error beep

def main():
    print("Initializing Voice Typer...")
    load_transcriber()
    
    print("Listening for Ctrl+Alt+Space...")
    try:
        # Register the hotkey
        keyboard.add_hotkey('ctrl+alt+space', on_activate, suppress=False)
        
        # Keep Super+Space as an alternative/legacy if it works for you
        # keyboard.add_hotkey('windows+space', on_activate, suppress=False)
        
        notify("Voice Typer", "Ready! Press Ctrl+Alt+Space to start.")
        
        keyboard.wait()
    except ImportError:
        print("Error: Library not found. Ensure you are running with sudo if required.")
    except Exception as e:
        print(f"Error setting hotkey: {e}")
        print("Try running with sudo.")

if __name__ == "__main__":
    # Register signal handler for toggling via external command
    signal.signal(signal.SIGUSR1, handle_signal)
    
    # Write PID to file so external scripts can find us
    pid_file = "/tmp/voice-typer.pid"
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()))
    
    try:
        main()
    finally:
        if os.path.exists(pid_file):
            os.remove(pid_file)
