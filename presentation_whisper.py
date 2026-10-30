import threading, tkinter as tk, sounddevice as sd, presentation_redis
from faster_whisper import WhisperModel

def listen(root, go, sub):
    model = WhisperModel("tiny.en", compute_type="int8")
    while True:
        audio = sd.rec(32000, samplerate=16000, channels=1, dtype="float32", blocking=True)
        segs, _ = model.transcribe(audio.flatten(), vad_filter=True)
        text = " ".join(s.text.strip() for s in segs)
        if text:
            presentation_redis.live["text"] += " " + text
            root.after(0, lambda t=text: sub.config(text=f"🎙 {t}"))
        if "next" in text.lower():
            root.after(0, go, 1)
        elif "back" in text.lower():
            root.after(0, go, -1)

def start(root, go):
    sub = tk.Label(root, text="🎙 Listening...", font=("Consolas", 12))
    sub.pack(side="bottom", pady=10)
    threading.Thread(target=listen, args=(root, go, sub), daemon=True).start()
