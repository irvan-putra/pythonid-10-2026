import tkinter as tk
import presentation_whisper, presentation_yolo, presentation_streamlit, presentation_redis

slides = [
    "Edge AI & Multimodal Applications in Python",
    open(__file__).read(),
    open("presentation_whisper.py").read(),
    open("presentation_yolo.py").read(),
    open("presentation_streamlit.py").read(),
    open("presentation_redis.py").read(),
]
i = 0

root = tk.Tk()
root.title(slides[0])
root.geometry("1100x600")
lbl = tk.Label(root, font=("Consolas", 13), justify="left")
lbl.pack(side="left", expand=True)

def go(step=0):
    global i
    i = presentation_redis.live["slide"] = (i + step) % len(slides)
    lbl.config(text=slides[i])

presentation_whisper.start(root, go)
presentation_yolo.start(root)
presentation_streamlit.start()
root.bind("<Left>", lambda e: go(-1))
root.bind("<Right>", lambda e: go(1))
go()
root.mainloop()
