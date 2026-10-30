import queue, threading, tkinter as tk, sounddevice as sd, slide_5_mqtt as mqtt
from faster_whisper import WhisperModel

phone = queue.Queue()  # 2-second chunks from the phone mic (slide_7_sensor.py)

def listen(root, go, subtitle):
    model, transcript, from_phone = WhisperModel("tiny.en", compute_type="int8"), "", False
    while True:
        try:  # the phone mic takes over while it streams, then the laptop mic again
            audio, from_phone = phone.get(timeout=3 if from_phone else 0.01), True
        except queue.Empty:  # 2 seconds from the laptop mic
            from_phone = False
            audio = sd.rec(32000, samplerate=16000, channels=1, dtype="float32", blocking=True)
        segments, _ = model.transcribe(audio.flatten(), vad_filter=True)
        text = " ".join(segment.text.strip() for segment in segments)
        if text:
            transcript += " " + text  # retained: a dashboard opened later still gets all of it
            mqtt.publish("speech", transcript, retain=True)
            line = f"{'📱' if from_phone else '🎙'} {text}"
            root.after(0, lambda line=line: subtitle.config(text=line))
        if "next" in text.lower():
            root.after(0, go, 1)
        elif "back" in text.lower():
            root.after(0, go, -1)

def start(root, go):
    subtitle = tk.Label(root, text="🎙 Listening...", font=("Consolas", 12), wraplength=320)
    subtitle.pack(side="bottom")
    threading.Thread(target=listen, args=(root, go, subtitle), daemon=True).start()
