import sys, pathlib, importlib, tkinter as tk

sys.path.insert(0, "slides")  # one file per slide, shown in name order
files = sorted(pathlib.Path("slides").glob("slide_*"))  # .py, plus the .conf and .html they use
slides = [("presentation.py", open(__file__, encoding="utf-8").read())]
slides += [(f"slides/{path.name}", path.read_text(encoding="utf-8")) for path in files]
slide = 0

root = tk.Tk()
root.title("Edge AI & Multimodal Applications in Python")
root.geometry("1100x600")
label = tk.Label(root, font=("Consolas", 13), justify="left", anchor="w")
panel = tk.Frame(root)  # right column: file name, camera, phone LED, subtitle
panel.pack(side="right", padx=20)
filename = tk.Label(panel, font=("Consolas", 12, "bold"))
filename.pack()

def go(step=0):
    global slide
    slide = (slide + step) % len(slides)
    filename.config(text=slides[slide][0])
    label.config(text=slides[slide][1])

modules = [importlib.import_module(path.stem) for path in files if path.suffix == ".py"]
for module in modules:  # import all first, then each slide starts its part of the demo
    if hasattr(module, "start"):
        module.start(panel, go)
label.pack(side="left", expand=True, fill="both", padx=10)  # last: fills the space left over
root.bind("<Left>", lambda event: go(-1))
root.bind("<Right>", lambda event: go(1))
go()
root.mainloop()
