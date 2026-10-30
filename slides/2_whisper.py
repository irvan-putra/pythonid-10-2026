import threading, importlib, tkinter as tk, sounddevice as sd
from faster_whisper import WhisperModel
mqtt = importlib.import_module("5_mqtt")  # file names start with the slide number

def listen(root, go, subtitle):
    model, transcript = WhisperModel("tiny.en", compute_type="int8"), ""
    while True:
        audio = sd.rec(32000, samplerate=16000, channels=1, dtype="float32", blocking=True)
        segments, _ = model.transcribe(audio.flatten(), vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments)
        if text:
            transcript += " " + text  # retained: a dashboard opened later still gets all of it
            mqtt.publish("speech", transcript, retain=True)
            root.after(0, lambda text=text: subtitle.config(text=f"🎙 {text}"))
        if "next" in text.lower():
            root.after(0, go, 1)
        elif "back" in text.lower():
            root.after(0, go, -1)

def start(root, go):
    subtitle = tk.Label(root, text="🎙 Listening...", font=("Consolas", 12), wraplength=320)
    subtitle.pack(side="bottom")
    threading.Thread(target=listen, args=(root, go, subtitle), daemon=True).start()
