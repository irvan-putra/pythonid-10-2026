import sys, tkinter as tk
sys.path.insert(0, "laptop")  # the slide modules live in laptop/
import whisper, yolo, broker, mqtt, dashboard

read = lambda path: open(path, encoding="utf-8").read()
slides = [
    "Edge AI & Multimodal Applications in Python",
    read(__file__),
    *map(read, ["laptop/whisper.py", "laptop/yolo.py", "laptop/broker.py"]),
    *map(read, ["laptop/mqtt.py", "phone/termux.py", "laptop/dashboard.py"]),
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

panel = tk.Frame(root)  # right column, top to bottom: camera, phone LED, subtitle
panel.pack(side="right", padx=20)
yolo.start(panel)
broker.start()
mqtt.start(panel)
whisper.start(panel, go)
label.pack(side="left", expand=True, fill="both", padx=10)  # last: fills the space left over
dashboard.start()
root.bind("<Left>", lambda event: go(-1))
root.bind("<Right>", lambda event: go(1))
go()
root.mainloop()
