import threading, tkinter as tk, sounddevice as sd
from faster_whisper import WhisperModel

def record():  # 2 seconds at 16 kHz
    return sd.rec(32000, samplerate=16000, channels=1, dtype="float32", blocking=True).flatten()

def show(subtitle, text):
    subtitle.config(text=f"🎙 {text}")

def listen(root, go, subtitle):
    model = WhisperModel("tiny.en", compute_type="int8")
    while True:
        segments, _ = model.transcribe(record(), vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments)
        if text:
            root.after(0, show, subtitle, text)
        if "next" in text.lower():
            root.after(0, go, 1)
        elif "back" in text.lower():
            root.after(0, go, -1)

def start(root, go):
    subtitle = tk.Label(root, text="🎙 Listening...", font=("Consolas", 12), wraplength=320)
    subtitle.pack(side="bottom")
    threading.Thread(target=listen, args=(root, go, subtitle), daemon=True).start()
