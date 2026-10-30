import sys, pathlib, importlib, tkinter as tk, timer

sys.path.insert(0, "slides")
repo = "github.com/irvan-putra\n/pythonid-10-2026\n/blob/main/\n"
order = lambda path: (int(path.name.split("_")[1]), path.suffix == ".py", path.name)
files = sorted(pathlib.Path("slides").glob("slide_*"), key=order)
intro = sum(order(path)[0] == 0 for path in files)
slides, slide = [*files[:intro], pathlib.Path(pathlib.Path(__file__).name), *files[intro:]], 0

root = tk.Tk()
root.attributes("-fullscreen", True)
ctx = tk.Label(root, font=("Consolas", 13), justify="left", anchor="w")
panel = tk.Frame(root)
panel.pack(side="right", padx=20)
filename = tk.Label(panel, font=("Consolas", 12, "bold"))
filename.pack()
timer.start(panel, slides, lambda: slide)

def go(step=0):
    global slide
    slide = (slide + step) % len(slides)
    path = slides[slide]
    ctx.image = tk.PhotoImage(file=path) if path.suffix == ".png" else ""
    filename.config(text=repo + path.as_posix())
    ctx.config(text="" if ctx.image else path.read_text(encoding="utf-8"), image=ctx.image)

modules = [importlib.import_module(path.stem) for path in files if path.suffix == ".py"]
for module in modules:
    if hasattr(module, "start"):
        module.start(panel, go)
ctx.pack(side="left", expand=True, fill="both", padx=10)
root.bind("<Left>", lambda event: go(-1))
root.bind("<Right>", lambda event: go(1))
go()
root.mainloop()
