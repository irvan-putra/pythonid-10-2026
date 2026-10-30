import pathlib, threading, uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

app, here = FastAPI(), pathlib.Path(__file__).parent

@app.get("/")
def page():
    return FileResponse(here / "slide_9_sensor.html")

@app.get("/{name}.js")
def script(name: str):
    return FileResponse(here / f"{name}.js")

def start(root, go):
    server = {"app": app, "host": "0.0.0.0", "port": 8000, "log_level": "warning"}
    threading.Thread(target=uvicorn.run, kwargs=server, daemon=True).start()
