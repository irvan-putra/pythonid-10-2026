import sys, pathlib, importlib, tkinter as tk

sys.path.insert(0, "slides")
number = lambda path: int(path.name.split("_")[1])
files = sorted(pathlib.Path("slides").glob("slide_*"), key=number)
slides, slide = [pathlib.Path(pathlib.Path(__file__).name), *files], 0

root = tk.Tk()
root.title("Edge AI & Multimodal Applications in Python")
root.geometry("1100x600")
label = tk.Label(root, font=("Consolas", 13), justify="left", anchor="w")
panel = tk.Frame(root)
panel.pack(side="right", padx=20)
filename = tk.Label(panel, font=("Consolas", 12, "bold"))
filename.pack()

def go(step=0):
    global slide
    slide = (slide + step) % len(slides)
    path = slides[slide]
    label.image = tk.PhotoImage(file=path) if path.suffix == ".png" else ""
    filename.config(text=path.as_posix())
    label.config(text="" if label.image else path.read_text(encoding="utf-8"), image=label.image)

modules = [importlib.import_module(path.stem) for path in files if path.suffix == ".py"]
for module in modules:
    if hasattr(module, "start"):
        module.start(panel, go)
label.pack(side="left", expand=True, fill="both", padx=10)
root.bind("<Left>", lambda event: go(-1))
root.bind("<Right>", lambda event: go(1))
go()
root.mainloop()
