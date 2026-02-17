import pyautogui

class Typer:
    def __init__(self):
        pass

    def type_text(self, text):
        if not text:
            return
        print(f"Typing: {text}")
        pyautogui.write(text)
