# Voice Typer

A simple voice typing application for Linux Mint using OpenAI Whisper (using the `turbo` model for high accuracy).

## Prerequisites

- Python 3.8+
- `ffmpeg` (required for Whisper):
  ```bash
  sudo apt install ffmpeg
  ```

## Usage

1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   # You may need sudo for global hotkey support on Linux
   sudo .venv/bin/python src/main.py
   # OR if running without venv
   sudo python3 src/main.py
   ```
4. Press `Ctrl+Alt+Space` to toggle recording. (Note: The first run will download the large `turbo` model, which may take some time).
5. Speak, and the text will be typed into the active window.

## Troubleshooting

- If `Ctrl+Alt+Space` does not trigger, ensure you are running with `sudo`.
- If typing doesn't work, ensure you focus the text field immediately.

