import tkinter as tk
import slide_whisper, slide_yolo, slide_broker, slide_mqtt, slide_streamlit

read = lambda path: open(path, encoding="utf-8").read()
slides = [
    "Edge AI & Multimodal Applications in Python",
    read(__file__),
    read("slide_whisper.py"),
    read("slide_yolo.py"),
    read("slide_broker.py"),
    read("slide_mqtt.py"),
    read("phone/sensor_termux.py"),
    read("slide_streamlit.py"),
]
slide = 0

root = tk.Tk()
root.title(slides[0])
root.geometry("1100x600")
label = tk.Label(root, font=("Consolas", 13), justify="left", anchor="w")

def go(step=0):
    global slide
    slide = (slide + step) % len(slides)
    label.config(text=slides[slide])

slide_whisper.start(root, go)
slide_yolo.start(root)
slide_broker.start()
slide_mqtt.start(root)
label.pack(side="left", expand=True, fill="both", padx=10)  # last: fills the space left over
slide_streamlit.start()
root.bind("<Left>", lambda event: go(-1))
root.bind("<Right>", lambda event: go(1))
go()
root.mainloop()
