import tkinter as tk
import presentation_whisper, presentation_yolo, presentation_streamlit

read = lambda path: open(path, encoding="utf-8").read()
slides = [
    "Edge AI & Multimodal Applications in Python",
    read(__file__),
    read("presentation_whisper.py"),
    read("presentation_yolo.py"),
    read("presentation_streamlit.py"),
    read("presentation_redis.py"),
]
slide = 0

root = tk.Tk()
root.title(slides[0])
root.geometry("1100x600")
label = tk.Label(root, font=("Consolas", 13), justify="left")
label.pack(side="left", expand=True)

def go(step=0):
    global slide
    slide = (slide + step) % len(slides)
    label.config(text=slides[slide])

presentation_whisper.start(root, go)
presentation_yolo.start(root)
presentation_streamlit.start()
root.bind("<Left>", lambda event: go(-1))
root.bind("<Right>", lambda event: go(1))
go()
root.mainloop()
